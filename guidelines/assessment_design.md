# Assessment Design Guide

FinOps++ is an open assessment framework that measures how consistently a FinOps practice performs the specific actions that turn technology spend into business value. We break each FinOps Foundation capability into discrete actions and score each against an explicit formula, so practitioners spend less time debating what a score means and more time closing the gaps it reveals. The actions are organized the way the NIST Cybersecurity Framework organizes security controls, so that cost governance can be assessed and reported with the rigor an organization already applies to security.

## Components

Domains and capabilities come from the FinOps Framework, where domains are the outcomes of a practice and capabilities describe how to achieve them. FinOps++ adds one layer beneath them: we break each capability into specific actions, the things a FinOps practice does or ensures get done. We score actions rather than capabilities because an action is specific enough to answer yes or no. You can say whether a practice records anomaly timelines; you can't say whether it "does anomaly management."

That extra layer is our secret sauce, and the idea came from NIST CSF. The Framework's domains already line up with CSF functions and its capabilities with CSF categories. Actions supply the level that was missing: CSF sub-categories. Our profiles correspond to CSF profiles.

Each action is made up of a scoring formula, a score breakdown, supplemental guidance, and references to assist in the scoring process.

## Framework

The FinOps++ framework assesses a practice action by action, and an assessment can cover a whole practice or a single scope. Weights can be adjusted before aggregation, so a practice can tune the assessment to what the business actually cares about. Raw action scores stay comparable even when weights differ, which is what makes it possible to compare across teams, across scopes, and over time.

The deliverable is an assessment worksheet, published per profile under `assessments/`, that a practice scores itself against.

## Accessibility

FinOps++ Strives to be as open as possible we take the opinion that we should be largely vendor agnostic. Generally, we will gravitate towards projects, specifications, and tools that are open to make the assessment. Though this is not always possible given market shares, it is a "North Star" for us. And where we have to use one vendor over another (such as using Excel as the default assessment format), we will do our best to ensure that the assessment is easily modifable to meet the needs of others.

### Linux User

For those of y'all that are using Linux, and specifically those using something like LibreOffice Calc, we also offer a `make` [target](https://makefiletutorial.com/#targets) called `ods` that will allow you to covert all the Excel documents in the project into LibreOffice Calc `.ods` files. For other Office-type suites, feel free to contribute back new coverts as needed be.
