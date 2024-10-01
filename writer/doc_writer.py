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

    html_advanced_template = r"""<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang xml:lang>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>REPLACE_STRING_TITLE</title>
    <style>
html {
    --blue: #A8DADC;   /* Pastel Cyan */
    --dark-blue: #457B9D;   /* Steel Blue */
    --light-blue: #F1FAEE;  /* Honeydew */
    --light-gray: #F8F9FA;  /* Light Gray */
    --gray: #D8E2DC;        /* Soft Gray */
    --dark-gray: #264653;   /* Deep Green */
    --dark-bg: #343A40;     /* Charcoal */
    --dark-card-bg: #495057; /* Granite */
    --dark-text: #E9ECEF;   /* Light Gray Text for Dark Mode */
    --darker-text: #121212; /* Dark text for Dark Mode */
    --dark-gray-text: #264653; /* Deep Green for Dark Mode Text */
    --dark-link: #A8DADC;   /* Pastel Cyan for Links */
    --dark-link-hover: #81B1BD; /* Steel Blue for Hover */
    --primary-gradient: linear-gradient(135deg, #A8DADC, #F1FAEE); /* Cyan to Honeydew */
    --secondary-gradient: linear-gradient(135deg, #457B9D, #A8DADC); /* Steel Blue to Cyan */
    --margin-top: 3em;
    --border-radius: 15px;
}

body, html {
    height: 100%;
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", "Liberation Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
    background-color: var(--light-gray);
    color: var(--dark-gray);
    transition: all 0.3s;
}

#navbar-outer {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: auto;
    background: var(--secondary-gradient);
    overflow-x: hidden;
    margin-top: 0;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    z-index: 1000;
    transition: all 0.3s;
}

#navbar, .container {
    max-width: 80%;
    margin: auto;
}

#navbar a {
    padding: 1em;
    text-decoration: none;
    color: var(--light-gray);
    display: inline-block;
    transition: background-color 0.3s, transform 0.3s;
    border-radius: var(--border-radius);
}

#navbar a:first-child {
    background: var(--primary-gradient);
    font-weight: bold;
    color: var(--dark-gray);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

#navbar a:hover {
    background: var(--primary-gradient);
    transform: translateY(-2px);
    color: var(--dark-gray);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}

#search {
    position: relative;
    padding: 15px;
    width: 98%;
    margin: 20px auto;
    display: block;
    font-size: medium;
    color: var(--dark-gray);
    border: none;
    border-radius: var(--border-radius);
    background: var(--light-gray);
    box-shadow: inset 6px 6px 12px #ccc, inset -6px -6px 12px #fff;
    transition: all 0.3s;
}

#search:focus {
    box-shadow: inset 6px 6px 12px #bbb, inset -6px -6px 12px #eee, 0 0 8px 2px rgba(248, 241, 225, 0.5);
    outline: none;
}

.content {
    padding: 25px;
    margin-top: var(--margin-top);
    background-color: white;
    border-radius: var(--border-radius);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: all 0.3s;
    background: var(--light-gray);
    overflow: hidden;
}

.container {
    padding: 25px;
    border-radius: var(--border-radius);
    box-shadow: 4px 4px 8px #ccc, -4px -4px 8px #fff;
    background-color: var(--light-gray);
    transition: all 0.3s;
    overflow: hidden;
}

table {
    border-collapse: collapse;
    background-color: white;
    border-radius: var(--border-radius);
    box-shadow: 0 0 8px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
    max-width: 100%; /* Prevents the table from exceeding the container's width */
    table-layout: fixed; /* Ensures the table columns distribute the width evenly */
    overflow-x: scroll;  /* Enables horizontal scrolling if content exceeds container width */
    display: inline-block; /* Allows the table to overflow horizontally */
    transition: all 0.3s;
}

td, th {
    border: 1px solid var(--gray);
    padding: 12px;
    transition: background-color 0.3s;
}

tr:nth-child(even) {
    background-color: #E9ECEF; /* Soft Light Gray */
}

tr:hover {
    background-color: #D8E2DC; /* Very Soft Gray */
}

th {
    padding-top: 14px;
    padding-bottom: 14px;
    text-align: left;
    background: var(--secondary-gradient);
    color: var(--light-gray);
}

pre {
    background-color: #E4E4E4;
    padding: 15px;
    border-radius: var(--border-radius);
    overflow-x: auto;
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
    transition: all 0.3s;
}

h1, h2, h3, h4, h5, h6 {
    scroll-margin-top: var(--margin-top);
    color: var(--dark-gray);
    transition: color 0.3s;
}

/* Dark Mode */
@media (prefers-color-scheme: dark) {
    body, html {
        background-color: var(--dark-bg);
        color: var(--dark-text);
    }

    #navbar-outer {
        background: var(--primary-gradient);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.5);
    }

    #navbar a {
        color: var(--dark-gray-text); /* Make navbar links text darker */
    }

    #navbar a:first-child {
        background: var(--secondary-gradient);
        color: var(--light-gray);
    }

    #navbar a:hover {
        background: var(--secondary-gradient);
        color: var(--light-gray);
    }

    #search {
        background: var(--dark-card-bg);
        color: var(--dark-text);
        box-shadow: inset 6px 6px 12px #292d31, inset -6px -6px 12px #5a616a;
    }

    #search:focus {
        box-shadow: inset 6px 6px 12px #292d31, inset -6px -6px 12px #5a616a, 0 0 8px 2px rgba(168, 218, 220, 0.5);
    }

    .content, .container {
        background: var(--dark-card-bg);
        box-shadow: 4px 4px 8px #292d31, -4px -4px 8px #5a616a;
    }

    table {
        background-color: var(--dark-card-bg);
        box-shadow: 0 0 8px rgba(0, 0, 0, 0.5);
    }

    td, th {
        border: 1px solid #555;
    }

    tr:nth-child(even) {
        background-color: #42474d; /* Dark Granite */
    }

    tr:hover {
        background-color: #3c3f41; /* Slightly lighter dark granite */
    }

    th {
        background: var(--primary-gradient);
        color: var(--dark-gray-text); /* Make table header text darker */
    }

    pre {
        background-color: #333;
    }

    h1, h2, h3, h4, h5, h6 {
        color: var(--light-blue);
    }

    a {
        color: var(--dark-link);
        transition: color 0.3s;
    }

    a:hover {
        color: var(--dark-link-hover);
    }
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
                result = html_advanced_template.replace("REPLACE_STRING_BODY", result)

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
                            value = value.replace("\n", "<br>") # keep newlines explicit
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
    lines = text.split("\n")
    # Count the number of lines
    return len(lines)


def get_name_from_keyword(keyword: str) -> str:
    result = keyword.replace("{", "").replace("}", "").strip().replace("stella.", "")
    return result
