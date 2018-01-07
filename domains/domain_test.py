from __future__ import print_function
__author__ = 'patras'
import sys
from domain_constants import *
from timer import globalTimer

import copy
import rae1
import gui

def c1():
    start = globalTimer.GetTime()
    while(globalTimer.IsCommandExecutionOver('c1', start) == False):
        pass
    rae1.state.value['a'] = 1
    return SUCCESS

def c1_Sim():
    start = globalTimer.GetTime()
    while(globalTimer.IsCommandExecutionOver('c1', start) == False):
        pass
    rae1.state.value['a'] = 1
    return SUCCESS

def c2():
    start = globalTimer.GetTime()
    while(globalTimer.IsCommandExecutionOver('c2', start) == False):
        pass
    rae1.state.value['a'] = 2
    return SUCCESS

def c2_Sim():
    start = globalTimer.GetTime()
    while(globalTimer.IsCommandExecutionOver('c2', start) == False):
        pass
    rae1.state.value['a'] = 2
    return SUCCESS

def c3():
    start = globalTimer.GetTime()
    while(globalTimer.IsCommandExecutionOver('c3', start) == False):
        pass
    rae1.state.value['a'] = 3
    return SUCCESS

def c3_Sim():
    start = globalTimer.GetTime()
    while(globalTimer.IsCommandExecutionOver('c3', start) == False):
        pass
    rae1.state.value['a'] = 3
    return SUCCESS

def t1_m1():
    rae1.do_task('t11')
    rae1.do_task('t12')
    return SUCCESS

def t11_m1():
    rae1.do_command(c1)
    return SUCCESS

def t11_m2():
    rae1.do_command(c2)
    return SUCCESS

def t12_m1():
    rae1.do_command(c2)
    return SUCCESS

def t12_m2():
    rae1.do_command(c3)
    return SUCCESS

def t1_m2():
    rae1.do_task('t12')
    return SUCCESS

def t2_m1():
    rae1.do_task('t3')
    rae1.do_command(c2)
    return SUCCESS

def t2_m2():
    rae1.do_task('t3')
    rae1.do_command(c3)
    return SUCCESS

def t3_m1():
    rae1.do_command(c3)
    return SUCCESS

def t2_m2():
    rae1.do_task('t3')
    rae1.do_command(c3)
    return SUCCESS

rv = RV()

rae1.declare_commands([c1, c2, c3], [c1_Sim, c2_Sim, c3_Sim])

rae1.declare_methods('t1', t1_m1, t1_m2)
rae1.declare_methods('t11', t11_m1, t11_m2)
rae1.declare_methods('t12', t12_m1, t12_m2)
rae1.declare_methods('t2', t2_m1, t2_m2)
rae1.declare_methods('t3', t3_m1)
