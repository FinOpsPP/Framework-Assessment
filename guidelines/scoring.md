# Action Scoring Guide

Each of our actions is required to have a score that is objective in order to assess FinOps maturity and benchmark against peers. 
These scores come in a variety of method that are deemed acceptable for use in the assessment by way of being an objective measurement.
New scoring methods are always welcome and can be submitted for review to be added to this list and for specific action scores.
Below we list each of the approved scoring methods and detail how to construct new action scores that align with each format. 

**Contents**:
* [Score Types](#score-types)
* [Weights](#weights)

## Score Types:
1. [Bucket of Accomplishments](#bucket-of-accomplishments) - `bucket`
2. [Percentage Calculation](#percentage-calculation) - `percent`
3. [Other Mathematical Formulae](#other-mathematical-formulae) - `calculation`
4. [Multiple Weighted Buckets](#multiple-weighted-buckets) - `multi_bucket`
5. [Sequential Process](#sequential-process) - `sequential`

### Bucket of Accomplishments
**Score Type**: `bucket`

For actions that aim to measure how proficient a team is at a managerial or operational task, there are often no numerical values applicable to be used in a formula.
Therefore, to measure maturity of these actions, we create a list of necessary tasks that are included in mature FinOps practices.
These are not comprehensive tasks for an action, but represent tasks that lead to higher maturity of the action, and subsequent capabilities.
These tasks are unordered, meaning that different orgs can achieve the same score for the action via different tasks.
This is because there isn't just one way to reach maturity, and we wanted to leave flexibility for teams to choose their own path to get there.

### Percentage Calculation
**Score Type**: `percent`

This scoring method is straightforward. This score applies when there is a clear path to completion by iterating on the same task until all iterations are exhausted.
For example, percent of resources that are deployed with a mandatory tag, or percent of teams complying with a policy, etc. 

### Other Mathematical Formulae
**Score Type**: `calculation`

If there is a way to get a consistent, reliable numerical value to measure progress on an action, we can use that number in a formula to measure maturity.
There are no restrictions as of yet for what the formula could consist of, as long as the result is objective and repeatable.
We welcome submissions of any scores that have a mathematical formula similar or different from any currently listed in the assessment. 

### Multiple Weighted Buckets
**Score Type**: `multi_bucket`

This method is similar to the Bucket of Accomplishments. Instead of one large bucket with tasks to choose from, there are multiple lists.
These multiple lists could be weighted amongst eachother, or ranked in order if some tasks must happen first, etc. 
This also presents a way to account for multiple solutions to the same problem. Teams will be able to gain maturity points by completing tasks from both groups. 
For example, you could earn one point for doing task A or B in one bucket, this must be done before moving to the next bucket within the scoring method. 


    Do this first
    Do this second

    Whenever
    Whenever 2

or

    Do first
    Do second
    Do third
        whenever
        whenever 2


### Sequential Process
**Score Type**: `sequential`

This scoring method includes a rank ordered list of a procedure that FinOps teams should follow to improve their maturity.
These tasks must be done in the order that they appear, otherwise no additional points are calculated.
For example, cost allocation usually starts very broad and then gets more granular over time.
Those more granular allocations can only come after initial broader allocations are completed.

## Weights:
