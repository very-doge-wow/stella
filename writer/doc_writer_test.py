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
| Banana | Yellow | <pre>Banana-shaped</br>and kinda bent</pre> |
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
| Banana |  | <pre>Banana-shaped:</br>  - list-item</br>  - list-item</br>  image:</br>    - name: busybox</br>    - entrypoint: ["/bin/sh", "-c"]</pre> |
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

    result = doc_writer.write("test/output.md", doc, "test/custom-template-keywords.md", False, "")
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

    result = doc_writer.write("test/output.md", doc, "", False, "")

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

    result = doc_writer.write("test/output.md", doc, "", False, "")
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

    result = doc_writer.write("test/output.md", doc, "", True, "")
    assert result == """<h1 id="unittest">unittest</h1>
<p><img
src="https://img.shields.io/badge/Version-1.0-informational?style=flat-square"
alt="Version: 1.0" /> <img
src="https://img.shields.io/badge/appVersion-1.1-informational?style=flat-square"
alt="Version: 1.1" /> <img
src="https://img.shields.io/badge/apiVersion-1.2-informational?style=flat-square"
alt="Version: 1.2" /> <img
src="https://img.shields.io/badge/Type-application-informational?style=flat-square"
alt="Type: application" /></p>
<h2 id="description">Description</h2>
<p>simple templating test</p>
<h2 id="dependencies">Dependencies</h2>
<p>This chart depends on the following subcharts.</p>
<p><em>No dependencies found.</em></p>
<h2 id="templates">Templates</h2>
<p>The following templates will be deployed.</p>
<p><em>No templates found.</em></p>
<h3 id="objects">Objects</h3>
<p>The aforementioned templates will deploy the following objects.</p>
<table>
<thead>
<tr class="header">
<th>Kind</th>
<th>From template</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>Ingress</td>
<td>template.yaml</td>
</tr>
</tbody>
</table>
<h2 id="values">Values</h2>
<p>The following values can/will be used for deployments.</p>
<table>
<thead>
<tr class="header">
<th>Name</th>
<th>Description</th>
<th>Default</th>
<th>Example</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>ReplicaCount</td>
<td>how many replicas to deploy</td>
<td><pre>1</pre></td>
<td><pre>replicaCount: 2</pre></td>
</tr>
</tbody>
</table>
<p><em>Automatic helm documentation generated using <a
href="https://github.com/very-doge-wow/stella">very-doge-wow/stella</a>.</em></p>
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

    result = doc_writer.write("test/output.md", doc, "", True, "test/style.css")
    assert result == """<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang xml:lang>
