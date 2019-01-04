RAE and RAEplan together form a refinement acting-and-planning engine with multiple stacks. Each stack corresponds to performing one incoming job (the task specified by the user).
Each stack is implemented as a Python thread.

We have the following domains in the folder /shared/domains/.

1. domain_chargeableRobot: A chargeable robot collecting different objects
2. domain_springDoor: Robot needs to collect objects in an environment with spring doors
3. domain_exploreEnv: Robots and UAV move through an area and collects various data
4. domain_industrialPlant: Orders of compound tasks involving painting, assembly and packing of components are handled
5. domain_searchAndRescue: Robots examine and monitor a 2D area and help victims of a natural disaster

HOW TO USE?
To test on any domain, do the following steps:

1. Go to the folder RAE_and_RAEplan

2. python3 testRAEandRAEplan.py [-h] [--v V] [--domain D] [--problem P] [--plan S] [--c C] [--b breadth]
optional arguments:
  -h, --help  	show this help message and exit
  --v V      	verbosity of RAE and RAEplan's debugging output (0, 1 or 2)
  --domain D    domain code of the test domain (STE, CR, SD, EE, SOD, IP or SF) (see below)
  --problem P   problem id for the problem eg. 'problem1', 'problem2', etc. The problem id should correspond to a
                problem inside the folder 'problems'.
  --plan pl   	Do you want to use planning or not? ('y' or 'n')
  --c C      	Mode of the clock ('Counter' or 'Clock')
  --b breadth 	Number of methods RAEplan should look at (for each task and sub-task) during planning
  --k commandSamples 	Number of outcomes of every command RAEplan should look at during planning

domain codes are as follows:
domain_chargeableRobot: 'CR',
domain_springDoor: 'SD',
domain_exploreEnv: 'EE',
domain_industrialPlan: 'IP'
domain_searchAndRescue: 'SR'


HOW TO ADD NEW PROBLEMS? 
A problem file (Please go inside the folder /shared/problems to view problems) specifies the initial state, the tasks arriving at different times and various parameters specific to the domain. To define a new problem, please follow the
following syntax to name the file.

problemId_domainCode.py

For example, a problem of SD domain with problemId 'problem1' should be named problem1_SD.py.
To test problem1 of Spring door, use the command:

python3 testRAEandRAEplan.py --domain SD --problem problem1
