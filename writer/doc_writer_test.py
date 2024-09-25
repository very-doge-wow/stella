import doc_writer as doc_writer


def test_translate_list_of_dicts_to_md_simple():
    list_of_dicts = [
        {
            "Name": "Banana",
            "Color": "Yellow",
            "Shape": "Banana-shaped",
        },
        {
            "Name": "Pear",
            "Color": "Green",
            "Shape": "Pear-shaped",
        }
    ]

    md_table = doc_writer.translate_list_of_dicts_to_md(list_of_dicts)
    assert md_table == """| Name | Color | Shape |
|---|---|---| 
| Banana | Yellow | Banana-shaped |
| Pear | Green | Pear-shaped |
"""


def test_translate_list_of_dicts_to_md_multiline():
    list_of_dicts = [
        {
            "Name": "Banana",
            "Color": "Yellow",
            "Shape": "Banana-shaped\nand kinda bent",
        },
        {
            "Name": "Pear",
            "Color": "Green",
            "Shape": "Pear-shaped",
        }
    ]

    md_table = doc_writer.translate_list_of_dicts_to_md(list_of_dicts)
    assert md_table == """| Name | Color | Shape |
|---|---|---| 
| Banana | Yellow | Banana-shaped and kinda bent |
| Pear | Green | Pear-shaped |
"""


def test_translate_list_of_dicts_to_md_multiline_with_codeblock():
    list_of_dicts = [
        {
            "Name": "Banana",
            "Color": "Yellow",
            "example": "Banana-shaped\nand kinda bent",
        },
        {
            "Name": "Pear",
            "Color": "Green",
            "example": "Pear-shaped",
        }
    ]

    md_table = doc_writer.translate_list_of_dicts_to_md(list_of_dicts)
    assert md_table == """| Name | Color | Example |
|---|---|---| 
| Banana | Yellow | <pre>Banana-shaped<br>and kinda bent</pre> |
| Pear | Green | <pre>Pear-shaped</pre> |
"""


def test_translate_list_of_dicts_to_md_empty_values():
    list_of_dicts = [
        {
            "Name": "Banana",
            "Color": "",
            "Shape": "Banana-shaped",
        },
        {
            "Name": "Pear",
            "Color": "Green",
            "Shape": "",
        }
    ]

    md_table = doc_writer.translate_list_of_dicts_to_md(list_of_dicts)
    assert md_table == """| Name | Color | Shape |
|---|---|---| 
| Banana |  | Banana-shaped |
| Pear | Green |  |
"""


def test_translate_list_of_dicts_to_md_big_codeblock():
    list_of_dicts = [
        {
            "Name": "Banana",
            "Color": "",
            "default": 'Banana-shaped:\n  - list-item\n  - list-item\n  image:\n    - name: busybox\n    - entrypoint: ["/bin/sh", "-c"]',
        },
        {
            "Name": "Pear",
            "Color": "Green",
            "default": "pear",
        }
    ]

    md_table = doc_writer.translate_list_of_dicts_to_md(list_of_dicts)
    assert md_table == """| Name | Color | Default |
|---|---|---| 
| Banana |  | <pre>Banana-shaped:<br>  - list-item<br>  - list-item<br>  image:<br>    - name: busybox<br>    - entrypoint: ["/bin/sh", "-c"]</pre> |
| Pear | Green | <pre>pear</pre> |
"""


def test_translate_list_of_dicts_to_md_capitalize():
    list_of_dicts = [
        {
            "name": "Banana",
            "color": "",
            "shape": "",
        },
        {
            "name": "Pear",
            "color": "Green",
            "shape": "Pear",
        }
    ]

    md_table = doc_writer.translate_list_of_dicts_to_md(list_of_dicts)
    print(md_table)
    assert md_table == """| Name | Color | Shape |
|---|---|---| 
| Banana |  |  |
| Pear | Green | Pear |
"""


