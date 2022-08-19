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
        {'name': 'test-chart', 'appVersion': '1.16.0', 'apiVersion': 'v2', 'version': '0.1.0',
         'description': 'A Helm chart for Kubernetes', 'type': 'application', 'dependencies': [
            {'name': 'postgresql', 'condition': 'postgresql.enabled', 'version': '1.2.3',
             'repository': 'https://lol.de/repo/'},
            {'name': 'mysql', 'condition': 'mysql.enabled', 'version': '1.2.3', 'repository': 'https://lol.de/repo/'}],
         'values': [
             {'name': 'replicaCount', 'description': 'how many replicas to deploy\n', 'default': {'replicaCount': 1},
              'example': ''}, {'name': 'image', 'description': 'which image to deploy\n',
                               'default': {'image': {'repository': 'nginx', 'pullPolicy': 'IfNotPresent', 'tag': ''}},
                               'example': '\nimage:\n  repository: very-doge-wow/stella\n  pullPolicy: IfNotPresent\n  tag: "latest"\n'},
             {'name': 'imagePullSecrets', 'description': '', 'default': {'imagePullSecrets': []}, 'example': ''},
             {'name': 'nameOverride', 'description': '', 'default': {'nameOverride': ''}, 'example': ''},
             {'name': 'fullnameOverride', 'description': '', 'default': {'fullnameOverride': ''}, 'example': ''},
             {'name': 'serviceAccount', 'description': '',
              'default': {'serviceAccount': {'create': True, 'annotations': {}, 'name': ''}}, 'example': ''},
             {'name': 'podAnnotations', 'description': '', 'default': {'podAnnotations': {}}, 'example': ''},
             {'name': 'podSecurityContext', 'description': '', 'default': {'podSecurityContext': {}}, 'example': ''},
             {'name': 'securityContext', 'description': '', 'default': {'securityContext': {}}, 'example': ''},
             {'name': 'service', 'description': '', 'default': {'service': {'type': 'ClusterIP', 'port': 80}},
              'example': ''}, {'name': 'ingress', 'description': '', 'default': {
                 'ingress': {'enabled': False, 'className': '', 'annotations': {}, 'hosts': [
                     {'host': 'chart-example.local', 'paths': [{'path': '/', 'pathType': 'ImplementationSpecific'}]}],
                             'tls': []}}, 'example': ''},
             {'name': 'resources', 'description': '', 'default': {'resources': {}}, 'example': ''},
             {'name': 'autoscaling', 'description': '', 'default': {
                 'autoscaling': {'enabled': False, 'minReplicas': 1, 'maxReplicas': 100,
                                 'targetCPUUtilizationPercentage': 80}}, 'example': ''},
             {'name': 'nodeSelector', 'description': '', 'default': {'nodeSelector': {}}, 'example': ''},
             {'name': 'tolerations', 'description': '', 'default': {'tolerations': []}, 'example': ''},
             {'name': 'affinity', 'description': '', 'default': {'affinity': {}}, 'example': ''}],
         'templates': [{'path': 'deployment.yaml'}, {'path': 'hpa.yaml'}, {'path': 'ingress.yaml'},
                       {'path': 'service.yaml'}, {'path': 'serviceaccount.yaml'}],
         'objects': [{'kind': 'Deployment', 'from Template': 'deployment.yaml'},
                     {'kind': 'HorizontalPodAutoscaler', 'from Template': 'hpa.yaml'},
                     {'kind': 'Ingress', 'from Template': 'ingress.yaml'},
                     {'kind': 'Service', 'from Template': 'service.yaml'},
                     {'kind': 'ServiceAccount', 'from Template': 'serviceaccount.yaml'}],
         'commands': [{'description': '', 'command': ''}]}
    ))


def test_generate_chart_metadata_real_file():
    result = chart_reader.generate_chart_metadata({}, "test/test-chart")
    assert_that(result, has_entries(
        {
            'apiVersion': 'v2',
            'appVersion': '1.16.0',
            'description': 'A Helm chart for Kubernetes',
            'name': 'test-chart',
            'type': 'application',
            'version': '0.1.0'
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
            'apiVersion': 'unknown',
            'appVersion': 'unknown',
            'description': 'unknown',
            'name': 'unknown',
            'type': 'unknown',
            'version': 'unknown'
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
            'name': 'replicaCount',
            'description': 'how many replicas to deploy\n',
            'default': {'replicaCount': 1}, 'example': ''
        },
        {
            'name': 'image',
            'description': 'which image to deploy\n',
            'default': {'image': {'repository': 'nginx', 'pullPolicy': 'IfNotPresent', 'tag': ''}},
            'example': '\nimage:\n  repository: very-doge-wow/stella\n  pullPolicy: IfNotPresent\n  tag: "latest"\n'
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
            'name': 'replicaCount',
            'description': 'how many replicas to deploy\n',
            'default': {'replicaCount': 1}, 'example': ''
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
        {'name': 'customObjects', 'description': 'Test for using pipes in examples\n', 'default': {'customObjects': []}, 'example': '\ncustomObjects:\n  - \\|\n    best-string\n'}
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
        {'name': 'best', 'description': 'Test for comments in examples\n', 'default': {'best': []},
         'example': '\nbest:\n  # this is a comment inside an example\n  - value\n'}
    ))


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
