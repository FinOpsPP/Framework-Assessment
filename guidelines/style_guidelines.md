# YAML

This project makes use of the the [YAML specification v1.2.2](https://yaml.org/spec/1.2.2/)

# Markdown

Largely, this project work around the [GitHub Flavored Markdown](https://github.github.com/gfm/), but should generally also work well with the [CommonMark](https://commonmark.org/) with some difference related to handling of HTML elements when creating nested tableds

# Python

Python modules hold to the [PEP 8](https://peps.python.org/pep-0008/) standard. 

# Linting/Validation recommendations

## Python Environment

It is strongly recommended to use [pylint](https://www.pylint.org/) for linting for pythong code. While [yamllint](https://yamllint.readthedocs.io/en/stable/) is recommended for the YAML components specifications. And [pymarkdown](https://pymarkdown.readthedocs.io/en/latest/) can be used to spot check the Markdown documentation.

There are built-in configuration files for these in the top-level directory of this project that will help make sure your code is compliant with the project's standards. These packages can be pretty easily installed in [CLI Tool](../README.md#cli-tool) with the following modification to the pip install command `python -m pip install -e ".[validation]"`
