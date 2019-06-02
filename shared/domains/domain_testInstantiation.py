__author__ = 'patras'

'''Test method parameter instantiation'''

from domain_constants import *
import importlib
loader = importlib.find_loader('RAE1_and_RAEplan')
if loader is not None:
    import RAE1_and_RAEplan as alg
import gui
from state import state, rv
from timer import globalTimer
import GLOBALS

def fail():
    return FAILURE

def m1_t(o):
    print("object is ", o, "\n")
    alg.do_command(fail)
# no preconditions

# r is not a task parameter for t
# r needs to be instantiated
def m2_t(o, r):
    print(rv.ROBOTS)
    gui.Simulate("object is ", o, "\n")
    gui.Simulate("robot is ", r, "\n")
    alg.do_command(fail)
m2_t.parameters = "[(r,) for r in rv.ROBOTS]"

# r1 and r2 are not task parameters
def m3_t(o, r1, r2):
    gui.Simulate("object is ", o, "\n")
    gui.Simulate("robots are ", r1, r2, "\n")
    alg.do_command(fail)
m3_t.parameters = "[(r1, r2,) for r1 in rv.ROBOTS for r2 in rv.ROBOTS if r1 != r2]"

def m4_t(o, loc):
    gui.Simulate("location is ", loc, o, "\n")
    alg.do_command(fail)
m4_t.parameters = "[(loc,) for loc in rv.LOCATIONS if loc == state.loc[o]]"

def t1_c1():
    return SUCCESS

def t1_c2():
    return SUCCESS

def m1_t1():
    gui.Simulate("t1")
    alg.do_command(t1_c1)

def m2_t1():
    gui.Simulate("m2_t1")
    alg.do_command(t1_c2)

def m1_t2():
    gui.Simulate("t2")
    alg.do_command(t1_c1)
    alg.do_task("t1")

alg.declare_task('t', 'o')
alg.declare_task('t1')
alg.declare_task('t2')

alg.declare_methods('t', m1_t, m2_t, m3_t, m4_t)
alg.declare_methods('t1', m1_t1, m2_t1)
alg.declare_methods('t2', m1_t2)

alg.declare_commands([fail, t1_c1, t1_c2])
