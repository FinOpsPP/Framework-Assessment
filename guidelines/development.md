# Development & Installation Guides

## Getting up & running

Installing git

## Developing the finopspp CLI tool

The CLI tools is a Python based tool that works for `Python >= 3.13`, it is recommended that you start off by creating a virtual environment (venv) as is discussed in <https://docs.python.org/3/library/venv.html>.

Once your venv is setup, [activate it](https://docs.python.org/3/library/venv.html#how-venvs-work) and run `python -m pip install -e .` from the same directory as this README. This command will pull in all required dependencies into the venv and then installs the script for you to use in your venv. It will also do this in what is called "[editable](https://pip.pypa.io/en/stable/cli/pip_install/#cmdoption-e)" mode. Which will allow you to change packages and files (including yaml specifications) used by `finopspp`, and to directly see those changes reflected in the invocation of the tool. Be careful when doing this, so as not to break the core functionality needed to generate the assessment.

If you use VSCode, or would like to, you can follow the tutorial from <https://code.visualstudio.com/docs/python/python-tutorial> to get started with setting up this python project environment.

> [!IMPORTANT]
> The parts related to installing python and activating an existing venv should also work with pretty much any other IDE or text editor. So you are under no obligation to us VSCode if you have another coding tool like Vim, Emacs, PyCharm, Cursor, etc.

It is also recommended to read through <https://realpython.com/python-pyproject-toml/> to get an overview of `pyproject.toml` based python projects. And to get a feel for the setup of this project in [pyproject.toml](/pyproject.toml) used for `finopspp`.
