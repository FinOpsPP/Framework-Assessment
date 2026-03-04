# Action Scoring Guide

Each of our actions is required to have a score that is objective in order to assess FinOps maturity and benchmark against peers. 
These scores come in a variety of method that are deemed acceptable for use in the assessment by way of being an objective measurement.
We require each scoring method to be converted to an integer score between 0 and 10 for effective use in the assessment.
New scoring methods are always welcome and can be submitted for review to be added to this list and for specific action scores.
Below we list each of the approved scoring methods and detail how to construct new action scores that align with each format. 

**Contents**:
* [Score Types](#score-types)
* [Weights](#weights)
* [Targets](#targets)

## Score Types:
1. [Bucket of Accomplishments](#bucket-of-accomplishments) - `bucket`
2. [Percentage Calculation](#percentage-calculation) - `percent`
3. [Other Mathematical Formulae](#other-mathematical-formulae) - `calculation`
4. [Multiple Weighted Buckets](#multiple-weighted-buckets) - `multi_bucket`
5. [Sequential Process](#sequential-process) - `sequential`

---
### Bucket of Accomplishments
**Score Type**: `bucket`

**Description**:
For actions that aim to measure how proficient a team is at a managerial or operational task, there are often no numerical values applicable to be used in a formula.
Therefore, to measure maturity of these actions, we create a list of necessary tasks that are included in mature FinOps practices.
These are not comprehensive tasks for an action, but represent tasks that lead to higher maturity of the action, and subsequent capabilities.
These tasks are unordered, meaning that different orgs can achieve the same score for the action via different tasks.
This is because there isn't just one way to reach maturity, and we wanted to leave flexibility for teams to choose their own path to get there.

**Example**: From action [034](https://github.com/FinOpsPP/Framework-Assessment/blob/main/components/actions/034.md)

This action falls under the Planning and Estimating Capability and is titled: "Establish Scenario Decision Process."
For this score, we have a bucket of three items to complete to reach a high maturity.
The formula used here is `10*Ceil(x/3)` which represents the percent of items completed rounded up to the next integer.
So 1/3 = .33... rounds to 4, 2/3 = 0.66... rounds to 7, and 3/3 will get you a score of 10.
The bucket score relies on the fact that the formula items are independent, and you don't need to complete them in any order.

**YAML Format**:
  ```
  Formula: |-
    * Define and follow process for gathering deployment plans from teams
    * Determine timeline for each new project to adjust the forecast during that time
    * Determine how optimizations and lower run rate will impact the forecast on a rolling basis

    10*Ceil(x/3)
  Scoring:
  - Score: 0
    Condition: No items completed
  - Score: 4
    Condition: 1 item completed
  - Score: 7
    Condition: 2 items completed
  - Score: 10
    Condition: 3 items completed
```

---
### Percentage Calculation
**Score Type**: `percent`

**Description**:
This scoring method is straightforward. This score applies when there is a clear path to completion by iterating on the same task until all iterations are exhausted.
For example, percent of resources that are deployed with a mandatory tag, or percent of teams complying with a policy, etc. 

**Example**: From action [010](https://github.com/FinOpsPP/Framework-Assessment/blob/main/components/actions/010.md)

This action falls under the Allcoation Capability and is titled: "Identify Shared Costs & Rules"
Here, we would like to determine our apportionment rules for shared costs, and document progress towards full allocation.
Thus, we can use a mathematical formula to calculate the percentage of our shared costs that have been allocated.
This formula converts to our score between 0 and 10 based on percentage.
If your allocation is at 49%, you will receive a score of 4. It is only when it crosses each threshold that you move up to the next score level.

**YAML Format**:
```
Formula: Unallocated Shared CSP Effective Cloud Cost/ Total CSP Effective Cloud
    Cost
  Scoring:
  - Score: 0
    Condition: 0%
  - Score: 1
    Condition: 10%
  - Score: 2
    Condition: 20%
  - Score: 3
    Condition: 30%
  - Score: 4
    Condition: 40%
  - Score: 5
    Condition: 50%
  - Score: 6
    Condition: 60%
  - Score: 7
    Condition: 70%
  - Score: 8
    Condition: 80%
  - Score: 9
    Condition: 90%
  - Score: 10
    Condition: Near 100%
```

---
### Other Mathematical Formulae
**Score Type**: `calculation`

**Description**:
If there is a way to get a consistent, reliable numerical value to measure progress on an action, we can use that number in a formula to measure maturity.
There are no restrictions as of yet for what the formula could consist of, as long as the result is objective and repeatable.
We welcome submissions of any scores that have a mathematical formula similar or different from any currently listed in the assessment. 

**Example**:
Since this method is left open to ideas, we don't have examples in use yet.
But it could be something similar to log returns of ROI Unit Economics KPIs which would have the formula `log(1 + r)` where r is your percent return.
Feel free to find creative solutions that can quantify progress in any of the action areas.

**YAML Format**:

---
### Multiple Weighted Buckets
**Score Type**: `multi_bucket`

**Description**:
This method is similar to the Bucket of Accomplishments. Instead of one large bucket with tasks to choose from, there are multiple lists.
These multiple lists could be weighted amongst eachother, or ranked in order if some tasks must happen first, etc. 
This also presents a way to account for multiple solutions to the same problem. Teams will be able to gain maturity points by completing tasks from both groups. 
For example, you could earn one point for doing task A or B in one bucket, this must be done before moving to the next bucket within the scoring method. 

**Example**:
While we don't have this scoring method in use as of yet, we expect that this will be a common method to employ for various action scoring.
The example yml format shows that different tasks do have different weights (different from the overall weight of the action score).
Here, items 1 and 2 get you more points than the items in bucket 3. Therefore, the initial steps are weighted more heavily than the subsequent ones.
Other combinations of formula items can be created as well that fit this method.

**YAML Format**:
```
  Formula: |-
    1. Must do first
    2. Either or
        * choice 1
        * choice 2
    3. Bucket
        * item 1
        * item 2
  
  Scoring:
  - Score: 0
    Condition: no items completed
  - Score: 4
    Condition: item 1 completed
  - Score: 6
    Condition: item 1 and 2 completed
  - Score: 8
    Condition: item 1, 2, and 1/2 of item 3 completed
  - Score: 10
    Condition: item 1, 2, and 2/2 of item 3 completed
```

---
### Sequential Process

**Score Type**: `sequential`

**Description**:
This scoring method includes a rank ordered list of a procedure that FinOps teams should follow to improve their maturity.
These tasks must be done in the order that they appear, otherwise no additional points are calculated.
For example, cost allocation usually starts very broad and then gets more granular over time.
Those more granular allocations can only come after initial broader allocations are completed.

**Example**:

It is unlikely that you will complete an item further down the list effectively without first completing the preceeding items on the list.
Therefore, you only get points for completing the items in order to reach the next level.
The scoring values are still based on the Ceil function mentioned in the bucket method, where you round up to the next integer based on percent completion of all the tasks in order.

**YAML Format**:
```
  Formula: |-
    1. item 1
    2. item 2
    3. etc...
  Scoring:
  - Score: 0
    Condition: No items completed
  - Score: 4
    Condition: item 1 completed
  - Score: 7
    Condition: items 1 and 2 completed
  - Score: 10
    Condition: items 1, 2, and 3 completed
```

---

## Weights:

Weights are a way for finops teams to customize the assessment based on what is important to the business.
For example, if an action or entire capability is low priority for the business, then you can essentially filter those out of the assessment by setting the weight to zero.
A company may still prioritize completing multiple actions, but some actions are higher priority than others.
You can add in this customization by adjusting the weights. A weight of 1 means top priority, but a weight of 0.5 might mean it is a nice to have or a stretch goal.

## Targets:

This is the maturity goal that a finops team wants to reach by the next assessment evaluation, or over a longer term.
For each action, the target is the desired maturity score after improvements are made, not a current evaluation of the score.
For example, a company may desire to be at a level 10 maturity for an action in the next few years,
but a quarterly target may be to increase that score by one or two points based on the team capacity for improvements. 
