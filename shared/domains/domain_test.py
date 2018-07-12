from __future__ import print_function
__author__ = 'patras'
import sys
from domain_constants import *
from timer import globalTimer

import copy
import importlib
loader = importlib.find_loader('RAE1_and_RAEplan')
if loader is not None:
    import RAE1_and_RAEplan as ape
else:
    import ape1_and_apeplan as ape

from state import state
import gui

def c1():
    start = globalTimer.GetTime()
    while(globalTimer.IsCommandExecutionOver('c1', start) == False):
        pass
    state.value['a'] = 1
    return SUCCESS

def c1_Sim():
    start = globalTimer.GetTime()
    while(globalTimer.IsCommandExecutionOver('c1', start) == False):
        pass
    state.value['a'] = 1
    return SUCCESS

def c2():
    start = globalTimer.GetTime()
    while(globalTimer.IsCommandExecutionOver('c2', start) == False):
        pass
    state.value['a'] = 2
    return SUCCESS

def c2_Sim():
    start = globalTimer.GetTime()
    while(globalTimer.IsCommandExecutionOver('c2', start) == False):
        pass
    state.value['a'] = 2
    return SUCCESS

def c3():
    start = globalTimer.GetTime()
    while(globalTimer.IsCommandExecutionOver('c3', start) == False):
        pass
    state.value['a'] = 3
    return SUCCESS

def c3_Sim():
    start = globalTimer.GetTime()
    while(globalTimer.IsCommandExecutionOver('c3', start) == False):
        pass
    state.value['a'] = 3
    return SUCCESS

def c4():
    return FAILURE

def c5():
    return SUCCESS

def t1_m1():
    ape.do_task('t11')
    ape.do_task('t12')
    return SUCCESS

def t11_m1():
    ape.do_command(c1)
    return SUCCESS

def t11_m2():
    ape.do_command(c2)
    return SUCCESS

def t12_m1():
    ape.do_task('t6')
    ape.do_command(c1)
    return SUCCESS

def t12_m2():
    ape.do_command(c3)
    return SUCCESS

def t1_m2():
    ape.do_task('t12')
    return SUCCESS

def t2_m1():
    ape.do_task('t3')
    ape.do_command(c2)
    return SUCCESS

def t2_m2():
    ape.do_task('t3')
    ape.do_command(c3)
    return SUCCESS

def t3_m1():
    ape.do_command(c3)
    return SUCCESS

def t4_m1():
    ape.do_command(c4)
    return SUCCESS

def t4_m2():
    ape.do_command(c5)
    return SUCCESS

def t6_m1():
    ape.do_command(c4)
    return SUCCESS

def t6_m2():
    ape.do_command(c5)
    return SUCCESS

rv = RV()

ape.declare_commands([c1, c2, c3, c4, c5])

ape.declare_methods('t1', t1_m1, t1_m2)
ape.declare_methods('t11', t11_m1, t11_m2)
ape.declare_methods('t12', t12_m1, t12_m2)
ape.declare_methods('t2', t2_m1, t2_m2)
ape.declare_methods('t3', t3_m1)
ape.declare_methods('t4', t4_m1, t4_m2)
ape.declare_methods('t6', t6_m1, t6_m2)
