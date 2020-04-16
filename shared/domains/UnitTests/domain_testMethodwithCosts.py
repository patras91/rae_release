__author__ = 'patras'

'''Test methods with costs'''

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
from timer import DURATION

DURATION.COUNTER = {
    'c1': 50,
    'c2': 2,
    'c3': 8,
    'c4': 40,
}

def c1():
    return SUCCESS

def c2():
    return SUCCESS

def c3():
    return SUCCESS

def c4():
    return SUCCESS

def fail():
    return FAILURE

def m1_t():
    gui.Simulate("m1_t")
    alg.do_command(c1)

def m2_t():
    gui.Simulate("m2_t")
    alg.do_command(c2)
m2_t.cost = 10

def m3_t():
    gui.Simulate("m3_t")
    alg.do_command(c3)
m3_t.cost = 1

alg.declare_task('t')

alg.declare_methods('t', m1_t, m2_t, m3_t)

alg.declare_commands([fail, c1, c2, c3, c4])

