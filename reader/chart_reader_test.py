
import yaml

import chart_reader
from unittest.mock import Mock
from hamcrest import assert_that, has_entries, contains_inanyorder


def test_read():
    doc = {
        "name": "",
        "appVersion": "",
        "apiVersion": "",
        "version": "",
        "description": "",
        "type": "",
        "dependencies": [],
        "values": [],
        "templates": [],
        "objects": [],
        "commands": [],
    }
    result = chart_reader.read("test/test-chart")
    result["objects"] = sorted(result["objects"], key=lambda item: item.get("kind"))
    result["templates"] = sorted(result["templates"], key=lambda item: item.get("path"))
    assert_that(result, has_entries(
        {"name": "test-chart", "appVersion": "1.16.0", "apiVersion": "v2", "version": "0.1.0",
         "description": "A Helm chart for Kubernetes", "type": "application", "dependencies": [
            {"name": "postgresql", "condition": "postgresql.enabled", "version": "1.2.3",
             "repository": "https://lol.de/repo/"},
            {"name": "mysql", "condition": "mysql.enabled", "version": "1.2.3", "repository": "https://lol.de/repo/"}],
         "values": [
             {"name": "affinity",
              "description": "",
              "default": {"affinity": {}}, "example": ""},{"name": "autoscaling", "description": "", "default":
                 {"autoscaling": {"enabled": False, "minReplicas": 1, "maxReplicas": 100,
                                  "targetCPUUtilizationPercentage": 80}}, "example": ""},
             {"name": "fullnameOverride", "description": "", "default": {"fullnameOverride": ""},
              "example": ""}, {"name": "image", "description": "which image to deploy\n", "default":
                 {"image": {"repository": "nginx", "pullPolicy": "IfNotPresent", "tag": ""}}, "example":
                 '\nimage:\n  repository: very-doge-wow/stella\n  pullPolicy: IfNotPresent\n  tag: "latest"\n'},
             {"name": "imagePullSecrets", "description": "", "default": {"imagePullSecrets": []}, "example": ""},
             {"name": "ingress", "description": "", "default": {"ingress": {"enabled": False, "className": "",
            "annotations": {}, "hosts": [{"host": "chart-example.local", "paths":
             [{"path": "/", "pathType": "ImplementationSpecific"}]}], "tls": []}}, "example": ""},
             {"name": "nameOverride", "description": "", "default": {"nameOverride": ""}, "example": ""},
             {"name": "nodeSelector", "description": "", "default": {"nodeSelector": {}}, "example": ""},
             {"name": "podAnnotations", "description": "", "default": {"podAnnotations": {}}, "example": ""},
             {"name": "podSecurityContext", "description": "", "default": {"podSecurityContext": {}}, "example": ""},
             {"name": "replicaCount", "description": "how many replicas to deploy\n", "default":
                 {"replicaCount": 1}, "example": ""}, {"name": "resources", "description": "", "default":
                 {"resources": {}}, "example": ""}, {"name": "securityContext", "description": "",
                 "default": {"securityContext": {}}, "example": ""}, {"name": "service", "description": "",
                  "default": {"service": {"type": "ClusterIP", "port": 80}}, "example": ""},
             {"name": "serviceAccount", "description": "", "default": {"serviceAccount":
             {"create": True, "annotations": {}, "name": ""}}, "example": ""},
             {"name": "tolerations", "description": "", "default": {"tolerations": []}, "example": ""}],
         "templates": [{"path": "deployment.yaml"}, {"path": "hpa.yaml"}, {"path": "ingress.yaml"},
                       {"path": "service.yaml"}, {"path": "serviceaccount.yaml"}],
         "objects": [{"kind": "Deployment", "from Template": "deployment.yaml"},
                     {"kind": "HorizontalPodAutoscaler", "from Template": "hpa.yaml"},
                     {"kind": "Ingress", "from Template": "ingress.yaml"},
                     {"kind": "Service", "from Template": "service.yaml"},
                     {"kind": "ServiceAccount", "from Template": "serviceaccount.yaml"}],
         "commands": [{"description": "", "command": ""}]}
    ))


def test_generate_chart_metadata_real_file():
    result = chart_reader.generate_chart_metadata({}, "test/test-chart")
    assert_that(result, has_entries(
        {
            "apiVersion": "v2",
            "appVersion": "1.16.0",
            "description": "A Helm chart for Kubernetes",
            "name": "test-chart",
            "type": "application",
            "version": "0.1.0"
        }
    ))


