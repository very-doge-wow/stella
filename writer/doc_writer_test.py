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

    result = doc_writer.write("test/output.md", doc, "test/custom-template-keywords.md")
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

    result = doc_writer.write("test/output.md", doc, "")

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

    result = doc_writer.write("test/output.md", doc, "")
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
