from __future__ import print_function

"""
File RAE1_and_RAEplan.py
Author:
Sunandita Patra <patras@umd.edu>
"""

import threading
import multiprocessing

import math

import types
import sys, pprint
import os
import time
#import torch
#import torch.nn as nn

from state import GetState, PrintState, RestoreState, EvaluateParameters
from helper_functions import *

#import colorama
from timer import globalTimer, DURATION
from dataStructures import rL_PLAN
from APE_stack import print_entire_stack, print_stack_size

import stateSpaceUCT as ssu

#learning stuff
from learningData import trainingDataRecords
#from paramInfo import *
#from convertDataFormat import Encode_LearnM, Decode_LearnM, Encode_LearnH, Decode_LearnH, Encode_LearnMI, Decode_LearnMI

############################################################

### for debugging

verbose = 0     

def verbosity(level):
    """
    Specify how much debugging printout to produce:

    verbosity(0) makes RAE1 and RAEplan run silently; the only printout will be
    whatever the domain author has put into the commands and methods.

    verbosity(1) prints messages at the start and end, and
    print the name and args of each task and command.

    verbosity(2) makes RAE1 and RAEplan also print the states after executing commands.
    """

    global verbose
    verbose = level
    if level > 0:
        pass
        #import colorama

#only RAEplan
planLocals = rL_PLAN() # APEplan_systematic variables that are local to every call to APEplan_systematic, 
                       # we need this to be thread local because we have multiple stacks in APE as 
                       # multiple threads and each thread call its own APEplan_systematic



############################################################
# The user can use these to see what the commands and methods are.

# def print_commands(olist=commands):
#     """Print out the names of the commands"""
#     print('commands:', ', '.join(olist))

# def print_methods(mlist=methods):
#     """Print out a table of what the methods are for each task"""
#     print('{:<14}{}'.format('TASK:','METHODS:'))
#     for task in mlist:
#         print('{:<14}'.format(task) + ', '.join([f.__name__ for f in mlist[task]]))


   