def test_generate_chart_metadata_unknown():
    mocked_content = {}
    real_yaml_load = chart_reader.yaml.safe_load
    chart_reader.yaml.safe_load = Mock(return_value=mocked_content)
    result = chart_reader.generate_chart_metadata({}, "test/test-chart")
    chart_reader.yaml.safe_load = real_yaml_load
    assert_that(result, has_entries(
        {
            "apiVersion": "unknown",
            "appVersion": "unknown",
            "description": "unknown",
            "name": "unknown",
            "type": "unknown",
            "version": "unknown"
        }
    ))


def test_generate_values_doc_and_example():
    doc = {
        "name": "",
        "appVersion": "",
        "apiVersion": "",
        "version": "",
        "description": "",
        "type": "",
        "dependencies": [],
        "values": [],
        "templates": [],
        "objects": [],
        "commands": [],
    }
    result = chart_reader.generate_values_doc(doc, "test/values-stella")
    assert_that(result["values"], contains_inanyorder(
        {
            "name": "replicaCount",
            "description": "how many replicas to deploy\n",
            "default": {"replicaCount": 1}, "example": ""
        },
        {
            "name": "image",
            "description": "which image to deploy\n",
            "default": {"image": {"repository": "nginx", "pullPolicy": "IfNotPresent", "tag": ""}},
            "example": '\nimage:\n  repository: very-doge-wow/stella\n  pullPolicy: IfNotPresent\n  tag: "latest"\n'
        }
    ))


def test_generate_values_doc_only():
    doc = {
        "name": "",
        "appVersion": "",
        "apiVersion": "",
        "version": "",
        "description": "",
        "type": "",
        "dependencies": [],
        "values": [],
        "templates": [],
        "objects": [],
        "commands": [],
    }
    result = chart_reader.generate_values_doc(doc, "test/values-stella-only")
    assert_that(result["values"], contains_inanyorder(
        {
            "name": "replicaCount",
            "description": "how many replicas to deploy\n",
            "default": {"replicaCount": 1}, "example": ""
        }
    ))


def test_generate_values_pipes_in_tables():
    doc = {
        "name": "",
        "appVersion": "",
        "apiVersion": "",
        "version": "",
        "description": "",
        "type": "",
        "dependencies": [],
        "values": [],
        "templates": [],
        "objects": [],
        "commands": [],
    }
    result = chart_reader.generate_values_doc(doc, "test/values-pipes")
    assert_that(result["values"], contains_inanyorder(
        {"name": "customObjects", "description": "Test for using pipes in examples\n", "default": {"customObjects": []}, "example": "\ncustomObjects:\n  - \\|\n    best-string\n"}
    ))


def test_generate_values_comments_in_examples():
    doc = {
        "name": "",
        "appVersion": "",
        "apiVersion": "",
        "version": "",
        "description": "",
        "type": "",
        "dependencies": [],
        "values": [],
        "templates": [],
        "objects": [],
        "commands": [],
    }
    result = chart_reader.generate_values_doc(doc, "test/values-comments-examples")
    print(result)
    assert_that(result["values"], contains_inanyorder(
        {"name": "best", "description": "Test for comments in examples\n", "default": {"best": []},
         "example": "\nbest:\n  # this is a comment inside an example\n  - value\n"}
    ))


def test_generate_values_docs_nested():
    doc = {
        "name": "",
        "appVersion": "",
        "apiVersion": "",
        "version": "",
        "description": "",
        "type": "",
        "dependencies": [],
        "values": [],
        "templates": [],
        "objects": [],
        "commands": [],
    }
    result = chart_reader.generate_values_doc(doc, "test/values-nested-docs")
    print(result)
    assert_that(result["values"], contains_inanyorder(
    {"name": "image", "description": "which image to deploy\n", "default": {"image": {"repository": "nginx", "pullPolicy": "IfNotPresent", "tag": ""}}, "example": "\nimage:\n  repository: very-doge-wow/stella\n  pullPolicy: IfNotPresent\n"}, {"name": "image.tag", "description": "Overrides the image tag whose default is the chart appVersion.\n", "default": {"image": {"tag": ""}}, "example": '\nimage:\n  tag: "latest"\n'}, {"name": "replicaCount", "description": "how many replicas to deploy\n", "default": {"replicaCount": 1}, "example": ""}
    ))