def test_writer_keywords_custom_template():
    doc = {
        "type": "application",
        "version": "1.0",
        "appVersion": "1.1",
        "apiVersion": "1.2",
        "name": "unittest",
        "description": "simple templating test",
        "dependencies": [
            {
                "name": "dependency",
                "condition": "ifEnabled=true",
                "version": "1.3",
                "repository": "https://unit.test/"
            }
        ],
        "templates": [
            {
                "path": "template.yaml"
            }
        ],
        "objects": [
            {
                "kind": "Ingress",
                "from Template": "template.yaml"
            }
        ],
        "values": [
            {
                "name": "ReplicaCount",
                "description": "how many replicas to deploy",
                "default": "1",
                "example": "replicaCount: 2"
            }
        ]
    }

    result = doc_writer.write("test/output.md", doc, "test/custom-template-keywords.md", False, False,"")
    assert result == """unittest

1.0

1.1

1.2

application

simple templating test

| Name | Condition | Version | Repository |
|---|---|---|---| 
| dependency | ifEnabled=true | 1.3 | https://unit.test/ |


| Path |
|---| 
| template.yaml |


| Kind | From template |
|---|---| 
| Ingress | template.yaml |


| Name | Description | Default | Example |
|---|---|---|---| 
| ReplicaCount | how many replicas to deploy | <pre>1</pre> | <pre>replicaCount: 2</pre> |


"""


def test_writer_keywords_default_template():
    doc = {
        "type": "application",
        "version": "1.0",
        "appVersion": "1.1",
        "apiVersion": "1.2",
        "name": "unittest",
        "description": "simple templating test",
        "dependencies": [
            {
                "name": "dependency",
                "condition": "ifEnabled=true",
                "version": "1.3",
                "repository": "https://unit.test/"
            }
        ],
        "templates": [
            {
                "path": "template.yaml"
            }
        ],
        "objects": [
            {
                "kind": "Ingress",
                "from Template": "template.yaml"
            }
        ],
        "values": [
            {
                "name": "ReplicaCount",
                "description": "how many replicas to deploy",
                "default": "1",
                "example": "replicaCount: 2"
            }
        ]
    }

    result = doc_writer.write("test/output.md", doc, "", False, False, "")

    assert result == """
# unittest
![Version: 1.0](https://img.shields.io/badge/Version-1.0-informational?style=flat-square) ![Version: 1.1](https://img.shields.io/badge/appVersion-1.1-informational?style=flat-square) ![Version: 1.2](https://img.shields.io/badge/apiVersion-1.2-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square) 

## Description
simple templating test

## Dependencies
This chart depends on the following subcharts.

| Name | Condition | Version | Repository |
|---|---|---|---| 
| dependency | ifEnabled=true | 1.3 | https://unit.test/ |


## Templates
The following templates will be deployed.

| Path |
|---| 
| template.yaml |


### Objects
The aforementioned templates will deploy the following objects.

| Kind | From template |
|---|---| 
| Ingress | template.yaml |


## Values
The following values can/will be used for deployments.

| Name | Description | Default | Example |
|---|---|---|---| 
| ReplicaCount | how many replicas to deploy | <pre>1</pre> | <pre>replicaCount: 2</pre> |


*Automatic helm documentation generated using [very-doge-wow/stella](https://github.com/very-doge-wow/stella).*

"""


def test_writer_empty():
    doc = {
        "type": "application",
        "version": "1.0",
        "appVersion": "1.1",
        "apiVersion": "1.2",
        "name": "unittest",
        "description": "simple templating test",
        "dependencies": [],
        "templates": [],
        "objects": [
            {
                "kind": "Ingress",
                "from Template": "template.yaml"
            }
        ],
        "values": [
            {
                "name": "ReplicaCount",
                "description": "how many replicas to deploy",
                "default": "1",
                "example": "replicaCount: 2"
            }
        ]
    }

    result = doc_writer.write("test/output.md", doc, "", False, False, "")
    assert result == """
# unittest
![Version: 1.0](https://img.shields.io/badge/Version-1.0-informational?style=flat-square) ![Version: 1.1](https://img.shields.io/badge/appVersion-1.1-informational?style=flat-square) ![Version: 1.2](https://img.shields.io/badge/apiVersion-1.2-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square) 

## Description
simple templating test

## Dependencies
This chart depends on the following subcharts.

*No dependencies found.*

## Templates
The following templates will be deployed.

*No templates found.*

### Objects
The aforementioned templates will deploy the following objects.

| Kind | From template |
|---|---| 
| Ingress | template.yaml |


## Values
The following values can/will be used for deployments.

| Name | Description | Default | Example |
|---|---|---|---| 
| ReplicaCount | how many replicas to deploy | <pre>1</pre> | <pre>replicaCount: 2</pre> |


*Automatic helm documentation generated using [very-doge-wow/stella](https://github.com/very-doge-wow/stella).*

"""


