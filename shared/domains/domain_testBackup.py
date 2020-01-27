__author__ = 'patras'

'''Test UCT backup strategy'''

from domain_constants import *
import importlib
loader = importlib.find_loader('RAE1_and_RAEplan')
if loader is not None:
    import RAE1_and_RAEplan as alg
import gui
from state import state, rv
from timer import globalTimer
import GLOBALS
import numpy

import UCTwithCommandsOnly as cOnly 

def fail():
    return FAILURE

def u1():
    state.v[0] = 0
    return SUCCESS

def u2():
    if state.v[0] == 0:
        state.v[0] = 2
        return SUCCESS
    else:
        return FAILURE

def u3():
    if state.v[0] == 2:
        state.v[0] = 3
        return SUCCESS
    else:
        return FAILURE

def u4():
    if state.v[0] == 1:
        state.v[0] = 4
        return SUCCESS
    else:
        return FAILURE

def u5():
    if state.v[0] == 0:
        state.v[0] = 2
        return SUCCESS
    else:
        return FAILURE

def u6():
    if state.v[0] == 2:
        state.v[0] = 5
        return SUCCESS
    else:
        return FAILURE

def u7():
    if state.v[0] == 2:
        state.v[0] = 6
        return SUCCESS
    else:
        return FAILURE

def tbackup_Goal():
    if state.v[0] == 4:
        return True
    else:
        return False

def m1_tbackup():
    alg.do_command(fail)

def m2_tbackup():
    alg.do_command(fail)

alg.declare_task('tbackup')

alg.declare_methods('tbackup', m1_tbackup, m2_tbackup)

alg.declare_commands([u1, u2, u3, u4, u5, u6, u7, fail])

cOnly.declare_goalCheck('tbackup', tbackup_Goal)
