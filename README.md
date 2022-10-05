# 💫 stella

![stella](https://github.com/very-doge-wow/stella/blob/main/stella.png?raw=true)

[![Lint Markdown](https://github.com/very-doge-wow/stella/actions/workflows/lintmarkdown.yml/badge.svg)](https://github.com/very-doge-wow/stella/actions/workflows/lintmarkdown.yml)
[![Unittests](https://github.com/very-doge-wow/stella/actions/workflows/unittest.yml/badge.svg)](https://github.com/very-doge-wow/stella/actions/workflows/unittest.yml)
[![Docker Pulls](https://img.shields.io/docker/pulls/suchdogewow/stella.svg)](https://hub.docker.com/r/suchdogewow/stella)

`stella` is a free tool to help automatically generate
[helm](https://helm.sh/) chart documentation.
It supports simple templating, so custom templates for output can be used as
well. Will read metadata such as `Chart.yaml`, `values.yaml` or the present
templates and generate a Markdown or HTML documentation from that data.

## Example

For an example output when running `stella` for the
[kibana](https://github.com/elastic/helm-charts/tree/main/kibana) helm chart,
follow [this](https://github.com/very-doge-wow/stella/blob/main/EXAMPLE_OUTPUT.md)
link.

## Usage

### Docker Image

Using the [OCI image](https://hub.docker.com/r/suchdogewow/stella):

<!-- markdownlint-disable MD013 -->
```shell
docker pull suchdogewow/stella:latest
docker run -v ${full_path_to_host_chart_dir}:/tmp/chart suchdogewow/stella -hcp /tmp/chart -o /tmp/chart/output.md [OPTIONS]
```
<!-- markdownlint-enable MD013 -->

### Installation

To run it natively on your machine using pipenv:

```shell
git clone https://github.com/very-doge-wow/stella.git
cd stella
pipenv install
pipenv run python stella.py --help
```

Alternatively install dependencies using pip:

```shell
git clone https://github.com/very-doge-wow/stella.git
cd stella
pip install pyyaml markdown
python stella.py --help
```

### General Usage

<!-- markdownlint-disable MD013 -->
```text
usage: stella.py [-h] [-hcp HELM_CHART_PATH] [-o OUTPUT] [-t TEMPLATE] [-fh] [-css CSS] [-v]

Will create documentation for helm charts using metadata.

optional arguments:
  -h, --help            show this help message and exit
  -hcp HELM_CHART_PATH, --helm-chart-path HELM_CHART_PATH
                        Path to helm chart (default `.`).
  -o OUTPUT, --output OUTPUT
                        Output file (default `output.md`).
  -t TEMPLATE, --template TEMPLATE
                        Custom template file.
  -fh, --format-html    Output using html instead of md.
  -css CSS, --css CSS   Path to optional css file to use for html generation (use in conjunction with -fh).
  -v, --verbose         Activate debug logging.
```
<!-- markdownlint-enable MD013 -->

## Adding `stella` Docstrings to your Chart

Metadata is read from the present files of your chart.
Additionally, you should also document the options given
in your `values.yaml`. This can be done as follows:

```yaml
# -- stella
# Define how many replicas should be deployed.
# -- example
# replicaCount: 2
replicaCount: 1
```

You can use multiline descriptions as well as multiline
examples. In that case, the formatting of the example
is preserved **as is**, meaning you can simply copy
a working example and then prepend the comment delimiter (`#`).

The line starting with `# -- stella` tells `stella` that the following
comment is a `stella` docstring. Use the `# -- example` delimiter to
specify an optional example. If you leave this empty, the resulting
documentation will leave this field blank.

## Custom Templating

To specify a custom template, create a text/markdown file, then pass it to
stella using the config parameter.
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
* `{{ stella.values }}`

## Contributing to `stella`

You want to contribute? Awesome!
Feel free to propose changes, report bugs or request features and
improvements. But first, please read the
[contribution guidelines](https://github.com/very-doge-wow/stella/blob/main/CONTRIBUTING.md).

## Why `stella`?

`stella` is named after
[Tilemann Stella](https://de.wikipedia.org/wiki/Tilemann_Stella),
a scholar from the Renaissance era.
He is most famously known for being a cartographer and for creating
multiple waterways, which is fitting when considering the tool should
create helm chart docs.
