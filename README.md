RAE is a refinement acting engine with multiple stacks. Each stack is implemented as a Python thread.

We have the following domains in the domain folder.

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
To test on any domain, use the following commands in python

from testRAE import *
testRAE(domainCode, problemId)

domain codes are as follows:
domain_simpleFetch: 'SF',
domain_simpleOpenDoor: 'SOD',
domain_ste: 'STE',
domain_chargeableRobot: 'CR',
domain_springDoor: 'SD',
domain_exploreEnv: 'EE',
domain_industrialPlan: 'IP'

The problemid should correspond to a problem inside the folder 'problems'.
A problem file specifies the initial state, the tasks arriving at different times and
various parameters specific to the domain. To define a new problem, please follow the
following syntax to name the file.

problemId_domainCode.py

For example, a problem of SD domain with problemId 'problem1' should be named problem1_SD.py.
To test problem1 of Spring door, use the command:

testRAE('SD', 'problem1')

You can see different amount of output by changing the verbosity as follows:
verbosity(0), verbosity(1) or verbosity(2)

The commands can be executed in two modes: 'Clock' or 'Counter'.
By default, the mode is set to 'Counter'.
To change mode, use:

SetMode('Counter') or SetMode('Clock')