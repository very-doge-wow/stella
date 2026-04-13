import logging
import os
import yaml
import markdown


def indent_text(text: str, prefix: str) -> str:
    return "\n".join(prefix + line if line else line for line in text.splitlines())


def write(output: str, doc: dict, template: str, format_html: bool, advanced_html: bool, css: str) -> str:
    """
    Creates a Markdown doc file for the helm chart.
    Uses a custom template if present, else uses a default template.
    Parameters:
        output (str): Output path to save the md file to.
        doc (dict): Data structure containing all relevant helm chart information.
        template (str): Path to custom template. If value is empty, uses default template.
        format_html (bool): Whether to convert the finished md to html before writing to file.
        advanced_html (bool): Whether to use the advanced html template to render the md file.
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

## Commands
{{ stella.commands }}

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
        "{{ stella.values }}",
        "{{ stella.commands }}"
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

    html_simple_template = """<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang xml:lang>
<head>
  <meta charset="utf-8" />
  <meta name="generator" content="very-doge-wow/stella" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes" />
  <title>REPLACE_STRING_TITLE</title>
  <style type="text/css" media="screen">
    REPLACE_STRING_STYLE
  </style>
</head>
<body>
REPLACE_STRING_BODY
</body>
</html>
"""

    writer_dir = os.path.dirname(__file__)
    with open(os.path.join(writer_dir, "advanced.css")) as f:
        advanced_css = f.read()
    with open(os.path.join(writer_dir, "advanced.js")) as f:
        advanced_js = f.read()

    html_advanced_template = r"""<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang xml:lang>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>REPLACE_STRING_TITLE</title>
    <style>
REPLACE_STRING_ADVANCED_STYLE
    </style>
</head>
<body>
    <div id="navbar-outer">
        <div id="navbar"></div>
    </div>
    <div class="content">
        <div class="container">
          REPLACE_STRING_BODY
        </div>
    </div>

    <script>
REPLACE_STRING_ADVANCED_SCRIPT
    </script>
</body>
</html>
"""

    with open(output, "w") as file:
        if format_html:
            logging.debug("Converting Markdown to HTML")
            title_str = f"{doc['name']} - helm chart documentation"
            result = markdown.markdown(result, extensions=["tables"])

            if not advanced_html:
                if css:
                    logging.debug("Adding custom CSS to HTML")
                    with open(css, "r") as style:
                        css_content = style.read()
                    result = html_simple_template.replace("REPLACE_STRING_STYLE", css_content).replace(
                        "REPLACE_STRING_BODY", result)
            else:
                logging.debug("Using advanced HTML template")
                result = html_advanced_template.replace(
                    "REPLACE_STRING_ADVANCED_STYLE", indent_text(advanced_css, "    ")
                ).replace(
                    "REPLACE_STRING_ADVANCED_SCRIPT", indent_text(advanced_js, "        ")
                ).replace("REPLACE_STRING_BODY", result)

            # title is replaced regardless of advanced or simple html
            result = result.replace("REPLACE_STRING_TITLE", title_str)

        file.write(result)

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
        for times in range(len(sort)):
            for key in sort:
                for dict_key in dictionary.keys():
                    if key == dict_key and times == sort[key]:
                        value = dictionary[key]
                        if key == "name":
                            name = value
                        if type(value) == dict:
                            value = yaml.safe_dump(value).replace("|", "\\|")  # escape pipe chars to fix md tables
                        if (key == "default" or key == "example") and value != "":
                            # we should put this into a code-block
                            value = "<pre>" + str(value).lstrip() + "</pre>"
                            # wrap element inside html details element if num of lines exceeded
                            if count_lines(value) >= 15:
                                value = f"<details><summary>Expand</summary>{value}</details>"
                            # replace newlines with html equivalent
                            value = value.replace("\n", "<br>")
                        value = value.replace("\n", "<br>")  # keep newlines explicit
                        md += f"| {value.rstrip()} "
        md += "|\n"
    return md


def count_lines(text):
    # Split the text by newline characters
    lines = text.split("\n")
    # Count the number of lines
    return len(lines)


def get_name_from_keyword(keyword: str) -> str:
    result = keyword.replace("{", "").replace("}", "").strip().replace("stella.", "")
    return result
