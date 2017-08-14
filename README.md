RAE is working with multiple stacks. Each stack is implemented as a Python thread.

We have the following domains.

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
6. domain_exploreEnv: Robots and UAV move through an area and collects various data
   --- developed and integrated with RAE: testing needed
7. domain_industrialPlant: Orders of compound tasks involving painting, assembly and packing of components are handled
   --- developed and integrated with RAE: testing needed

HOW TO USE?
To test on any domain, import testRAE and use the following command in python

testRAE(domainCode)

domain codes are as follows:
domain_simpleFetch: 'SF',
domain_simpleOpenDoor: 'SOD',
domain_ste: 'STE',
domain_chargeableRobot: 'CR',
domain_springDoor: 'SD',
domain_exploreEnv: 'EE',
domain_industrialPlan: 'IP'

for example, to test Spring door, type
testRAE('SD')

You can see different amount of output by changing the verbosity as follows:
verbosity(0), verbosity(1) or verbosity(2)

The commands can be executed in two modes: 'Clock' or 'Counter'.
By default, the mode is set to 'Counter'.
To change mode, use:

SetMode('Counter') or SetMode('Clock')