def test_get_name_from_keyword():
    keywords = [
        "{{ stella.lol }}",
        "{{ stella.banana }}",
        "",
        "{{stella.rofl}}",
        "{{pear}}"
    ]

    results = [
        "lol",
        "banana",
        "",
        "rofl",
        "pear"
    ]

    for index, keyword in enumerate(keywords):
        result = doc_writer.get_name_from_keyword(keyword)
        assert results[index] == result


def test_writer_html():
    doc = {
        "type": "application",
        "version": "1.0",
        "appVersion": "1.1",
        "apiVersion": "1.2",
        "name": "unittest",
        "description": "simple templating test",
        "dependencies": [],
        "templates": [],
        "objects": [
            {
                "kind": "Ingress",
                "from Template": "template.yaml"
            }
        ],
        "values": [
            {
                "name": "ReplicaCount",
                "description": "how many replicas to deploy",
                "default": "1",
                "example": "replicaCount: 2"
            }
        ]
    }

    result = doc_writer.write("test/output.md", doc, "", True, False, "")
    assert result == """<h1>unittest</h1>
<p><img alt="Version: 1.0" src="https://img.shields.io/badge/Version-1.0-informational?style=flat-square" /> <img alt="Version: 1.1" src="https://img.shields.io/badge/appVersion-1.1-informational?style=flat-square" /> <img alt="Version: 1.2" src="https://img.shields.io/badge/apiVersion-1.2-informational?style=flat-square" /> <img alt="Type: application" src="https://img.shields.io/badge/Type-application-informational?style=flat-square" /> </p>
<h2>Description</h2>
<p>simple templating test</p>
<h2>Dependencies</h2>
<p>This chart depends on the following subcharts.</p>
<p><em>No dependencies found.</em></p>
<h2>Templates</h2>
<p>The following templates will be deployed.</p>
<p><em>No templates found.</em></p>
<h3>Objects</h3>
<p>The aforementioned templates will deploy the following objects.</p>
<table>
<thead>
<tr>
<th>Kind</th>
<th>From template</th>
</tr>
</thead>
<tbody>
<tr>
<td>Ingress</td>
<td>template.yaml</td>
</tr>
</tbody>
</table>
<h2>Values</h2>
<p>The following values can/will be used for deployments.</p>
<table>
<thead>
<tr>
<th>Name</th>
<th>Description</th>
<th>Default</th>
<th>Example</th>
</tr>
</thead>
<tbody>
<tr>
<td>ReplicaCount</td>
<td>how many replicas to deploy</td>
<td><pre>1</pre></td>
<td><pre>replicaCount: 2</pre></td>
</tr>
</tbody>
</table>
<p><em>Automatic helm documentation generated using <a href="https://github.com/very-doge-wow/stella">very-doge-wow/stella</a>.</em></p>"""


