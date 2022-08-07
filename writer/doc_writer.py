import logging
import yaml
from markdownTable import markdownTable

def write(output: str, input: dict, template: str):
    """
    Creates a Markdown doc file for the helm chart.
    Uses a custom template if present, else uses a default template.
    Parameters:
        output (str): Output path to save the md file to.
        input (dict): Data structure containing all relevant helm chart information.
        template (str): Path to custom template. If value is empty, uses default template.
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
    translated = input
    for key in input:
        if type(input[key]) == list:
            logging.debug(f"converting list of dicts {key} to md")

            if len(input[key]) > 0:
                md = translate_list_of_dicts_to_md(input[key])
                translated[key] = md

    result = ""
    for line in template_content.split("\n"):
        for keyword in keywords:
            if keyword in line:
                line = line.replace(keyword, str(input[keyword.replace("{", "").replace("}","").strip().replace("stella.","")]))
        result += line + "\n"

    logging.debug("writing output to file")

    with open(output, "w") as file:
        file.write(result)

    logging.info(f"Wrote doc to {output}.")


def translate_list_of_dicts_to_md(input: dict) -> str:
    md = ""

    sort = {}

    for num, key in enumerate(input[0].keys()):
        md += f"| {key.capitalize()} "
        sort[key] = num
    md += " |\n"
    md += "|---" * len(input[0].keys()) + " | \n"

    for dictionary in input:
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
                        md += f"| {value.rstrip()}"
        md += " |\n"
    return md