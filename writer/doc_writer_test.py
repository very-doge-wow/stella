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