def test_get_value_from_yaml():
    yaml_string = """first:
  second:
    third: "value"
"""
    path = "first.second.third"
    result = chart_reader.get_value_from_yaml(yaml.safe_load(yaml_string), path)
    assert result == {
        "first": {
            "second": {
                "third": "value"
            }
        }
    }

    yaml_string = """first: 1
"""
    path = "first"
    result = chart_reader.get_value_from_yaml(yaml.safe_load(yaml_string), path)
    assert result == {
        "first": 1
    }

    yaml_string = """first:
  - name: lol
    value: rofl
"""
    path = "first"
    result = chart_reader.get_value_from_yaml(yaml.safe_load(yaml_string), path)
    assert result == {
        "first": [{"name": "lol", "value": "rofl"}]
    }

    yaml_string = """first:
  second:
    third: lol
  fourth: rofl
"""
    path = "first.fourth"
    result = chart_reader.get_value_from_yaml(yaml.safe_load(yaml_string), path)
    assert result == {
        "first": {
            "fourth": "rofl"
        }
    }

    yaml_string = """first:
  second:
    third:
      fifth: uhuhu
    fourth: rofl
"""
    path = "first.second.fourth"
    result = chart_reader.get_value_from_yaml(yaml.safe_load(yaml_string), path)
    assert result == {
        "first": {
            "second": {
                "fourth": "rofl"
            }
        }
    }

    yaml_string = """first:
  second:
    third:
      fifth: uhuhu
    fourth: rofl
another: one
"""
    path = "first.second.fourth"
    result = chart_reader.get_value_from_yaml(yaml.safe_load(yaml_string), path)
    assert result == {
        "first": {
            "second": {
                "fourth": "rofl"
            }
        }
    }

    yaml_string = """first:
  second:
    third:
      fifth: uhuhu
    fourth: rofl
another: one
    """
    path = "another"
    result = chart_reader.get_value_from_yaml(yaml.safe_load(yaml_string), path)
    assert result == {
        "another": "one"
    }

    yaml_string = """first: {}
    """
    path = "first"
    result = chart_reader.get_value_from_yaml(yaml.safe_load(yaml_string), path)
    assert result == {
        "first": {}
    }

    yaml_string = """first: []
    """
    path = "first"
    result = chart_reader.get_value_from_yaml(yaml.safe_load(yaml_string), path)
    assert result == {
        "first": []
    }

    yaml_string = """first: ""
    """
    path = "first"
    result = chart_reader.get_value_from_yaml(yaml.safe_load(yaml_string), path)
    assert result == {
        "first": ""
    }

    yaml_string = """first: ''
    """
    path = "first"
    result = chart_reader.get_value_from_yaml(yaml.safe_load(yaml_string), path)
    assert result == {
        "first": ""
    }

    yaml_string = """first:
  very:
    nested:
      indeed:
        omg:
          this:
            is:
              so:
                nested: true
    """
    path = "first"
    result = chart_reader.get_value_from_yaml(yaml.safe_load(yaml_string), path)
    assert result == {
        "first": {
            "very": {
                "nested": {
                    "indeed": {
                        "omg": {
                            "this": {
                                "is": {
                                    "so": {
                                        "nested": True
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }


def test_build_full_path():
    test_yaml = """---
first:
  element: "wow"
  another: "one"

emptydict: {}

emptyarray: []

yet:
  another: []

eins:
  zwei:
    drei: true
    vier:
      fuenf: "wow"
      lol: "rofl"
  sechs: "sieben"

banane:
  melone:
    cpu: 100Mi
    ram: 100Gi
  test:
    another:
      indent: false
    # -- stella
    # desc
    getme: true
"""
    result = chart_reader.build_full_path(i=3, value_name_dirty="  another", value_name_clean="another",
                                          values_lines=test_yaml.split("\n"))
    assert result == "first.another"

    result = chart_reader.build_full_path(i=2, value_name_dirty="  element", value_name_clean="element",
                                          values_lines=test_yaml.split("\n"))
    assert result == "first.element"

    result = chart_reader.build_full_path(i=5, value_name_dirty="emptydict", value_name_clean="emptydict",
                                          values_lines=test_yaml.split("\n"))
    assert result == "emptydict"

    result = chart_reader.build_full_path(i=5, value_name_dirty="emptyarray", value_name_clean="emptyarray",
                                          values_lines=test_yaml.split("\n"))
    assert result == "emptyarray"

    result = chart_reader.build_full_path(i=9, value_name_dirty="yet", value_name_clean="yet",
                                          values_lines=test_yaml.split("\n"))
    assert result == "yet"

    result = chart_reader.build_full_path(i=10, value_name_dirty="  another", value_name_clean="another",
                                          values_lines=test_yaml.split("\n"))
    assert result == "yet.another"

    result = chart_reader.build_full_path(i=14, value_name_dirty="    drei", value_name_clean="drei",
                                          values_lines=test_yaml.split("\n"))
    assert result == "eins.zwei.drei"

    result = chart_reader.build_full_path(i=16, value_name_dirty="      fuenf", value_name_clean="fuenf",
                                          values_lines=test_yaml.split("\n"))
    assert result == "eins.zwei.vier.fuenf"

    result = chart_reader.build_full_path(i=18, value_name_dirty="  sechs", value_name_clean="sechs",
                                          values_lines=test_yaml.split("\n"))
    assert result == "eins.sechs"

    result = chart_reader.build_full_path(i=29, value_name_dirty="    getme", value_name_clean="getme",
                                          values_lines=test_yaml.split("\n"))
    assert result == "banane.test.getme"


def test_generate_requirements():
    doc = {
        "name": "",
        "appVersion": "",
        "apiVersion": "",
        "version": "",
        "description": "",
        "type": "",
        "dependencies": [],
        "values": [],
        "templates": [],
        "objects": [],
        "commands": [],
    }

    result = chart_reader.generate_requirements(doc, "test/test-chart")
    assert_that(result["dependencies"], contains_inanyorder(
        {
            "name": "postgresql",
            "condition": "postgresql.enabled",
            "version": "1.2.3",
            "repository": "https://lol.de/repo/"
        },
        {
            "name": "mysql",
            "condition": "mysql.enabled",
            "version": "1.2.3",
            "repository": "https://lol.de/repo/"
        }
    ))


def test_generate_requirements_from_chart_yaml():
    doc = {
        "name": "",
        "appVersion": "",
        "apiVersion": "",
        "version": "",
        "description": "",
        "type": "",
        "dependencies": [],
        "values": [],
        "templates": [],
        "objects": [],
        "commands": [],
    }

    result = chart_reader.generate_requirements(doc, "test/test-chart-dependencies")
    assert_that(result["dependencies"], contains_inanyorder(
        {
            "name": "postgresql",
            "condition": "postgresql.enabled",
            "version": "1.2.3",
            "repository": "https://lol.de/repo/"
        },
        {
            "name": "mysql",
            "condition": "mysql.enabled",
            "version": "1.2.3",
            "repository": "https://lol.de/repo/"
        }
    ))


def test_generate_templates():
    doc = {
        "name": "",
        "appVersion": "",
        "apiVersion": "",
        "version": "",
        "description": "",
        "type": "",
        "dependencies": [],
        "values": [],
        "templates": [],
        "objects": [],
        "commands": [],
    }

    result = chart_reader.generate_templates(doc, "test/test-chart")
    assert_that(result["templates"], contains_inanyorder(
        {
            "path": "deployment.yaml"
        },
        {
            "path": "ingress.yaml"
        },
        {
            "path": "service.yaml"
        },
        {
            "path": "hpa.yaml"
        },
        {
            "path": "serviceaccount.yaml"
        }
    ))

def test_generate_objects():
    doc = {
        "name": "",
        "appVersion": "",
        "apiVersion": "",
        "version": "",
        "description": "",
        "type": "",
        "dependencies": [],
        "values": [],
        "templates": [
            {
                "path": "deployment.yaml"
            },
            {
                "path": "hpa.yaml"
            },
            {
                "path": "ingress.yaml"
            },
            {
                "path": "service.yaml"
            },
            {
                "path": "serviceaccount.yaml"
            }
        ],
        "objects": [],
        "commands": [],
    }

    result = chart_reader.generate_objects(doc, "test/test-chart")
    assert_that(result["objects"], contains_inanyorder(
            {
                "kind": "Deployment",
                "from Template": "deployment.yaml"
            },
            {
                "kind": "HorizontalPodAutoscaler",
                "from Template": "hpa.yaml"
            },
            {
                "kind": "Ingress",
                "from Template": "ingress.yaml"
            },
            {
                "kind": "Service",
                "from Template": "service.yaml"
            },
            {
                "kind": "ServiceAccount",
                "from Template": "serviceaccount.yaml"
            }
    ))


def test_generate_objects_multiple_objects_single_template():
    doc = {
        "name": "",
        "appVersion": "",
        "apiVersion": "",
        "version": "",
        "description": "",
        "type": "",
        "dependencies": [],
        "values": [],
        "templates": [
            {
                "path": "best.yaml"
            }
        ],
        "objects": [],
        "commands": [],
    }

    result = chart_reader.generate_objects(doc, "test/test-chart-objects")
    assert_that(result["objects"], contains_inanyorder(
            {
                "kind": "Deployment",
                "from Template": "best.yaml"
            },
            {
                "kind": "Secret",
                "from Template": "best.yaml"
            }
    ))
