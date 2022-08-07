# 💫 stella

Stella is a free tool to help automatically generate
[helm](https://helm.sh/) chart documentation.
It supports simple templating, so custom templates for output can be used as well.
Will read metadata such as `Chart.yaml`, `values.yaml` or the present templates and generate
a Markdown documentation from that data.

## Usage

### Installation
To run it natively on your machine using pipenv:
```shell
cd ~
git clone https://github.com/very-doge-wow/stella.git
cd stella
pipenv install
pipenv run python main.py --help
```

Alternatively install dependencies using pip and create an alias to your `/usr/local/bin`, for example:
```shell
cd ~
git clone https://github.com/very-doge-wow/stella.git
cd stella
pip install pyyaml pytest
python main.py --help
```

### General Usage

```shell
usage: main.py [-h] [-hcp HELM_CHART_PATH] [-o OUTPUT] [-t TEMPLATE] [-v]

Will create documentation for helm charts using metadata.

optional arguments:
  -h, --help            show this help message and exit
  -hcp HELM_CHART_PATH, --helm-chart-path HELM_CHART_PATH
                        Path to helm chart.
  -o OUTPUT, --output OUTPUT
                        Output file.
  -t TEMPLATE, --template TEMPLATE
                        Custom template file.
  -v, --verbose         Activate debug logging.
```

## Custom Templating
To specifiy a custom template, create a text/markdown file, then pass it to stella
using the config parameter.
You can use the following fields inside your template:

* `{{ stella.name }}`
* `{{ stella.version }}`
* `{{ stella.appVersion }}`
* `{{ stella.apiVersion }}`
* `{{ stella.type }}`
* `{{ stella.description }}`
* `{{ stella.dependencies }}`
* `{{ stella.templates }}`
* `{{ stella.objects }}`
* `{{ stella.values }`

## Why `stella`?
`stella` is named after [Tilemann Stella](https://de.wikipedia.org/wiki/Tilemann_Stella), a scholar from the Renaissance era.
He is most famously known for being a cartographer and for creating
multiple waterways, which is fitting when considering the tool should 
create helm chart docs.