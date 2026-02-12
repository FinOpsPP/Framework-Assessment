# Contributing to the FinOps++ Framework Assessment

To start off, we wanted to say welcome! We are more than happy that you took the time to come over to this CONTRIBUTING.md document to see how you can start adding to the FinOps++ Framework-Assessment project. We accept contributions from all, but we do have specific ways of doing things that we ask you to follow. We will try and outline those procedures below to the best of our abilities. But if you have any additional questions on things, please feel free to reach out to maintainers via Email, or in an [Issue](#have-a-suggestion-found-an-issue) in for this repository.

## Have a suggestion? Found an Issue?

* For bugs that are found, please open an issue based on Bug Report template
* For new feature requests, please open an issue based on the Enhancement template

For bugs, an attempt will be made to reproduce the bug. The only expectation we have for you in this process is to be open to try out some things (such as additional commands) to help us gather more information to diagnose the problem.

Your GitHub issue (regardless of type) will be reviewed, and discussed as a community with the issue author. Confirmed/accepted issues will be added to the next feasible release milestone. At this point, cheers! You are official already a contributor to the Framework-Assessment project. If you desire though, feel free now to consider [Submitting a specification change](#submitting-specification-changes) or [Submitting a tools change](#submitting-tools-changes)

## Pull/Change Request

Change for the Framework-Assessment project largely into two categories Specifications changes and Tools changes. While a contribution to the project can be make up from both types of changes, we do find this breakdown useful for providing guidance on *how* to contribute. Before getting started on a change, first make sure that an issue exists in the current milestone for your desired change. To help the maintainers with organization, we will unfortunately not merge a proposed contribution that does not resolve a milestone issue.

Once all your changes are ready, you can submit a PR request using the provided PR template in the repository. We don't require your PRs to be a single commit, but do please try to keep the commits down to a minimum need to complete an issue. Your PR will be reviewed, discussed, and if approved merged in. Again cheers! You are now a contributor.

> [!NOTE]
> For those new tO GitHub, please follow [Getting up & running with GitHub](/guidelines/development.md#getting-up--running-with-github).

### Submitting specification changes

The Framework-Assessment project uses an [As-Code](https://arxiv.org/pdf/2507.05100), with the Components and Frameworks markdown files, as well as the Assessments excel being generated from yaml [specifications](/specifications). For you, this mean that most of the changes you might want to make to the Components, Frameworks, or Assessments should start with changes to those specifications. Things that would necessitate a yaml specification change could include

* "Patching" a typo found in the markdown or excel files.
* Adding a new Note or Reference for an existing Action.
* Creating a completely new instance of a Component, such as an Action, Capability, or Domain
* Adding a new scope definition to an existing Profile.
* Creating a completely new a community Framework Profile.
* Removing any complete Component or Framework Profile

Once you have updated your specification(s), this is the minimum we require for a change to be submitted for consideration. But, if your want or would like to go one step further, you can consider using the commands from the [finopspp cli](README.md#cli-tool) to [generate](README.md#generating-commands) updates to the Components and Frameworks. If not, that is fine too. At some point soon after merging, these command will be run by the maintainers before the next release to make sure your changes are represented in the next milestone release.

### Submitting tools changes

> [!IMPORTANT]
> Make sure to follow the [Developing the finopspp CLI tool](/guidelines/development.md#developing-the-finopspp-cli-tool)
> [!CRITICAL]
> Please make sure your tools changes are tested locally before submitting a PR

There are some times, when you might also want to suggest an update to the whole structure of the Components. We allow these, but to achieve them, you will need to update the structure of these files by updating their [jinja2 templates](https://jinja.palletsprojects.com/en/stable/) that can be found under [tools/templates](/tools/templates/). Once the structure updates are completed, we will require you to run the [generate](README.md#generating-commands) commands to test locally that the structural changes have been represented in any relevant files.
