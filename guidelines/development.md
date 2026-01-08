# Development & Installation Guides

The Framework-Assessment project has many moving parts, lots of auto-generated content, and a plethora of articulation points for customizations. With all of that, we know it can be daunting on how to actually develop this project. The goal of this guide is to provide just-enough information to get people going on developing to the standards required of the project.

It is written from the prospective that a potential contributor has zero (or next to zero) experience with one or more of the core software elements used to build the project. It links out to several sources that are more authoritative for those that desire to read more on the subject. Hopefully, with that point of view in mind, this document will be useful for people with all levels of skills in the development space to contribute to this project

## Getting up & running with GitHub

For GitHub newbies, the first step you will probably need to start with is [installing git](https://git-scm.com/install/) itself. Git is a source control command line tool from the Linus Torvalds (the creator of Linux), and forms the base of GitHub's features. It will allow you to clone the Framework-Assessment repository to your local machine and make changes that can be eventually merged back into the project.

Once you have git installed for your Operating system, you will be ready to get started with GitHub. For this project, we make use of what is called the [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow) for making changes/updates. To follow this flow, you will need to [make a GitHub account](https://docs.github.com/en/get-started/start-your-journey/creating-an-account-on-github).

GitHub Flow largely revolves around [creating feature branches](https://docs.github.com/en/get-started/using-github/github-flow#create-a-branch) to "house" your proposed change. When you feel your proposed changes are ready, you will then open what is called a [Pull Request](https://docs.github.com/en/get-started/using-github/github-flow#create-a-pull-request) that will be reviewed by the project maintainers (the FinOps++ Authors). The maintainers will [provide feedback as needed](https://docs.github.com/en/get-started/using-github/github-flow#address-review-comments), which could require making additional changes to your feature branch. Once feedback has been addressed and your proposed change has been approved by the maintainers, it will be [merged into the default branch](https://docs.github.com/en/get-started/using-github/github-flow#merge-your-pull-request) of the project. At which point you can [delete you feature branch](https://docs.github.com/en/get-started/using-github/github-flow#delete-your-branch) and then celebrate yourself becoming an published contributor to the Framework-Assessment project of FinOps++! :partying_face:

## Developing the finopspp CLI tool

The CLI tools is a Python based tool that works for `Python >= 3.13`, it is recommended that you start off by creating a virtual environment (venv) as is discussed in <https://docs.python.org/3/library/venv.html>.

Once your venv is setup, [activate it](https://docs.python.org/3/library/venv.html#how-venvs-work) and run `python -m pip install -e .` from the same directory as this README. This command will pull in all required dependencies into the venv and then installs the script for you to use in your venv. It will also do this in what is called "[editable](https://pip.pypa.io/en/stable/cli/pip_install/#cmdoption-e)" mode. Which will allow you to change packages and files (including yaml specifications) used by `finopspp`, and to directly see those changes reflected in the invocation of the tool. Be careful when doing this, so as not to break the core functionality needed to generate the assessment.

If you use VSCode, or would like to, you can follow the tutorial from <https://code.visualstudio.com/docs/python/python-tutorial> to get started with setting up this python project environment.

> [!IMPORTANT]
> The parts related to installing python and activating an existing venv should also work with pretty much any other IDE or text editor. So you are under no obligation to us VSCode if you have another coding tool like Vim, Emacs, PyCharm, Cursor, etc.

It is also recommended to read through <https://realpython.com/python-pyproject-toml/> to get an overview of `pyproject.toml` based python projects. And to get a feel for the setup of this project in [pyproject.toml](/pyproject.toml) used for `finopspp`.
