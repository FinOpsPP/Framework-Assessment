# FinOps++ Style Guide

Style can mean a lot. It may provide a sense of structure, can act as a mark of quality, enable understanding for new user, or even aid in recognition of a project. In may ways, style is the beating heart of the FinOps++ streaming from the desire to produce exactly these outcomes.

To help with this, when designing the structure of the Assessments project, we looked closely at how to provide a style scaffolding via time-tested specifications and popular linters.

## Linting

It is strongly recommended to use [pylint](https://www.pylint.org/) for linting for python code. While [yamllint](https://yamllint.readthedocs.io/en/stable/) is recommended for the YAML components specifications. And [pymarkdownlnt](https://pymarkdown.readthedocs.io/en/latest/) (also called `pymarkdown` for short) can be used to spot check the Markdown documentation.

There are built-in configuration files for these in the top-level directory of this project that will help make sure your code is compliant with the project's standards. These packages can be pretty easily installed in [CLI Tool](../README.md#cli-tool) with the following modification to the pip install command `python -m pip install -e ".[validation]"`.

> **NOTE**: There is an older and unaffiliated package called `pymarkdown`. Make sure to not download this version by installing specifically `pymarkdownlnt` if you choose to install the dependencies separately into your environment.

## YAML

This project makes use of the [YAML specification v1.2.2](https://yaml.org/spec/1.2.2/) for all files with the `.yaml` extension. That largely includes the `action`, `capability`, `domain`, and `profile` component specifications that are used generate other core pieces of FinOps++ such as the Markdown components.

Differences from the standard specification used for FinOps++ can be found in the `yamllint` configuration file [.yamllint](../.yamllint). The biggest change being that FinOps++ makes uses of 2 spaces for indentation rather than 4. This was chosen on purpose to help readability when it comes to nesting used by the component specifications.

## Markdown

Largely, this project work around the [GitHub Flavored Markdown](https://github.github.com/gfm/), but should generally also work well with the [CommonMark](https://commonmark.org/). Files that are governed by these specifications largely have the `.md` extension, there there are some exceptions such as the files found under [guidelines/](../guidelines/) or the project's base [README.md](../README.md).

Even when these specifications are enforce, there are some difference related to handling of HTML elements when creating nested tables for the framework markdowns. Additionally, we also along line-lengths of 120 characters rather than the typical length of 80. But generally we try to keep as close as possible to these specifications. These (hopefully) minimal changes can be found in the `pymarkdownlnt` configuration file [.pymarkdown](../.pymarkdown).

## Python

All python modules and code with the `.py` extension generally hold to the [PEP 8](https://peps.python.org/pep-0008/) standard. Deviations generally are around things like line-length, where much like the Markdown change, we allow 120 character lines. We also use PascalCase for local variables rather than the standard UPPER_CASE format.

The full list of changes (honestly, the full list of configuration even including basic defaults) can be found in [.pylintrc](../.pylintrc). This might be a bit hard to read,and if you are really interested in seeing the differences, would suggest running `pylint --generate-rcfile > .pylintrc2` in another directory and compare the differences using a tool like `diff` in *nix like environments or something like `Compare-Object` in PowerShell.
