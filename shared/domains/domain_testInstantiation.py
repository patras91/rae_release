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
import numpy

def fail():
    return FAILURE

commandProb = {
    'sr1': [0.9, 0.1],
    'sr2': [0.7, 0.3],
    'sr3': [0.3, 0.7],
}

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


def Sense(cmd):
    p = commandProb[cmd]
    outcome = numpy.random.choice(len(p), 50, p=p)
    res = outcome[0]
    if res == 0:
        return SUCCESS
    else:
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

def c10():
    if state.v[0] == 1:
        return FAILURE
    else:
        return SUCCESS

def m1_t1():
    gui.Simulate("m1_t1\n")
    alg.do_command(t1_c1)

def m2_t1():
    gui.Simulate("m2_t1\n")
    alg.do_command(t1_c2)

def m1_t2():
    gui.Simulate("m1_t2\n")
    alg.do_command(t1_c1)
    alg.do_task("t1")

def m2_t2():
    gui.Simulate("m2_t2\n")
    alg.do_command(t1_c1)
    alg.do_task("t1")


def m1_t3():
    alg.do_task("t2")

def m2_t3():
    alg.do_task("t1")
    alg.do_task("t2")


# success ratio optimization test

def sr1():
    gui.Simulate('sr1')
    res = Sense('sr1')
    return res

def sr2():

    gui.Simulate('sr2')
    res = Sense('sr2')
    return res

def sr3():
    gui.Simulate('sr3')
    res = Sense('sr3')
    return res

def m1_tsr():
    alg.do_task('t_sr1')

def m2_tsr():
    alg.do_task('t_sr2')

def m1_tsr1():
    alg.do_command(sr1)
    alg.do_command(sr3)

def m1_tsr2():
    alg.do_command(sr2)

def m1_t10():
    alg.do_task('t10_1')
    alg.do_command(c10)

def m1_t10_1():
    gui.Simulate("m1\n")
    state.v[0] = 1

def m2_t10_1():
    gui.Simulate("m2\n")
    if state.v[0] != 1:
        state.v[0] = 2

def m1_tbackup():
    alg.do_command(fail)

def m2_tbackup():
    alg.do_command(fail)

def tBackup_Goal():
    if state.v[0] == 4:
        return True
    else:
        return False

alg.declare_task('t', 'o')
alg.declare_task('t1')
alg.declare_task('t2')
alg.declare_task('t3')
alg.declare_task('t_sr')
alg.declare_task('t_sr1')
alg.declare_task('t_sr2')
alg.declare_task('t10')
alg.declare_task('t10_1')
alg.declare_task('t10_2')

alg.declare_task('tbackup')
alg.declare_task('l1')

alg.declare_methods('t', m1_t, m2_t, m3_t, m4_t)
alg.declare_methods('t1', m1_t1, m2_t1)
alg.declare_methods('t2', m1_t2, m2_t2)
alg.declare_methods('t3', m1_t3, m2_t3)
alg.declare_methods('t_sr', m1_tsr, m2_tsr)
alg.declare_methods('t_sr1', m1_tsr1)
alg.declare_methods('t_sr2', m1_tsr2)
alg.declare_methods('t10', m1_t10)
alg.declare_methods('t10_1', m1_t10_1, m2_t10_1)
alg.declare_methods('tbackup', m1_tbackup, m2_tbackup)
alg.declare_methods('l1', t1_c1)# t1_c1)

alg.declare_goalCheck('tbackup', tbackup_Goal)

#alg.declare_commands([fail, t1_c1, t1_c2, sr1, sr2, sr3, c10, u1, u2, u3, u4])
alg.declare_commands([u1, u2, u3, u4, u5, u6, u7])

