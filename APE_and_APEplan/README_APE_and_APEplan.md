APE and APEplan together form a refinement acting-and-planning engine with multiple stacks. Each stack is implemented as a Python thread.

We have the following domains in the domain folder.

1. domain_chargeableRobot: A chargeable robot collecting different objects
2. domain_springDoor: Robot needs to collect objects in an environment with spring doors
3. domain_exploreEnv: Robots and UAV move through an area and collects various data
4. domain_industrialPlant: Orders of compound tasks involving painting, assembly and packing of components are handled

# The following may not work as expected: not tested recently
5. domain_simpleFetch: Robot collecting objects in a harbour
6. domain_simpleOpenDoor: Robot opening a door
7. domain_ste: Robot travelling from one location to another by foot or taxi

HOW TO USE?
To test on any domain, use the following command in terminal

python3 testAPE.py [-h] [--v V] [--domain D] [--problem P] [--s S] [--c C]
optional arguments:
  -h, --help  show this help message and exit
  --v V       verbosity of RAE's debugging output (0, 1 or 2)
  --domain D       name of the test domain (STE, CR, SD, EE, SOD, IP or SF)
  --p P       identifier for the problem eg. 'problem1', 'problem2', etc
  --s S       Do you want to use APE-plan or not? ('y' or 'n')
  --c C       Mode of the clock ('Counter' or 'Clock')

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

python3 testAPE.py --domain SD --problem problem1

The commands can be executed in two modes: 'Clock' or 'Counter'.
By default, the mode is set to 'Counter'.