def test_writer_advanced_html():
    doc = {
        "type": "application",
        "version": "1.0",
        "appVersion": "1.1",
        "apiVersion": "1.2",
        "name": "unittest",
        "description": "simple templating test",
        "dependencies": [],
        "templates": [],
        "objects": [
            {
                "kind": "Ingress",
                "from Template": "template.yaml"
            }
        ],
        "values": [
            {
                "name": "ReplicaCount",
                "description": "how many replicas to deploy",
                "default": "1",
                "example": "replicaCount: 2"
            }
        ]
    }

    result = doc_writer.write("test/output.md", doc, "", True, True, "")
    assert result == r"""<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang xml:lang>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>unittest - helm chart documentation</title>
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
}

.container {
    padding: 25px;
    border-radius: var(--border-radius);
    box-shadow: 4px 4px 8px #ccc, -4px -4px 8px #fff;
    background-color: var(--light-gray);
    transition: all 0.3s;
}

.table-container {
    padding: 0 1em;
    overflow: auto;
}

table {
    border-collapse: collapse;
    width: 100%;
    background-color: white;
    border-radius: var(--border-radius);
    box-shadow: 0 0 8px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
    overflow: hidden;
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
          <h1>unittest</h1>
<p><img alt="Version: 1.0" src="https://img.shields.io/badge/Version-1.0-informational?style=flat-square" /> <img alt="Version: 1.1" src="https://img.shields.io/badge/appVersion-1.1-informational?style=flat-square" /> <img alt="Version: 1.2" src="https://img.shields.io/badge/apiVersion-1.2-informational?style=flat-square" /> <img alt="Type: application" src="https://img.shields.io/badge/Type-application-informational?style=flat-square" /> </p>
<h2>Description</h2>
<p>simple templating test</p>
<h2>Dependencies</h2>
<p>This chart depends on the following subcharts.</p>
<p><em>No dependencies found.</em></p>
<h2>Templates</h2>
<p>The following templates will be deployed.</p>
<p><em>No templates found.</em></p>
<h3>Objects</h3>
<p>The aforementioned templates will deploy the following objects.</p>
<table>
<thead>
<tr>
<th>Kind</th>
<th>From template</th>
</tr>
</thead>
<tbody>
<tr>
<td>Ingress</td>
<td>template.yaml</td>
</tr>
</tbody>
</table>
<h2>Values</h2>
<p>The following values can/will be used for deployments.</p>
<table>
<thead>
<tr>
<th>Name</th>
<th>Description</th>
<th>Default</th>
<th>Example</th>
</tr>
</thead>
<tbody>
<tr>
<td>ReplicaCount</td>
<td>how many replicas to deploy</td>
<td><pre>1</pre></td>
<td><pre>replicaCount: 2</pre></td>
</tr>
</tbody>
</table>
<p><em>Automatic helm documentation generated using <a href="https://github.com/very-doge-wow/stella">very-doge-wow/stella</a>.</em></p>
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


def test_writer_html_custom_css():
    doc = {
        "type": "application",
        "version": "1.0",
        "appVersion": "1.1",
        "apiVersion": "1.2",
        "name": "unittest",
        "description": "simple templating test",
        "dependencies": [],
        "templates": [],
        "objects": [
            {
                "kind": "Ingress",
                "from Template": "template.yaml"
            }
        ],
        "values": [
            {
                "name": "ReplicaCount",
                "description": "how many replicas to deploy",
                "default": "1",
                "example": "replicaCount: 2"
            }
        ]
    }

    result = doc_writer.write("test/output.md", doc, "", True, False, "test/style.css")
    assert result == """<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang xml:lang>
<head>
  <meta charset="utf-8" />
  <meta name="generator" content="very-doge-wow/stella" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes" />
  <title>unittest - helm chart documentation</title>
  <style type="text/css" media="screen">
    tr {
    border-top: 1px solid #ddd;
    border-bottom: 1px solid #ddd;
}

body {
  padding: 0 2em;
  font-family: Montserrat, sans-serif;
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
  color: #444;
  background: #eee;
}

h1 {
  font-weight: normal;
  letter-spacing: -1px;
  color: #34495E;
}

/* Styling for HTML tables */
table {
  border-collapse: collapse;
  width: 100%;
}

/* Styling for table headings */
th {
  background-color: lightblue;
  color: black;
}

/* Styling for table rows */
tr:nth-child(even) {
  background-color: #f2f2f2; /* Light gray background */
}

tr:nth-child(odd) {
  background-color: white; /* White background */
}

/* Styling for table cells */
td {
  border: 1px solid black; /* Add borders to table cells */
}

/* Hover effect */
tr:hover {
  background-color: #cce6ff; /* Light blue background on hover */
}

  </style>
