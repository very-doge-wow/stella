import re

import yaml
import logging
import os


def read(helm_chart_path: str) -> dict:
    """
    Reads all present chart metadata into a data structure.
    Parameters:
        helm_chart_path (str): Path to the chart.
    Returns:
        doc (dict): Generated data structure.
    """

    # define desired data structure
    doc = {
        "name": "",
        "appVersion": "",
        "apiVersion": "",
        "version": "",
        "description": "",
        "type": "",
        "dependencies": [],
        "values": [],
        "templates": [],
        "objects": [],
        "commands": [
            {
                "description": "",
                "command": ""
            }
        ],
    }

    # get basic metadata for chart
    doc = generate_chart_metadata(doc, helm_chart_path)
    # generate values metadata
    doc = generate_values_doc(doc, helm_chart_path)
    # generate requirements
    doc = generate_requirements(doc, helm_chart_path)
    # generate templates
    doc = generate_templates(doc, helm_chart_path)
    # generate objects
    doc = generate_objects(doc, helm_chart_path)
    # generate default commands
    doc = generate_commands(doc, helm_chart_path)

    return doc


def generate_chart_metadata(doc: dict, helm_chart_path: str) -> dict:
    """
    Reads basic chart metadata from Chart.yaml into a data structure.
    Parameters:
        doc (dict): Data structure to save to.
        helm_chart_path (str): Path to the chart.
    Returns:
        doc (dict): Generated data structure.
    """
    logging.debug("generating metadata doc")
    content = {}
    try:
        with open(f"{helm_chart_path}/Chart.yaml") as file:
            content = yaml.safe_load(file)
    except FileNotFoundError:
        logging.debug("Chart.yaml not found")
    doc["description"] = content.get("description", "unknown")
    doc["apiVersion"] = content.get("apiVersion", "unknown")
    doc["type"] = content.get("type", "unknown")
    doc["name"] = content.get("name", "unknown")
    doc["appVersion"] = content.get("appVersion", "unknown")
    doc["version"] = content.get("version", "unknown")
    logging.debug("done generating metadata doc")
    return doc


def get_value_from_yaml(parsed_yaml: dict, full_path: str) -> dict:
    """
    Takes a full yaml path such as first.second.third and gets
    the associated yaml value from the dictionary. Preserves
    toplevel keys inside the output dict while doing so.
    Parameters:
        parsed_yaml (dict): data structure from which to read
        full_path (str): full path to desired values
    Returns:
        result (dict): Generated data structure.
    """
    keys = full_path.split(".")  # Split the full path into individual keys
    result = {}  # Initialize an empty dictionary to store the result
    current = result  # Set a pointer to the beginning of the result dictionary
    for key in keys[:-1]:  # Iterate over each key except the last one
        current[key] = {}  # Create an empty dictionary for the current key
        current = current[key]  # Move the pointer to the newly created dictionary
        if key in parsed_yaml:  # Check if the current key exists in the parsed_yaml dictionary
            parsed_yaml = parsed_yaml[key]  # Update parsed_yaml to the value corresponding to the current key
        else:
            return result  # If any intermediate key is not found, return the result immediately
    if keys[-1] in parsed_yaml:
        value = parsed_yaml[keys[-1]]
        if isinstance(value, dict):
            current[keys[-1]] = value  # Set the value if it's a dictionary
        elif isinstance(value, list) and not value:
            current[keys[-1]] = []  # Set the value if it's an empty list
        elif isinstance(value, str) and not value.strip():
            current[keys[-1]] = ""  # Set the value if it's an empty string or contains only whitespace
        else:
            current[keys[-1]] = value  # Otherwise, set the value as is
    else:
        current[keys[-1]] = {}  # Set the value to an empty dictionary if it does not exist
    return result  # Return the result dictionary


