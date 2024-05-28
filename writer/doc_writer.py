import logging
import yaml
import markdown


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

    html_simple_template = """<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang xml:lang>
<head>
  <meta charset="utf-8" />
  <meta name="generator" content="very-doge-wow/stella" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes" />
  <style type="text/css" media="screen">
    REPLACE_STRING_STYLE
  </style>
</head>
<body>
REPLACE_STRING_BODY
</body>
</html>
"""

    html_advanced_template = r"""<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang xml:lang>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        html {
            --blue: #0288d1;
            --dark-blue: #006da8;
            --light-blue: #E0F2FF;
        }
        
        body, html {
            height: 100%;
            margin: 0;
            font-family: Arial, Helvetica, sans-serif;
        }

        #navbar-outer {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: auto;
            background-color: var(--dark-blue);
            overflow-x: hidden;
            margin-top: 0;
        }

        #navbar, .container {
            max-width: 80%;
            margin: auto;
        }

        #navbar a {
            padding: 1em;
            text-decoration: none;
            color: white;
            display: inline-block;
            height: 100%;
        }

        #navbar a:first-child {
            background-color: var(--blue);
            font-weight: bold;
        }

        #navbar a:hover {
            background-color: var(--blue);
        }

        #search {
            padding: 10px;
            width: 90%;
            margin: 20px auto;
            display: block;
        }
        .content {
            padding: 20px;
            margin-top: 3em;
        }
        .container {
            padding: 20px;
            border: 1px solid #ccc;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        
        table {
            border-collapse: collapse;
            width: 100%;
            display: block;
            overflow: auto;
        }

        td, th {
            border: 1px solid #ddd;
            padding: 8px;
        }

        tr:nth-child(even){
            background-color: #f2f2f2;
        }

        tr:hover {
            background-color: var(--light-blue);
        }

        th {
            padding-top: 12px;
            padding-bottom: 12px;
            text-align: left;
            background-color: var(--blue);
            color: white;
        }

        pre {
            background-color: #E4E4E4;
            padding: 0.5em;
            border-radius: 5px;
        }

        #search {
            width: 98%;
            display: block;
            overflow: auto;
            font-size: medium;
        }
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
        function selectTableBelowHeading(headingText) {
            // Find the heading element with the specified text
            const headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
            let targetHeading = null;
            for (let i = 0; i < headings.length; i++) {
                if (headings[i].textContent.trim() === headingText.trim()) {
                    targetHeading = headings[i];
                    break;
                }
            }

            if (!targetHeading) {
                console.log("Heading not found");
                return null;
            }

            // Find the nearest subsequent table element
            let nextElement = targetHeading.nextElementSibling;
            while (nextElement) {
                if (nextElement.tagName.toLowerCase() === 'table') {
                    return nextElement;
                }
                nextElement = nextElement.nextElementSibling;
            }

            console.log("Table not found below the specified heading");
                return null;
        }

        document.addEventListener("DOMContentLoaded", function () {
            // create dynamic navbar
            const navbar = document.getElementById("navbar");
            const headers = document.querySelectorAll("h1, h2, h3");

            headers.forEach(header => {
                const id = header.textContent.toLowerCase().replace(/\s+/g, '-');
                header.id = id;

                const anchor = document.createElement("a");
                anchor.href = `#${id}`;
                anchor.textContent = header.textContent;
                navbar.appendChild(anchor);
            });

            const navbarFirstItem = document.querySelectorAll("#navbar a")[0]
            navbarFirstItem.innerText = "🏠 " + navbarFirstItem.innerText

            // enable searching values
            const valuesTable = selectTableBelowHeading("Values")
            // add the input field for searching values
            valuesTable.insertAdjacentHTML('beforebegin', '<input type="text" id="search" placeholder="Search...">');

            const searchInput = document.getElementById("search")
            searchInput.addEventListener("input", function () {
                // Declare variables
                var input, filter, tables, tableRows, txtValue;
                input = document.getElementById('search');
                filter = input.value.toUpperCase();
                tableRows = valuesTable.getElementsByTagName('tr');

                // Loop through all tableRows except the first and hide those who don't match the search query
                for (i = 1; i < tableRows.length; i++) {
                    tableRowColumns = tableRows[i].getElementsByTagName("td");
                    txtValue = ""
                    for (j = 0; j < tableRowColumns.length; j++) {
                        additionalText = tableRowColumns[j].textContent || tableRowColumns[j].innerText
                        txtValue += additionalText
                    }
                    if (txtValue.toUpperCase().indexOf(filter) > -1) {
                        tableRows[i].style.display = "";
                    } else {
                        tableRows[i].style.display = "none";
                    }
                }
            });
        });
    </script>
</body>
</html>
"""

    with (open(output, "w") as file):
        if format_html:
            logging.debug("converting md to html before write")
            result = markdown.markdown(result, extensions=["tables"])
        if format_html and not advanced_html:
            if css != "":
                logging.debug("adding custom css to html before write")
                with open(css, "r") as style:
                    result = html_simple_template.replace("REPLACE_STRING_STYLE", style.read()).replace("REPLACE_STRING_BODY", result)
        elif format_html:
            logging.debug("converting md to html before write using advanced html")
            result = html_advanced_template.replace("REPLACE_STRING_BODY", result)
        # simply output the text (md or html, don't care)
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
                        if key != "default" or key != "example":
                            value = value.replace("\n", " ")  # no newlines allowed out of code-blocks
                        md += f"| {value.rstrip()} "
        md += "|\n"
    return md


def count_lines(text):
    # Split the text by newline characters
    lines = text.split('\n')
    # Count the number of lines
    return len(lines)


def get_name_from_keyword(keyword: str) -> str:
    result = keyword.replace("{", "").replace("}", "").strip().replace("stella.", "")
    return result
