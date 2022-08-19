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
    with open(f"{helm_chart_path}/Chart.yaml") as file:
        content = yaml.safe_load(file)
    doc["description"] = content.get("description", "unknown")
    doc["apiVersion"] = content.get("apiVersion", "unknown")
    doc["type"] = content.get("type", "unknown")
    doc["name"] = content.get("name", "unknown")
    doc["appVersion"] = content.get("appVersion", "unknown")
    doc["version"] = content.get("version", "unknown")
    logging.debug("done generating metadata doc")
    return doc


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

    if values_yaml is None or values_string == "":
        logging.error("Couldn't import values.yaml")
        raise ValueError

    # determine if a stella description has been added
    stella = "-- stella"
    values_lines = values_string.split("\n")
    for index, line in enumerate(values_lines):
        if stella in line:
            # found a stella doc string
            doc_string = ""
            i = index
            # check if the next line still is a comment, if so add it to docstring
            while values_lines[i + 1].startswith("#"):
                # remove first char (#) and add newline
                calc = values_lines[i + 1].replace("#", "", 1) + "\n"
                if calc[0] == " ":
                    calc = calc.replace(" ", "", 1)
                doc_string += calc
                i += 1
            # this loop starts when no comment is present anymore
            while values_lines[i + 1].strip() == "":
                # if it is whitespace, ignore the line
                i += 1
            # when the loop is terminated, the nearest value name is extracted
            value_name = values_lines[i + 1].split(":")[0].strip()

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
                "name": value_name,
                "description": doc_string,
                "default": {value_name: values_yaml[value_name]},
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
    return doc


def generate_requirements(doc: dict, helm_chart_path: str) -> dict:
    """
    Reads basic requirements/dependency metadata from requirements.yaml into a data structure.
    Parameters:
        doc (dict): Data structure to save to.
        helm_chart_path (str): Path to the chart.
    Returns:
        doc (dict): Generated data structure.
    """
    logging.debug("generating requirements/dependencies doc")
    if not os.path.exists(f"{helm_chart_path}/requirements.yaml"):
        return doc

    with open(f"{helm_chart_path}/requirements.yaml") as file:
        req_yaml = yaml.safe_load(file)

    doc["dependencies"] = req_yaml["dependencies"]
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
                    "from Template": tmpl['path']
                })

        logging.debug("done generating objects doc")
    return doc