def build_full_path(i: int, value_name_dirty: str, value_name_clean: str, values_lines: list) -> str:
    """
    Takes a value name and its current index when traversing a values file
    line by line and tries to determine the full path inside the yaml
    document without parsing it. Will evaluate lines above the current
    line and their respective indent until the toplevel is reached, all
    the while building the full path.
    Parameters:
        i (int): current index while traversing values_lines (from outer scope)
        value_name_dirty (str): the current value's name without having removed leading whitespace
        value_name_clean (str): the current value's name sanitized
        values_lines (list): list of all lines in the values document
    Returns:
        full_path (str): Full path to the currently evaluated value inside the document.
    """
    # first element will always be the current key's name
    full_path = value_name_clean
    # check if whitespace before key is found
    match = re.search(r"^(\s+).*$", value_name_dirty)
    # if already on top-level, we are done here
    if not match:
        return full_path
    # save original indent to compare against it below
    initial_indent = match.group(0).count(" ")
    index = i
    # save all indents to which a key was already added to full_path, as only one can exist for each indent
    matched_indents = []
    while match:
        # count the indent
        indent_num = match.group(0).count(" ")
        # early exit if already on toplevel
        if indent_num == 0:
            return f"{upper_key}.{full_path}"
        # iterate to the nearest key which is (closer to) top-level
        upper_line = values_lines[index - 1].lstrip()
        # loop ignores empty lines and comments
        while upper_line.startswith("#") or upper_line == "":
            index -= 1
            upper_line = values_lines[index - 1].lstrip()
        # loop terminates when next yaml key is found
        index -= 1
        # index now points to the line with the key
        value_name_dirty = values_lines[index].split(":")[0]
        upper_key = value_name_dirty.strip()
        match_new = re.search(r"^\s+", value_name_dirty)
        if match_new:
            indent_num_new = match_new.group(0).count(" ")
            # make sure the found key is actually closer to top-level than the first one by counting indent
            if indent_num > indent_num_new and initial_indent > indent_num_new and (indent_num_new not in matched_indents):
                full_path = f"{upper_key}.{full_path}"
                matched_indents.append(indent_num_new)
        match = re.search(r"^\s*", value_name_dirty)
    return full_path


def generate_values_doc(doc: dict, helm_chart_path: str) -> dict:
    """
    Reads stella doc strings from values.yaml and assigns them to a specific value entry.
    Extracts name, description, default and example of value and saves it into a data structure.
    Parameters:
        doc (dict): data structure to save to
        helm_chart_path (str): Path to the chart.
    Returns:
        doc (dict): Generated data structure.
    """
    logging.debug("generating values doc")

    with open(f"{helm_chart_path}/values.yaml", "r") as values_file:
        values_yaml = yaml.safe_load(values_file)
    with open(f"{helm_chart_path}/values.yaml", "r") as values_file:
        values_string = values_file.read()

    # determine if a stella description has been added
    stella = "-- stella"
    values_lines = values_string.split("\n")
    for index, line in enumerate(values_lines):
        if stella in line:
            # found a stella doc string
            # get the indent
            match = re.search(r"^(\s+).*$", line)
            indent_num = match.group(0).count(" ")-1 if match else 0
            doc_string = ""
            i = index
            # check if the next line still is a comment, if so add it to docstring
            while values_lines[i + 1].lstrip().startswith("#"):
                # remove first char (#) and add newline
                calc = values_lines[i + 1].replace("#", "", 1).replace(" ", "", indent_num) + "\n"
                if indent_num == 0 and calc[0] == " ":
                    calc = calc.replace(" ", "", 1)
                doc_string += calc
                i += 1
            # this loop starts when no comment is present anymore
            while values_lines[i + 1].strip() == "":
                # if it is whitespace, ignore the line
                i += 1

            # when the loop is terminated, the nearest value name is extracted
            i += 1
            value_name_dirty = values_lines[i].split(":")[0]
            value_name_sanitized = value_name_dirty.strip()
            # if it is not a top-level value, we need to determine the entire yaml path to the element
            full_path = build_full_path(i, value_name_dirty, value_name_sanitized, values_lines)

            # check if an example is present in the docstring
            example_delimiter = "-- example"
            example = ""
            if example_delimiter in doc_string:
                doc_string_lines = doc_string.split("\n")
                for j, l in enumerate(doc_string_lines):
                    if example_delimiter in l:
                        split = doc_string.split(l)
                        doc_string = split[0]
                        example = split[1]

            # write the generated values to the output data structure
            doc["values"].append({
                "name": full_path,
                "description": doc_string,
                "default": get_value_from_yaml(values_yaml, full_path),
                "example": example.replace("|", "\\|")  # escape pipe symbol to correctly render md table
            })
    # also add doc entries for values that do not have stella docstrings
    for values in values_yaml:
        docs_created = False
        for dictionary in doc["values"]:
            for value in dictionary.values():
                if values == value:
                    docs_created = True
        if not docs_created:
            doc["values"].append({
                "name": values,
                "description": "",
                "default": {values: values_yaml[values]},
                "example": ""
            })

    # sort values alphabetically
    doc["values"] = sorted(doc["values"], key=lambda item: item["name"])
    return doc