<head>
  <meta charset="utf-8" />
  <meta name="generator" content="pandoc" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes" />
  <title>input</title>
  <style>
    code{white-space: pre-wrap;}
    span.smallcaps{font-variant: small-caps;}
    span.underline{text-decoration: underline;}
    div.column{display: inline-block; vertical-align: top; width: 50%;}
    div.hanging-indent{margin-left: 1.5em; text-indent: -1.5em;}
    ul.task-list{list-style: none;}
    .display.math{display: block; text-align: center; margin: 0.5rem auto;}
  </style>
  <style type="text/css">tr {
border-top: 1px solid #ddd;
border-bottom: 1px solid #ddd;
}
th {
display: none;
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
</style>
  <!--[if lt IE 9]>
    <script src="//cdnjs.cloudflare.com/ajax/libs/html5shiv/3.7.3/html5shiv-printshiv.min.js"></script>
  <![endif]-->
</head>
<body>
<h1 id="unittest">unittest</h1>
<p><img src="data:image/svg+xml;charset=utf-8;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB3aWR0aD0iNzgiIGhlaWdodD0iMjAiIHJvbGU9ImltZyIgYXJpYS1sYWJlbD0iVmVyc2lvbjogMS4wIj48dGl0bGU+VmVyc2lvbjogMS4wPC90aXRsZT48ZyBzaGFwZS1yZW5kZXJpbmc9ImNyaXNwRWRnZXMiPjxyZWN0IHdpZHRoPSI1MSIgaGVpZ2h0PSIyMCIgZmlsbD0iIzU1NSIvPjxyZWN0IHg9IjUxIiB3aWR0aD0iMjciIGhlaWdodD0iMjAiIGZpbGw9IiMwMDdlYzYiLz48L2c+PGcgZmlsbD0iI2ZmZiIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZm9udC1mYW1pbHk9IlZlcmRhbmEsR2VuZXZhLERlamFWdSBTYW5zLHNhbnMtc2VyaWYiIHRleHQtcmVuZGVyaW5nPSJnZW9tZXRyaWNQcmVjaXNpb24iIGZvbnQtc2l6ZT0iMTEwIj48dGV4dCB4PSIyNjUiIHk9IjE0MCIgdHJhbnNmb3JtPSJzY2FsZSguMSkiIGZpbGw9IiNmZmYiIHRleHRMZW5ndGg9IjQxMCI+VmVyc2lvbjwvdGV4dD48dGV4dCB4PSI2MzUiIHk9IjE0MCIgdHJhbnNmb3JtPSJzY2FsZSguMSkiIGZpbGw9IiNmZmYiIHRleHRMZW5ndGg9IjE3MCI+MS4wPC90ZXh0PjwvZz48L3N2Zz4=" alt="Version: 1.0" /> <img src="data:image/svg+xml;charset=utf-8;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB3aWR0aD0iOTgiIGhlaWdodD0iMjAiIHJvbGU9ImltZyIgYXJpYS1sYWJlbD0iYXBwVmVyc2lvbjogMS4xIj48dGl0bGU+YXBwVmVyc2lvbjogMS4xPC90aXRsZT48ZyBzaGFwZS1yZW5kZXJpbmc9ImNyaXNwRWRnZXMiPjxyZWN0IHdpZHRoPSI3MSIgaGVpZ2h0PSIyMCIgZmlsbD0iIzU1NSIvPjxyZWN0IHg9IjcxIiB3aWR0aD0iMjciIGhlaWdodD0iMjAiIGZpbGw9IiMwMDdlYzYiLz48L2c+PGcgZmlsbD0iI2ZmZiIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZm9udC1mYW1pbHk9IlZlcmRhbmEsR2VuZXZhLERlamFWdSBTYW5zLHNhbnMtc2VyaWYiIHRleHQtcmVuZGVyaW5nPSJnZW9tZXRyaWNQcmVjaXNpb24iIGZvbnQtc2l6ZT0iMTEwIj48dGV4dCB4PSIzNjUiIHk9IjE0MCIgdHJhbnNmb3JtPSJzY2FsZSguMSkiIGZpbGw9IiNmZmYiIHRleHRMZW5ndGg9IjYxMCI+YXBwVmVyc2lvbjwvdGV4dD48dGV4dCB4PSI4MzUiIHk9IjE0MCIgdHJhbnNmb3JtPSJzY2FsZSguMSkiIGZpbGw9IiNmZmYiIHRleHRMZW5ndGg9IjE3MCI+MS4xPC90ZXh0PjwvZz48L3N2Zz4=" alt="Version: 1.1" /> <img src="data:image/svg+xml;charset=utf-8;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB3aWR0aD0iOTQiIGhlaWdodD0iMjAiIHJvbGU9ImltZyIgYXJpYS1sYWJlbD0iYXBpVmVyc2lvbjogMS4yIj48dGl0bGU+YXBpVmVyc2lvbjogMS4yPC90aXRsZT48ZyBzaGFwZS1yZW5kZXJpbmc9ImNyaXNwRWRnZXMiPjxyZWN0IHdpZHRoPSI2NyIgaGVpZ2h0PSIyMCIgZmlsbD0iIzU1NSIvPjxyZWN0IHg9IjY3IiB3aWR0aD0iMjciIGhlaWdodD0iMjAiIGZpbGw9IiMwMDdlYzYiLz48L2c+PGcgZmlsbD0iI2ZmZiIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZm9udC1mYW1pbHk9IlZlcmRhbmEsR2VuZXZhLERlamFWdSBTYW5zLHNhbnMtc2VyaWYiIHRleHQtcmVuZGVyaW5nPSJnZW9tZXRyaWNQcmVjaXNpb24iIGZvbnQtc2l6ZT0iMTEwIj48dGV4dCB4PSIzNDUiIHk9IjE0MCIgdHJhbnNmb3JtPSJzY2FsZSguMSkiIGZpbGw9IiNmZmYiIHRleHRMZW5ndGg9IjU3MCI+YXBpVmVyc2lvbjwvdGV4dD48dGV4dCB4PSI3OTUiIHk9IjE0MCIgdHJhbnNmb3JtPSJzY2FsZSguMSkiIGZpbGw9IiNmZmYiIHRleHRMZW5ndGg9IjE3MCI+MS4yPC90ZXh0PjwvZz48L3N2Zz4=" alt="Version: 1.2" /> <img src="data:image/svg+xml;charset=utf-8;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB3aWR0aD0iMTA2IiBoZWlnaHQ9IjIwIiByb2xlPSJpbWciIGFyaWEtbGFiZWw9IlR5cGU6IGFwcGxpY2F0aW9uIj48dGl0bGU+VHlwZTogYXBwbGljYXRpb248L3RpdGxlPjxnIHNoYXBlLXJlbmRlcmluZz0iY3Jpc3BFZGdlcyI+PHJlY3Qgd2lkdGg9IjM3IiBoZWlnaHQ9IjIwIiBmaWxsPSIjNTU1Ii8+PHJlY3QgeD0iMzciIHdpZHRoPSI2OSIgaGVpZ2h0PSIyMCIgZmlsbD0iIzAwN2VjNiIvPjwvZz48ZyBmaWxsPSIjZmZmIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LWZhbWlseT0iVmVyZGFuYSxHZW5ldmEsRGVqYVZ1IFNhbnMsc2Fucy1zZXJpZiIgdGV4dC1yZW5kZXJpbmc9Imdlb21ldHJpY1ByZWNpc2lvbiIgZm9udC1zaXplPSIxMTAiPjx0ZXh0IHg9IjE5NSIgeT0iMTQwIiB0cmFuc2Zvcm09InNjYWxlKC4xKSIgZmlsbD0iI2ZmZiIgdGV4dExlbmd0aD0iMjcwIj5UeXBlPC90ZXh0Pjx0ZXh0IHg9IjcwNSIgeT0iMTQwIiB0cmFuc2Zvcm09InNjYWxlKC4xKSIgZmlsbD0iI2ZmZiIgdGV4dExlbmd0aD0iNTkwIj5hcHBsaWNhdGlvbjwvdGV4dD48L2c+PC9zdmc+" alt="Type: application" /></p>
<h2 id="description">Description</h2>
<p>simple templating test</p>
<h2 id="dependencies">Dependencies</h2>
<p>This chart depends on the following subcharts.</p>
<p><em>No dependencies found.</em></p>
<h2 id="templates">Templates</h2>
<p>The following templates will be deployed.</p>
<p><em>No templates found.</em></p>
<h3 id="objects">Objects</h3>
<p>The aforementioned templates will deploy the following objects.</p>
<table>
<thead>
<tr class="header">
<th>Kind</th>
<th>From template</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>Ingress</td>
<td>template.yaml</td>
</tr>
</tbody>
</table>
<h2 id="values">Values</h2>
<p>The following values can/will be used for deployments.</p>
<table>
<thead>
<tr class="header">
<th>Name</th>
<th>Description</th>
<th>Default</th>
<th>Example</th>
</tr>
</thead>
<tbody>
<tr class="odd">
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