# FinOps++ Framework Assessment

A FinOps Assessment perspective as a NIST CSF Community Profile

As organizations move their FinOps practices to shift-left, more of the FinOps optimization and maintenance tasks get pushed to the edge where the Engineers are. In this case, FinOps teams need to move their focus towards supporting the Inform and Operate phases of the FinOps lifecycle. Through building more formal FinOps Policies and Governance standards, FinOps teams can accelerate their iteration through the lifecycle phases to increase their practice maturity for the long run. Pulling inspiration from the Intersecting Discipline of Security, FinOps teams can solidify their position as a trusted partner to the business.

This assessment is an expansion of the existing FinOps Framework Assessment as of 7/3/25. By combining FinOps capabilities with controls found in the NIST Cybersecurity Framework, FinOps practitioners can provide a structured and proven foundation for strengthening governance for cost accountability. Additionally, treating financial risk with the same rigor as cybersecurity empowers FinOps teams to better define their policies, processes, and enforcement of best practices for the organization.

## Project Structure

This repository is broken down into encapsulated directories, where the function of a directory reflects a core design aspect or goal of the project.

### Components

At the very beginning of this project, there was a desire to establish way to define the building blocks that would go into creating a framework and its' assessment. We quickly decided that since the project was inspired by the [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework) (CSF), that we should also try to mirror the CSF by architecting the blocks into a logical grouping. But with a distinctly FinOps flavor.

The grouping that was selected is based on the fundamental units that we call *actions*, which map to the *sub-categories* found in the CSF. These `actions` are organized into *capabilities* from the FinOps framework, now made to correspond to *categories* from the CSF. And as the FinOps framework does, these are placed into *domains* that we correlate with *functions* from the CSF.

In this way, the heart of this project is located in the [components/](/components/) directory. The formalism that was selected is directly represented in the folder structure of this directory. Each subdirectory being a key piece (or component) of the FinOps++ scaffolding used to construct frameworks and their assessments.

The Markdown files found in these subdirectories are navigable, allowing you to traverse the logical grouping going from `Domain -> Capability -> Action` for the pre-defined `domains`, `capabilities`, and `actions` components.

To further fashion out building blocks into something useful, we place the `domains` into *profiles*, which closely parallel the function of the *profiles* from CSF. While the `profiles` are not directly considered a component themselves, they are integral to organizing this project into usable, extensible, and reproducible schemas. With their primary use-case being to define a framework.

### Assessments

The [assessments/](/assessments/) directory is where you can find subdirectories (based on the profile names) representing different frameworks supported by FinOps++. Each subdirectory containing both the markdown file detailing how a framework is put together, and the assessment worksheet used for scoring against that framework. The worksheet is current an excel doc that can be easily downloaded from this repository and potentially convert to other cell-based, excel-like products (such as google sheets).

These subdirectories will be the primary entry point for most people using the FinOps++ project as the assessment is the primary product for it. The framework markdown and worksheet link to the different components used to create it as needed. With the hope of making it easy to trace out how a framework is designed to work (i.e what concerns a framework is trying to address).

### Specifications

At the very beginning of this project, there was a desire to establish a way to define the components that went into an assessment in such a way that ensured that each component was verifiable correct and that the information used for that component was as reusable as possible. To meet this goal, we choose to use [YAML](https://yaml.org/) to create strict specification files for the components of a framework.

These specifications can be found in the [specifications/](/specifications/) directory, divided into subdirectories that exactly echo those in [components/](/components/). If fact, these specification files are directly used to generate complementary component files found in the different components subdirectories (as well as the assessments found in [assessments/](/assessments/)). More of the generating process can be read about below in [Generating commands](#generating-commands) below.

> [!NOTE]
> The serialization number for a file uses the schema `xxx.yaml` with enough `0`s before the ID to pad out the length of the file name to 3 digits.

For more on schemas used for the different specification types, please check-out [specifications/README.md](./specifications/README.md).

### Tools

Assisting in the ideas that motivated the creation of the specifications, such as ease of reproducibility and sub-divisibility, the [tools/](/tools/) directory was setup to house all the custom programmed scripts and tools used to maintain the specifications. The main "product" of this directory being the `finopspp` CLI tools. You can read more about this tool, different commands that it includes, and how to get started with it in [CLI Tool](/tools/README.md#cli-tool) and [Developing the FinOpsPP CLI Tool](/guidelines/development.md#developing-the-finopspp-cli-tool).

### Guidelines

This project is only as useful as it is understandable. So chief amongst our goals is ensuring that ideas are cleanly explained and that expectations and clearly set. The [guidelines/](/guidelines/) directory is our attempt at bringing this goal to life.

This folder includes direction and explications on a range of topics, with the goal of being more in-depth than this README. From how assessments are designed, to how changes are to be made for this repository. And if you can't make sure to open up an Issue requesting clarification.  