def generate_requirements(doc: dict, helm_chart_path: str) -> dict:
    """
    Reads basic requirements/dependency metadata from requirements.yaml
    or from Chart.yaml into a data structure.
    Parameters:
        doc (dict): Data structure to save to.
        helm_chart_path (str): Path to the chart.
    Returns:
        doc (dict): Generated data structure.
    """
    logging.debug("generating requirements/dependencies doc")
    if not os.path.exists(f"{helm_chart_path}/requirements.yaml"):
        with open(f"{helm_chart_path}/Chart.yaml") as file:
            dep_yaml = yaml.safe_load(file)
            if "dependencies" not in dep_yaml:
                return doc
    else:
        with open(f"{helm_chart_path}/requirements.yaml") as file:
            dep_yaml = yaml.safe_load(file)

    doc["dependencies"] = dep_yaml["dependencies"]
    logging.debug("done generating requirements/dependencies doc")
    return doc


def generate_templates(doc: dict, helm_chart_path: str) -> dict:
    """
    Reads names of all present templates into a data structure.
    Parameters:
        doc (dict): Data structure to save to.
        helm_chart_path (str): Path to the chart.
    Returns:
        doc (dict): Generated data structure.
    """
    logging.debug("generating templates doc")
    files = os.listdir(f"{helm_chart_path}/templates")
    templates = []
    for file in files:
        if file.endswith(".yaml"):
            templates.append({"path": file})
    doc["templates"] = templates
    logging.debug("done generating templates doc")
    return doc


def generate_objects(doc: dict, helm_chart_path: str) -> dict:
    """
    Extracts objects from templates and saves them to a data structure.
    Parameters:
        doc (dict): Data structure to save to.
        helm_chart_path (str): Path to the chart.
    Returns:
        doc (dict): Generated data structure.
    """
    logging.debug("generating objects doc")

    for tmpl in doc["templates"]:
        with open(f"{helm_chart_path}/templates/{tmpl['path']}") as file:
            tmpl_string = file.read()

        objects = []
        for line in tmpl_string.split("\n"):
            if line.startswith("kind:"):
                objects.append(line.split("kind:")[1].strip())

        for obj in objects:
            if obj != "" and type(obj) == str:
                doc["objects"].append({
                    "kind": obj,
                    "from Template": tmpl["path"]
                })

        logging.debug("done generating objects doc")
    return doc


def generate_commands(doc: dict, helm_chart_path: str) -> dict:
    """
    Generates default commands for the chart and saves them to a data structure.
    Parameters:
        doc (dict): Data structure to save to.
        helm_chart_path (str): Path to the chart.
    Returns:
        doc (dict): Generated data structure.
    """
    doc["commands"] = []
    with open(f"{helm_chart_path}/Chart.yaml") as file:
        custom_yaml = yaml.safe_load(file)

    if not custom_yaml.get("annotations"):
        return doc

    if not any("stella" in annotation for annotation in custom_yaml.get("annotations")):
        return doc

    repo = custom_yaml.get("annotations").get("stella/repo", "unknown")
    repo_alias = custom_yaml.get("annotations").get("stella/repo-alias", "unknown")
    version = custom_yaml.get("version")
    name = custom_yaml.get("name")

    repo_add = f"<pre>helm repo add {repo_alias} {repo}</pre>"
    install = f"<pre>helm upgrade --install --wait my-release {repo_alias}/{name} --version {version}</pre>"

    doc["commands"] = [
        {
            "command": repo_add,
            "description": "Adds the remote repository."
        },
        {
            "command": install,
            "description": "Installs the given version of the chart."
        }
    ]
    return doc
