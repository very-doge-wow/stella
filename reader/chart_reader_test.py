import chart_reader
import yaml
from unittest.mock import Mock
import logging


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
    assert result is {'name': 'test-chart', 'appVersion': '1.16.0', 'apiVersion': 'v2', 'version': '0.1.0', 'description': 'A Helm chart for Kubernetes', 'type': 'application', 'dependencies': [{'name': 'postgresql', 'condition': 'postgresql.enabled', 'version': '1.2.3', 'repository': 'https://lol.de/repo/'}, {'name': 'mysql', 'condition': 'mysql.enabled', 'version': '1.2.3', 'repository': 'https://lol.de/repo/'}], 'values': [{'name': 'replicaCount', 'description': 'how many replicas to deploy\n', 'default': 1, 'example': ''}, {'name': 'image', 'description': 'which image to deploy\n', 'default': {'repository': 'nginx', 'pullPolicy': 'IfNotPresent', 'tag': ''}, 'example': '\nimage:\n  repository: very-doge-wow/stella\n  pullPolicy: IfNotPresent\n  tag: "latest"\n'}, {'name': 'imagePullSecrets', 'description': '', 'default': [], 'example': ''}, {'name': 'nameOverride', 'description': '', 'default': '', 'example': ''}, {'name': 'fullnameOverride', 'description': '', 'default': '', 'example': ''}, {'name': 'serviceAccount', 'description': '', 'default': {'create': True, 'annotations': {}, 'name': ''}, 'example': ''}, {'name': 'podAnnotations', 'description': '', 'default': {}, 'example': ''}, {'name': 'podSecurityContext', 'description': '', 'default': {}, 'example': ''}, {'name': 'securityContext', 'description': '', 'default': {}, 'example': ''}, {'name': 'service', 'description': '', 'default': {'type': 'ClusterIP', 'port': 80}, 'example': ''}, {'name': 'ingress', 'description': '', 'default': {'enabled': False, 'className': '', 'annotations': {}, 'hosts': [{'host': 'chart-example.local', 'paths': [{'path': '/', 'pathType': 'ImplementationSpecific'}]}], 'tls': []}, 'example': ''}, {'name': 'resources', 'description': '', 'default': {}, 'example': ''}, {'name': 'autoscaling', 'description': '', 'default': {'enabled': False, 'minReplicas': 1, 'maxReplicas': 100, 'targetCPUUtilizationPercentage': 80}, 'example': ''}, {'name': 'nodeSelector', 'description': '', 'default': {}, 'example': ''}, {'name': 'tolerations', 'description': '', 'default': [], 'example': ''}, {'name': 'affinity', 'description': '', 'default': {}, 'example': ''}], 'templates': [{'path': 'deployment.yaml'}, {'path': 'ingress.yaml'}, {'path': 'service.yaml'}, {'path': 'hpa.yaml'}, {'path': 'serviceaccount.yaml'}], 'objects': [{'kind': 'Deployment', 'from Template': 'deployment.yaml'}, {'kind': 'Ingress', 'from Template': 'ingress.yaml'}, {'kind': 'Service', 'from Template': 'service.yaml'}, {'kind': 'HorizontalPodAutoscaler', 'from Template': 'hpa.yaml'}, {'kind': 'ServiceAccount', 'from Template': 'serviceaccount.yaml'}], 'commands': [{'description': '', 'command': ''}]}


def test_generate_chart_metadata_real_file():
    result = chart_reader.generate_chart_metadata({}, "test/test-chart")
    assert result is {
        'apiVersion': 'v2',
        'appVersion': '1.16.0',
        'description': 'A Helm chart for Kubernetes',
        'name': 'test-chart',
        'type': 'application',
        'version': '0.1.0'
    }


def test_generate_chart_metadata_unknown():
    mocked_content = {}
    real_yaml_load = chart_reader.yaml.safe_load
    chart_reader.yaml.safe_load = Mock(return_value=mocked_content)
    result = chart_reader.generate_chart_metadata({}, "test/test-chart")
    chart_reader.yaml.safe_load = real_yaml_load
    assert result is {
        'apiVersion': 'unknown',
        'appVersion': 'unknown',
        'description': 'unknown',
        'name': 'unknown',
        'type': 'unknown',
        'version': 'unknown'
    }

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
    assert result["values"] is [
        {
            'name': 'replicaCount',
            'description': 'how many replicas to deploy\n',
            'default': 1, 'example': ''
        },
        {
            'name': 'image',
            'description': 'which image to deploy\n',
            'default': {'repository': 'nginx', 'pullPolicy': 'IfNotPresent', 'tag': ''},
            'example': '\nimage:\n  repository: very-doge-wow/stella\n  pullPolicy: IfNotPresent\n  tag: "latest"\n'
        }
    ]


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
    assert result["values"] is [
        {
            'name': 'replicaCount',
            'description': 'how many replicas to deploy\n',
            'default': 1, 'example': ''
        }
    ]


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
    assert result["dependencies"] is [
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
    ]


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
    assert result["templates"] is [
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
        ]


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
    assert result["objects"] is [
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
    ]
