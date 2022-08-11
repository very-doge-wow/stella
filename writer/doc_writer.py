import logging
import yaml
import pandoc
import tempfile


def write(output: str, doc: dict, template: str, format_html: bool, css: str) -> str:
    """
    Creates a Markdown doc file for the helm chart.
    Uses a custom template if present, else uses a default template.
    Parameters:
        output (str): Output path to save the md file to.
        doc (dict): Data structure containing all relevant helm chart information.
        template (str): Path to custom template. If value is empty, uses default template.
        format_html (bool): Whether to convert the finished md to html before writing to file.
        css (str): Path to optional css file for html generation.
    """
    logging.debug("starting to write doc from generated data")

    if template != "":
        logging.debug("found custom template, using it now")
        with open(template) as file:
            template_content = file.read()
    else:
        logging.debug("using default template")
        template_content = """
# {{ stella.name }}
![Version: {{ stella.version }}](https://img.shields.io/badge/Version-{{ stella.version }}-informational?style=flat-square) ![Version: {{ stella.appVersion }}](https://img.shields.io/badge/appVersion-{{ stella.appVersion }}-informational?style=flat-square) ![Version: {{ stella.apiVersion }}](https://img.shields.io/badge/apiVersion-{{ stella.apiVersion }}-informational?style=flat-square) ![Type: {{ stella.type }}](https://img.shields.io/badge/Type-{{ stella.type }}-informational?style=flat-square) 

## Description
{{ stella.description }}

## Dependencies
This chart depends on the following subcharts.

{{ stella.dependencies }}

## Templates
The following templates will be deployed.

{{ stella.templates }}

### Objects
The aforementioned templates will deploy the following objects.

{{ stella.objects }}

## Values
The following values can/will be used for deployments.

{{ stella.values }}

*Automatic helm documentation generated using [very-doge-wow/stella](https://github.com/very-doge-wow/stella).*
"""

    keywords = [
        "{{ stella.name }}",
        "{{ stella.version }}",
        "{{ stella.appVersion }}",
        "{{ stella.apiVersion }}",
        "{{ stella.type }}",
        "{{ stella.description }}",
        "{{ stella.dependencies }}",
        "{{ stella.templates }}",
        "{{ stella.objects }}",
        "{{ stella.values }}"
    ]

    # transform dicts to md tables
    translated = doc
    for key in translated:
        if type(translated[key]) == list:
            logging.debug(f"converting list of dicts {key} to md")

            if len(translated[key]) > 0:
                md = translate_list_of_dicts_to_md(doc[key])
                translated[key] = md
            else:
                md = f"*No {get_name_from_keyword(key)} found.*"
                translated[key] = md

    result = ""
    for line in template_content.split("\n"):
        for keyword in keywords:
            if keyword in line:
                line = line.replace(keyword, str(
                    translated[get_name_from_keyword(keyword)]))
        result += line + "\n"

    logging.debug("writing output to file")

    with open(output, "wb") as file:
        if format_html:
            logging.debug("converting md to html before write")
            # convert md to html and output as file / gfm = github-flavored-markdown
            doc = pandoc.read(source=result, format="gfm+raw_html")
            # pass custom css if desired
            write_options = []
            if css != "":
                write_options.append("--self-contained")
                write_options.append(f"--css={css}")
            result = pandoc.write(doc=doc, file=file, format="html", options=write_options)
        else:
            # simply output md
            file.write(bytes(result, encoding="utf-8"))

    logging.info(f"Wrote doc to {output}.")
    return result


def translate_list_of_dicts_to_md(list_of_dicts: list) -> str:
    """
    Creates a Markdown table from a list of python dictionaries.
    Parameters:
        list_of_dicts (list[dict]): Data structure containing all relevant helm chart information.
    Returns:
        md (str): Markdown table created from dict.
    """
    md = ""

    sort = {}

    for num, key in enumerate(list_of_dicts[0].keys()):
        md += f"| {key.capitalize()} "
        sort[key] = num
    md += "|\n"
    md += "|---" * len(list_of_dicts[0].keys()) + "| \n"

    for dictionary in list_of_dicts:
        name = ""
        for times in range(len(sort)):
            for key in sort:
                for dict_key in dictionary.keys():
                    if key == dict_key and times == sort[key]:
                        value = dictionary[key]
                        if key == "name":
                            name = value
                        if type(value) == dict:
                            value = yaml.safe_dump({name: value})
                        if (key == "default" or key == "example") and value != "":
                            # we should put this into a code-block
                            value = "<pre>" + str(value).lstrip()
                            value = value.replace("\n", "</br>")
                            value = value + "</pre>"
                        if key != "default" or key != "example":
                            value = value.replace("\n", " ")  # no newlines allowed out of code-blocks
                        md += f"| {value.rstrip()} "
        md += "|\n"
    return md


def get_name_from_keyword(keyword: str) -> str:
    result = keyword.replace("{", "").replace("}", "").strip().replace("stella.", "")
    return result
