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

    html_advanced_template = r"""<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang xml:lang>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>REPLACE_STRING_TITLE</title>
    <style>
/* Theme tokens */
:root {
  --bg: #0b1220;
  --surface: #0f172a;
  --muted: #0b1426;
  --border: #172036;
  --text: #e5e7eb;
  --text-muted: #cbd5e1;

  --primary: #22d3ee;
  --primary-600: #06b6d4;
  --primary-100: #083344;

  --radius: 14px;
  --radius-sm: 10px;
  --shadow-sm: 0 2px 10px rgba(2, 8, 23, 0.5);
  --shadow-md: 0 18px 50px rgba(2, 8, 23, 0.55);
  --ring: 0 0 0 3px rgba(34, 211, 238, 0.25);
  --navbar-height: 64px;
}

/* Base */
html, body {
  height: 100% !important;
  margin: 0 !important;
  color: var(--text) !important;
  background: radial-gradient(1200px 800px at 10% -10%, var(--muted) 0%, var(--bg) 30%, var(--bg) 100%) !important;
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol" !important;
  line-height: 1.6 !important;
  -webkit-font-smoothing: antialiased !important;
  -moz-osx-font-smoothing: grayscale !important;
  scroll-behavior: smooth !important;
}

/* Navbar */
#navbar-outer {
  position: fixed !important;
  inset: 0 0 auto 0 !important;
  height: var(--navbar-height) !important;
  display: flex !important;
  align-items: center !important;
  background: linear-gradient(135deg, rgba(34, 211, 238, 0.12), rgba(6, 182, 212, 0.12)) !important;
  backdrop-filter: saturate(180%) blur(10px) !important;
  border-bottom: 1px solid var(--border) !important;
  box-shadow: var(--shadow-sm) !important;
  z-index: 1000 !important;
}

#navbar {
  width: 100% !important;
  max-width: 1200px !important;
  padding: 0 20px !important;
  margin: 0 auto !important;
  display: flex !important;
  align-items: center !important;
  gap: 10px !important;
  overflow-x: auto !important;
  white-space: nowrap !important;
  scrollbar-width: thin !important;
}

#navbar a {
  display: inline-flex !important;
  align-items: center !important;
  padding: 10px 14px !important;
  color: var(--text) !important;
  text-decoration: none !important;
  border: 1px solid var(--border) !important;
  background: var(--surface) !important;
  border-radius: 999px !important;
  font-weight: 600 !important;
  letter-spacing: 0.01em !important;
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease, background-color 0.2s ease, color 0.2s ease !important;
}

#navbar a:first-child {
  background: linear-gradient(135deg, var(--primary-100), var(--surface)) !important;
  border-color: rgba(34, 211, 238, 0.35) !important;
  color: var(--primary-600) !important;
  box-shadow: 0 6px 16px rgba(34, 211, 238, 0.15) !important;
}

#navbar a:hover {
  transform: translateY(-1px) !important;
  border-color: rgba(34, 211, 238, 0.5) !important;
  color: var(--primary-600) !important;
  box-shadow: 0 10px 22px rgba(34, 211, 238, 0.18) !important;
}

/* Layout wrappers */
.content {
  margin: calc(var(--navbar-height) + 24px) auto 40px !important;
  padding: 0 16px !important;
}

.container {
  max-width: 1200px !important;
  margin: 0 auto !important;
  padding: 28px 24px !important;
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  box-shadow: var(--shadow-md) !important;
  overflow: auto !important; /* allow horizontal scroll for wide tables */
}

/* Typography */
h1, h2, h3, h4, h5, h6 {
  scroll-margin-top: calc(var(--navbar-height) + 16px) !important;
  color: var(--text) !important;
  margin: 0 0 12px !important;
  letter-spacing: 0.02em !important;
}

h1 { font-size: 28px !important; font-weight: 800 !important; }
h2 { font-size: 22px !important; font-weight: 700 !important; margin-top: 28px !important; }
h3 { font-size: 18px !important; font-weight: 700 !important; margin-top: 24px !important; }

p { margin: 10px 0 16px !important; color: var(--text) !important; }
em { color: var(--text-muted) !important; }

/* Links */
a {
  color: var(--primary-600) !important;
  text-decoration: none !important;
  transition: color 0.15s ease, opacity 0.15s ease !important;
}
a:hover { color: var(--primary) !important; opacity: 0.95 !important; }

/* Images (badges etc.) */
img { max-width: 100% !important; height: auto !important; vertical-align: middle !important; border-radius: 8px !important; }

/* Search input (inserted by JS) */
#search {
  position: sticky !important;
  top: calc(var(--navbar-height) + 10px) !important;
  z-index: 5 !important;
  display: block !important;
  width: 40% !important;
  margin: 14px 0 18px !important;
  padding: 12px 16px !important;
  font-size: 14px !important;
  color: var(--text) !important;
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: 999px !important;
  box-shadow: var(--shadow-sm) !important;
}
#search::placeholder { color: var(--text-muted) !important; opacity: 0.7 !important; }
#search:focus { outline: none !important; border-color: var(--primary) !important; box-shadow: var(--ring), var(--shadow-sm) !important; }

/* Tables (non-sticky header to avoid broken rendering) */
table {
  width: 100% !important;
  border-collapse: separate !important; /* crisp radius */
  border-spacing: 0 !important;
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  box-shadow: var(--shadow-sm) !important;
  margin: 16px 0 !important;
  display: table !important; /* ensure native table layout */
}

thead tr th {
  position: relative !important; /* remove sticky */
  top: auto !important;
  z-index: 1 !important;
  background: var(--surface) !important;              /* solid background fixes header artifacts */
  background-image: linear-gradient(180deg, rgba(34, 211, 238, 0.10), rgba(34, 211, 238, 0.06)) !important;
  color: var(--text) !important;
  border-bottom: 1px solid var(--border) !important;
  padding: 12px 14px !important;
  text-align: left !important;
  font-weight: 700 !important;
  font-size: 13px !important;
  letter-spacing: 0.02em !important;
}

tbody tr { transition: background-color 0.15s ease !important; }
tbody tr:nth-child(odd) { background-color: transparent !important; }
tbody tr:nth-child(even) { background-color: rgba(255, 255, 255, 0.02) !important; }
tbody tr:hover { background-color: rgba(34, 211, 238, 0.08) !important; }

td, th {
  border: 1px solid var(--border) !important;
  padding: 12px 14px !important;
  vertical-align: top !important;
  font-size: 14px !important;
  color: var(--text) !important;
}

/* Rounded corners */
table thead tr th:first-child { border-top-left-radius: var(--radius) !important; }
table thead tr th:last-child { border-top-right-radius: var(--radius) !important; }
table tbody tr:last-child td:first-child { border-bottom-left-radius: var(--radius) !important; }
table tbody tr:last-child td:last-child { border-bottom-right-radius: var(--radius) !important; }

/* Code blocks */
pre {
  margin: 8px 0 !important;
  padding: 12px 14px !important;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.03), rgba(255, 255, 255, 0.05)), var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-sm) !important;
  color: var(--text) !important;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace !important;
  font-size: 13px !important;
  line-height: 1.55 !important;
  overflow-x: auto !important;
  white-space: pre !important;
}

code, kbd {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace !important;
  background: rgba(255, 255, 255, 0.05) !important;
  border: 1px solid var(--border) !important;
  padding: 0.1em 0.35em !important;
  border-radius: 6px !important;
}

/* Details/summary */
details {
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-sm) !important;
  background: var(--surface) !important;
  box-shadow: var(--shadow-sm) !important;
  margin: 10px 0 !important;
}
summary {
  cursor: pointer !important;
  padding: 10px 12px !important;
  font-weight: 600 !important;
  color: var(--primary-600) !important;
  outline: none !important;
  list-style: none !important;
}
summary::-webkit-details-marker { display: none !important; }
details[open] summary {
  border-bottom: 1px solid var(--border) !important;
  background: linear-gradient(0deg, rgba(34, 211, 238, 0.06), rgba(34, 211, 238, 0.06)) var(--surface) !important;
}

/* Scrollbars */
* { scrollbar-width: thin !important; scrollbar-color: var(--border) transparent !important; }
*::-webkit-scrollbar { height: 10px !important; width: 10px !important; }
*::-webkit-scrollbar-track { background: transparent !important; }
*::-webkit-scrollbar-thumb { background-color: var(--border) !important; border-radius: 999px !important; border: 2px solid transparent !important; }
*::-webkit-scrollbar-thumb:hover { background-color: var(--primary) !important; }
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
