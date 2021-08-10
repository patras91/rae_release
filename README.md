# RAE and UPOM

RAE and UPOM together form a refinement acting-and-planning engine.

# Conda Setup Steps:

Install conda: https://docs.conda.io/projects/conda/en/latest/user-guide/install/

    conda env create -f RAE.yml
    conda activate RAE

To test problem1 of fetch via command line, use the commands:

    python3 main.py --domain fetch --problem problem1

To test using the visual GUI, simply run main_interface.py

# Test Domains

We have the following domains in the ./domains folder.

1. `domain_fetch`: A chargeable robot collecting different objects
2. `domain_nav`: Robot needs to collect objects in an environment with spring doors and ordinary doors
3. `domain_explore`: Robots and UAV move through a partially mapped terrain and collects various data
4. `domain_rescue`: UAVs and UGVs carry out search and rescue operations
5. `domain_deliver`: Robots pack objects in a warehouse and deliver them to a loading dock

# How to run?

To test on any domain, use the following command in terminal

    python3 main.py [-h] [--v V] [--domain D] [--problem PROBLEMNAME] 

    optional arguments:
      -h, --help  	show this help message and exit
      --v V      	verbosity of RAE and UPOM's debugging output (0, 1 or 2)
      --domain D    domain ID of the test domain ("fetch", "nav", "rescue", "explore", deliver") 
      --problem P   problem id for the problem eg. 'problem1', 'problem2', etc. The problem id should correspond to a problem inside the folder 'problems/domain'.
      --n_RO numRollouts 	Number of rollouts of UPOM


# How to add new problems? 

Please go inside the folder ./domains/<domainID>/problems/ to view examples of problem files. 
A problem file  specifies the initial state, the tasks arriving at different times and various parameters specific to the domain. Please follow the
following syntax to name a problem file.

`problemId_DomainID.py`

For example, a problem of fetch domain with problemId `problem1` should be named `problem1_fetch.py`.




