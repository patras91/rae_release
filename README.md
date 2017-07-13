RAE is working with multiple stacks. Each stack is implemented a Python thread.
Some issues to be resolved:
    1. Sharing the state variables globally instead of always passing them as a parameter to the tasks and commands
    2. Review in the code which portions are critical sections and which are not. Match this with the pseudocode
    3. Handle incoming sequence of tasks as another thread instead of assuming a predefined list of tasks

We have the following domains

1. domain_simpleFetch: Robot collecting objects in a harbour
   --- developed and integrated with RAE: testing needed
2. domain_simpleOpenDoor: Robot opening a door
   --- developed and integrated with RAE: testing needed
3. domain_ste: Robot travelling from one location to another by foot or taxi
   --- developed and integrated with RAE: testing needed
4. domain_chargeableRobot: A chargeable robot collecting different objects
   --- developed and integrated with RAE: testing needed
5. domain_springDoor: Robot needs to collect objects in an environment with spring doors
   --- developed and integrated with RAE: testing needed

HOW TO USE?
To test on any domain, import testRAE and use the following command in python

testRAE(domainCode)

domain codes are as follows:
domain_simpleFetch: 'SF',
domain_simpleOpenDoor: 'SOD',
domain_ste: 'STE',
domain_chargeableRobot: 'CR',
domain_springDoor: 'SD'

for example, to test Spring door, type
testRAE('SD')