</head>
<body>
<h1>unittest</h1>
<p><img alt="Version: 1.0" src="https://img.shields.io/badge/Version-1.0-informational?style=flat-square" /> <img alt="Version: 1.1" src="https://img.shields.io/badge/appVersion-1.1-informational?style=flat-square" /> <img alt="Version: 1.2" src="https://img.shields.io/badge/apiVersion-1.2-informational?style=flat-square" /> <img alt="Type: application" src="https://img.shields.io/badge/Type-application-informational?style=flat-square" /> </p>
<h2>Description</h2>
<p>simple templating test</p>
<h2>Dependencies</h2>
<p>This chart depends on the following subcharts.</p>
<p><em>No dependencies found.</em></p>
<h2>Templates</h2>
<p>The following templates will be deployed.</p>
<p><em>No templates found.</em></p>
<h3>Objects</h3>
<p>The aforementioned templates will deploy the following objects.</p>
<table>
<thead>
<tr>
<th>Kind</th>
<th>From template</th>
</tr>
</thead>
<tbody>
<tr>
<td>Ingress</td>
<td>template.yaml</td>
</tr>
</tbody>
</table>
<h2>Values</h2>
<p>The following values can/will be used for deployments.</p>
<table>
<thead>
<tr>
<th>Name</th>
<th>Description</th>
<th>Default</th>
<th>Example</th>
</tr>
</thead>
<tbody>
<tr>
<td>ReplicaCount</td>
<td>how many replicas to deploy</td>
<td><pre>1</pre></td>
<td><pre>replicaCount: 2</pre></td>
</tr>
</tbody>
</table>
<p><em>Automatic helm documentation generated using <a href="https://github.com/very-doge-wow/stella">very-doge-wow/stella</a>.</em></p>
</body>
</html>
"""


def test_count_lines():
    input_str = """one
    two
    three"""
    assert doc_writer.count_lines(input_str) == 3

    input_str = "just one"
    assert doc_writer.count_lines(input_str) == 1

    input_str = ""
    assert doc_writer.count_lines(input_str) == 1


# test if values/examples are wrapped in html details element
def test_translate_list_of_dicts_to_md_details_summary():
    list_of_dicts = [
        {
            "name": "Banana",
            "description": "Yellow",
            "default": """0 multiline
1 multiline
2 multiline
3 multiline
4 multiline
5 multiline
6 multiline
7 multiline
8 multiline
9 multiline
10 multiline
11 multiline
12 multiline
14 multiline
15 multiline
16 multiline""",
            "example": "lol",
        },
        {
            "name": "Pear",
            "description": "Green",
            "default": "Pear-shaped",
            "example": """0 multiline
1 multiline
2 multiline
3 multiline
4 multiline
5 multiline
6 multiline
7 multiline
8 multiline
9 multiline
10 multiline
11 multiline
12 multiline
14 multiline
15 multiline
16 multiline""",
        },
        {
            "name": "Melon",
            "description": "Green",
            "default": "Melon-shaped",
            "example": "rofl",
        }
    ]

    md_table = doc_writer.translate_list_of_dicts_to_md(list_of_dicts)
    print(md_table)
    assert md_table == """| Name | Description | Default | Example |
|---|---|---|---| 
| Banana | Yellow | <details><summary>Expand</summary><pre>0 multiline<br>1 multiline<br>2 multiline<br>3 multiline<br>4 multiline<br>5 multiline<br>6 multiline<br>7 multiline<br>8 multiline<br>9 multiline<br>10 multiline<br>11 multiline<br>12 multiline<br>14 multiline<br>15 multiline<br>16 multiline</pre></details> | <pre>lol</pre> |
| Pear | Green | <pre>Pear-shaped</pre> | <details><summary>Expand</summary><pre>0 multiline<br>1 multiline<br>2 multiline<br>3 multiline<br>4 multiline<br>5 multiline<br>6 multiline<br>7 multiline<br>8 multiline<br>9 multiline<br>10 multiline<br>11 multiline<br>12 multiline<br>14 multiline<br>15 multiline<br>16 multiline</pre></details> |
| Melon | Green | <pre>Melon-shaped</pre> | <pre>rofl</pre> |
"""
