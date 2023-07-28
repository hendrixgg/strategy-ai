from task import BaseTask
"""I have not thought through how we would do this activity, so this gives you some space to have some fun!

The simple example to work through is that which I talked about on the call today where we want a 20% growth in sales.

Pick a department or function. Examples would be the Sales Department, Customer Service function, or Operations. We need to explore what the increase would be over the previous year for that area, explore possible Objectives, and Key Results then look at the gap in the Key Results from last year's performance and develop recommendations to close the gap.

A slightly more sophisticated version would then look at the organizations capacity, budgets, etc. and determine if they have the right resources to close the gap. 

Potential Questions to answer:
- What would be the impact on the organization if they did not close the gap?
- If not, what would be required to close the gap?
- What remediation reccomendations would you make to the organization?
"""

"""Let's say that we are looking at the Sales Department. We want to get $10M in sales this year. Last year we had $8M in sales. I would like an AI tool that takes a look at a bunch of different things to see what is the likelihood that sales can actually go to $10M. It's going to have to take a look at headcount, budget, projects, problems, and come back with some feedback on where the sales department needs to focus their effort to get their sales to the target level.

If the target level is infeasible, I would like the tool to identify what it thinks the target level should be, or what would need to change to make that target level feasible.
"""

# Simple solution:
"""Specify a timeframe to do the analysis, lets pick a **year**.

Given a department or business function and key results achieved last year. 

1. Calculate the change required to reach the new target.
2. Bring up some objectives from last year and some possible new objectives that could be used to reach the new target.
3. compare the key results from last year to the new target and what the new key results would need to be in order to achieve the new target.
"""


# Sophisticated solution:
"""First we need to decide on what the smallest timeframe we want to consider, since each decision/action will take place and performance will be measured in intervals. For example, we could consider the smallest timeframe to be a day, a week, a month, a quarter, a year, etc. I think we should consider a quarter to be the smallest timeframe we consider at this point in time.

I need a tool that takes a look at a department (ex: sales) and understands the following:
- **what** the department achieved over the **last timeframe** (ex: $8M in sales selling products/services x, y, z, to customers a, b, c; over 1 quarter)
- the department's past performance (ex: 10% growth in sales, 5% growth in sales, 2% growth in sales)
- the department's and culture (startup vs. mature, vacation season vs. busy season, relaxed vs. stressed, etc.)
- **how** the department achieved what they did last year
    - strategy map
    - objectives
    - key results
    - processes (in place and in development) (self sustaining, manual, automated, etc.)
- the resources that the department has at their disposal (what they are using and what they could be using)
    - understands the department's budget (ex: $1M)
    - understands the department's capacity and what they are assigned to (ex: 10 sales people, 1 sales manager, 1 sales director, 1 sales VP, 1 sales admin, 1 sales operations manager, 1 sales operations analyst)
    - understands the department's projects and timelines
    - understands the department's technology/tools/partnerships/potential deals and the revenue they could bring in
- the department's internal problems/risks
    - understands the department's processes/bottlenecks (ex: process 1, process 2, process 3)
    - understand the department's various costs for increase in capacity or for new technologies or tools
- understands their external problems/risks from their competitors
- understands new potential opportunities they (or their competitors) could take advantage of 
    - and the revenue 
    - and associated probability of success

- different types of revenue generation: active, passive, recurring, one-time
- different types of costs: fixed, variable, one-time, recurring
- different types of capacity: run the business, change the business

Then provide feedback on the following possible actions that could be taken, noting: (+- impact on Revenue (R), +- impact on Costs (C), +- impact on Capacity/Energy (E))
- what if they did nothing and everyone was fired? what remaining processes are in place that drive recurring revenue, how long do those things last? (baseline)
- what if they did the same thing as last year? (what are the delta's in R, C, E from baseline?)
- how could they lower costs or free up resources? (what would be the associated impact on revenue? what could be done with the freed up resources?)
- what if they maximized revenue (what is impact on costs? and capacity?)
- what if they minimized costs (what is impact on revenue? and capacity?)
- what if they maximized capacity (what is impact on revenue? and costs?)
- what if they minimized capacity (what is impact on revenue? and costs?)

Then, provide a range of targets that the department could achieve and the associated changes that may result in those targets being achieved.
- understands the department's _target_ (ex: get $10M in sale's selling products/services x, y, z, to customers a, b, c)

Then, provide feedback on the possibility of the department achieving their initial target.
"""
