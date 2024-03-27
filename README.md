# 💫 stella

![stella](https://github.com/very-doge-wow/stella/blob/main/stella.png?raw=true)

[![release](https://img.shields.io/github/v/release/very-doge-wow/stella)](https://github.com/very-doge-wow/stella/releases)
[![release date](https://img.shields.io/github/release-date/very-doge-wow/stella?style=flat)](https://github.com/very-doge-wow/stella/releases)
[![unittests](https://github.com/very-doge-wow/stella/actions/workflows/unittest.yml/badge.svg)](https://github.com/very-doge-wow/stella/actions/workflows/unittest.yml)
[![code coverage](https://img.shields.io/codecov/c/github/very-doge-wow/stella/main)](https://app.codecov.io/github/very-doge-wow/stella)
[![markdownlint](https://github.com/very-doge-wow/stella/actions/workflows/lintmarkdown.yml/badge.svg)](https://github.com/very-doge-wow/stella/actions/workflows/lintmarkdown.yml)
[![license](https://img.shields.io/github/license/very-doge-wow/stella)](https://github.com/very-doge-wow/stella?tab=MIT-1-ov-file#readme)
[![docker pulls](https://img.shields.io/docker/pulls/suchdogewow/stella.svg)](https://hub.docker.com/r/suchdogewow/stella)


`stella` is a free tool to help automatically generate
[helm](https://helm.sh/) chart documentation.
It supports simple templating, so custom templates for output can be used as
well. Will read metadata such as `Chart.yaml`, `values.yaml` or the present
templates and generate a Markdown or HTML documentation from that data.

## Example

For an example output when running `stella` for the
[prometheus](https://github.com/prometheus-community/helm-charts/tree/main/charts/prometheus)
helm chart, follow
[this](https://github.com/very-doge-wow/stella/blob/main/EXAMPLE/prometheus.md)
link.

## Usage

### Docker Image

<!-- markdownlint-disable MD013 -->
|    | Note                                                                                                                                                                                                           |
|----|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 🐳 | `stella` has switched from [Docker Hub](https://hub.docker.com/r/suchdogewow/stella) to [ghcr.io](https://github.com/very-doge-wow/stella/pkgs/container/stella). Please update all references to the new URI. |

Using the [Docker image](https://github.com/very-doge-wow/stella/pkgs/container/stella):

<!-- markdownlint-disable MD013 -->
```shell
docker pull ghcr.io/very-doge-wow/stella:latest
docker run -v ${full_path_to_host_chart_dir}:/tmp/chart ghcr.io/very-doge-wow/stella:latest -hcp /tmp/chart -o /tmp/chart/output.md [OPTIONS]
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
documentation will leave this field blank. For example:

```yaml
# -- stella
# Define whether to enable the pod security policy.
# -- example
# podSecurityPolicy:
#   enabled: true
podSecurityPolicy:
  enabled: false
```

Will yield the output:

<!-- markdownlint-disable MD033 -->
<!-- markdownlint-disable MD013 -->
| Name | Description | Default | Example |
|---|---|---|---|
| podSecurityPolicy | Define whether to enable the pod security policy. | <pre>podSecurityPolicy:<br>  enabled: false<br></pre> | <pre>podSecurityPolicy:<br>  enabled: true<br></pre> |
<!-- markdownlint-enable MD013 -->

You may also document **nested keys**. For example:

```yaml
configmapReload:
  # -- stella
  # URL for configmap-reload to use for reloads
  reloadUrl: ""
```

Will yield the output:

<!-- markdownlint-disable MD013 -->
| Name | Description | Default | Example |
|---|---|---|---|
| configmapReload.reloadUrl | URL for configmap-reload to use for reloads | <pre>configmapReload:<br>  reloadUrl: ''<br></pre> |  |
<!-- markdownlint-enable MD013 -->
<!-- markdownlint-enable MD033 -->

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
