# Development & Installation Guides

The Framework-Assessment project has many moving parts, lots of auto-generated content, and a plethora of articulation points for customizations. With all of that, we know it can be daunting on how to actually develop this project. The goal of this guide is to provide just-enough information to get people going on developing to the standards required of the project.

It is written from the prospective that a potential contributor has zero (or next to zero) experience with one or more of the core software elements used to build the project. It links out to several sources that are more authoritative for those that desire to read more on the subject. Hopefully, with that point of view in mind, this document will be useful for people with all levels of skills in the development space to contribute to this project

## Getting up & running with GitHub

For GitHub newbies, the first step you will probably need to start with is [installing git](https://git-scm.com/install/) itself. Git is a source control command line tool from the Linus Torvalds (the creator of Linux), and forms the base of GitHub's features. It will allow you to clone the Framework-Assessment repository to your local machine and make changes that can be eventually merged back into the project.

Once you have git installed for your Operating system, you will be ready to get started with GitHub. For this project, we make use of what is called the [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow) for making changes/updates. To follow this flow, you will need to [make a GitHub account](https://docs.github.com/en/get-started/start-your-journey/creating-an-account-on-github).

GitHub Flow largely revolves around [creating feature branches](https://docs.github.com/en/get-started/using-github/github-flow#create-a-branch) to "house" your proposed change. When you feel your proposed changes are ready, you will then open what is called a [Pull Request](https://docs.github.com/en/get-started/using-github/github-flow#create-a-pull-request) that will be reviewed by the project maintainers (the FinOps++ Authors). The maintainers will [provide feedback as needed](https://docs.github.com/en/get-started/using-github/github-flow#address-review-comments), which could require making additional changes to your feature branch. Once feedback has been addressed and your proposed change has been approved by the maintainers, it will be [merged into the default branch](https://docs.github.com/en/get-started/using-github/github-flow#merge-your-pull-request) of the project. At which point you can [delete you feature branch](https://docs.github.com/en/get-started/using-github/github-flow#delete-your-branch) and then celebrate yourself becoming an published contributor to the Framework-Assessment project of FinOps++! :partying_face:

## Developing the finopspp CLI tool

The `finopspp` [CLI tool](/tools/README.md) is a Python based tool that works for `Python >= 3.13`, it is recommended that you start off by creating a virtual environment (venv) as is discussed in <https://docs.python.org/3/library/venv.html>.

Once your venv is setup, [activate it](https://docs.python.org/3/library/venv.html#how-venvs-work) and run `python -m pip install -e .` from the same directory as this README. This command will pull in all required dependencies into the venv and then installs the script for you to use in your venv. It will also do this in what is called "[editable](https://pip.pypa.io/en/stable/cli/pip_install/#cmdoption-e)" mode. Which will allow you to change packages and files (including yaml specifications) used by `finopspp`, and to directly see those changes reflected in the invocation of the tool. Be careful when doing this, so as not to break the core functionality needed to generate the assessment.

If you use VSCode, or would like to, you can follow the tutorial from <https://code.visualstudio.com/docs/python/python-tutorial> to get started with setting up this python project environment.

> [!IMPORTANT]
> The parts related to installing python and activating an existing venv should also work with pretty much any other IDE or text editor. So you are under no obligation to us VSCode if you have another coding tool like Vim, Emacs, PyCharm, Cursor, etc.

It is also recommended to read through <https://realpython.com/python-pyproject-toml/> to get an overview of `pyproject.toml` based python projects. And to get a feel for the setup of this project in [pyproject.toml](/pyproject.toml) used for `finopspp`.

### Jinja2 Templates

The markdown files [generated](/README.md#generating-commands) by the `finopspp` tool structured off of specialized [Jinja2 templates](https://jinja.palletsprojects.com/en/stable/) that can be found under [tools/templates](/tools/templates/). It is suggested that whatever text editor you use for development include support for the `.j2` extension and jinja template syntax in general.

### Composers

There are several composers used to aid in creating the different content provided by the Framework-Assessment project. It is quite possible, it could be argued, that of those, the most import is the one used to create the excel files used for the assessments. These live under [tools/composers/excel](/tools/composers/excel.py) and make use of the python version of `xlsxwriter`.

To fully develop for this, you will need to either have a properly licensed [Microsoft Excel](https://en.wikipedia.org/wiki/Microsoft_Excel) installed, or be on a Linux or Unix-like system that packages the free & opened sourced [LibreOffice Calc](https://en.wikipedia.org/wiki/LibreOffice_Calc). In this latter situation, you specifically will need to make sure that the `libreoffice` and `make` commands are installed. If they are, you can use the provided [Makefile target](/Makefile) `make ods` to convert existing excel files in the project to a natively supported LibreOffice format.

> [!NOTE]
> You can directly open a `.xlsx` file in LibreOffice Calc, but some elements might be broken. It is strongly encouraged that you covert before using.

## Versioning

There are a few different versioning systems used for the Framework-Assessment project. And we know that that can lead to a little bit of confusion when trying to talk about exactly what "version" of the assessment you are using. So in this next section we hope to illuminate some of those version systems used to make it easier to understand your assessment.

### Semantic Versioning

Used for the Project, Component, and Specification versions. Also know as [SemVer](https://semver.org/), is a nice way to include what a version a version might fix or potentially break. Browing from the semver web page, it is

```{text}
Given a version number MAJOR.MINOR.PATCH, increment the:

1. MAJOR version when you make incompatible API changes
2. MINOR version when you add functionality in a backward compatible manner
3. PATCH version when you make backward compatible bug fixes
```

Components & Specifications follow this pretty rigorously. With Patch version changes usually updated when fixing typos or grammer without really changing the semantics of the thing being changes. Minor versions updates can include things such as adding new fields, `Supplement Guidance`, `References`, or updating a `Formula` in such as way that `Scoring` is unchanged. While Major version would be incremented when removing or changing the names of fields, changing a `Score Type` to a different one, or updating a `Formula` in such a way that the `Scoring` is changed.

The semantic version of the Project is a little more ad-hoc than those used by the Components or Specifications. The "Patch" version of the project is less about bug fixes (though still can be at time), and more about closing out some duration of work during a milestone. So for example, say a milestone is designed to take 3 months to finish, and the maintainers have broken that milestone down into 6 two week "sprints". When a sprint finishes, we update the Patch version of the Project. In a similar manner, when the milestone finishes, we will usually update the Minor version. Though if the milestone included a lot of potentially breaking changes, we will opt instead to increment the Major version.

### Date Versioning

Used for the assessment version. We figured using the date as a timestamp-like version of a given framework (i.e Profile) and its' assessment made a lot of sense. Especially when an individual doing the assessment might want an easy way to show others when their assessment framework as created, so that others in their organizations can base their potential assessment on close date. Additional, this has the added benifit of allowing an individual to know just how old their current assessment version is, by just looking at the date. Something that is much more difficult when using something like SemVer above.

Compressed versions of older assessments can be found for a framework by its' date version in the `history` subfolder under that Profile's assessment folder.
