# Assessment Design Guide

FinOps++ is an open assessment framework that measures how consistently a FinOps practice performs the specific actions that turn technology spend into business value. We break each FinOps Foundation capability into discrete actions and score each against an explicit formula, so practitioners spend less time debating what a score means and more time closing the gaps it reveals. The actions are organized the way the NIST Cybersecurity Framework organizes security controls, so that cost governance can be assessed and reported with the rigor an organization already applies to security.

## Components

Our framework takes the current FinOps Foundation framework and breaks each capability into specific actions representing behaviors done to accomplish proficiency. These actions can be done at different levels of maturity. Each action is made up of a scoring formula, a score breakdown, supplemental guidance, and references to assist in the scoring process.

## Framework

The FinOps++ framework assesses a practice action by action, and an assessment can cover a whole practice or a single scope. Weights can be adjusted before aggregation, so a practice can tune the assessment to what the business actually cares about. Raw action scores stay comparable even when weights differ, which is what makes it possible to compare across teams, across scopes, and over time.

The deliverable is an assessment worksheet, published per profile under `assessments/`, that a practice scores itself against.

## Accessibility

FinOps++ Strives to be as open as possible we take the opinion that we should be largely vendor agnostic. Generally, we will gravitate towards projects, specifications, and tools that are open to make the assessment. Though this is not always possible given market shares, it is a "North Star" for us. And where we have to use one vendor over another (such as using Excel as the default assessment format), we will do our best to ensure that the assessment is easily modifable to meet the needs of others.

### Linux User

For those of y'all that are using Linux, and specifically those using something like LibreOffice Calc, we also offer a `make` [target](https://makefiletutorial.com/#targets) called `ods` that will allow you to covert all the Excel documents in the project into LibreOffice Calc `.ods` files. For other Office-type suites, feel free to contribute back new coverts as needed be.
