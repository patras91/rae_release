__author__ = 'patras'
from domain_constants import *
import rae1
import random
import gui
from timer import globalTimer

'''A simple example where a robot has to open a door. From Ch 3'''

#******************************************************
#commands controlling motion of the robot
def moveBy(r, lamda):
    start = globalTimer.GetTime()
    while(globalTimer.IsCommandExecutionOver('moveBy', start) == False):
	    pass
    gui.Simulate("Robot %s performs a motion defined by vector %s\n" %(r, lamda))
    return SUCCESS

def pull(r, lamda):
    start = globalTimer.GetTime()
    while(globalTimer.IsCommandExecutionOver('pull', start) == False):
	    pass
    gui.Simulate("Robot %s pulls its arm by vector %s\n" %(r, lamda))
    return SUCCESS

def push(r, lamda):
    start = globalTimer.GetTime()
    while(globalTimer.IsCommandExecutionOver('push', start) == False):
	    pass
    gui.Simulate("Robot %s pushes its arm vector %s\n" %(r, lamda))
    return SUCCESS
#******************************************************

#******************************************************
#commands controlling movement of door handle by robot
def grasp(r, o):
    rae1.state.reachable.AcquireLock(r,o)
    if rae1.state.reachable[r,o] == True:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('grasp', start) == False):
	        pass
        gui.Simulate("Robot %s has grasped handle %s\n" %(r, o))
        res = SUCCESS
    else:
        gui.Simulate("Robot %s cannot grasp handle %s because it is unreachable\n" %(r, o))
        res = FAILURE
    rae1.state.reachable.ReleaseLock(r,o)
    return res

def ungrasp(r, o):
    rae1.state.reachable.AcquireLock(r,o)
    if rae1.state.reachable[r,o] == True:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('ungrasp', start) == False):
	        pass
        gui.Simulate("Robot %s has ungrasped handle %s\n" %(r, o))
        res = SUCCESS
    else:
        gui.Simulate("Robot %s cannot ungrasp handle %s because it is unreachable\n" %(r, o))
        res = FAILURE
    rae1.state.reachable.ReleaseLock(r,o)
    return res

def turn(r, o, alpha):
    rae1.state.reachable.AcquireLock(r,o)
    if rae1.state.reachable[r,o] == True:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('turn', start) == False):
	        pass
        gui.Simulate("Robot %s turns %s by %s\n" %(r, o, alpha))
        res = SUCCESS
    else:
        gui.Simulate("Robot %s cannot turn handle %s because it is unreachable\n" %(r, o))
        res = FAILURE
    rae1.state.reachable.ReleaseLock(r,o)
    return res
#******************************************************

def moveClose(r, o):
    rae1.state.reachable.AcquireLock(r,o)
    if rae1.state.reachable[r,o] == False:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('moveClose', start) == False):
	        pass
        gui.Simulate("Robot %s moves close to door handle %s\n" %(r, o))
        rae1.state.reachable[r,o] = True
        res = SUCCESS
    else:
        gui.Simulate("Robot %s is already close to handle %s\n" %(r, o))
        res = SUCCESS
    rae1.state.reachable.ReleaseLock(r,o)
    return res

def getStatus(r, d):
    start = globalTimer.GetTime()
    while(globalTimer.IsCommandExecutionOver('getStatus', start) == False):
        pass
    gui.Simulate("Robot %s is monitoring the status of door %s\n" %(r, d))
    stat = random.choice(['closed', 'cracked'])
    gui.Simulate("Robot %s found it to be %s\n" %(r, stat))
    rae1.state.doorStatus.AcquireLock(d)
    rae1.state.doorStatus[d] = stat
    rae1.state.doorStatus.ReleaseLock(d)
    return SUCCESS

def Unlatch_Method1(r, d, o):
    if ((rae1.state.loc[r],d) in rv.TOWARDSIDE and (d,'left') in rv.SIDE  and (d, 'rotates') in rv.TYPE and (d, o) in rv.HANDLE):
        rae1.do_command(grasp, r, o)
        rae1.do_command(turn, r, o, 'alpha1')
        rae1.do_command(pull, r, 'val1')
        rae1.do_command(getStatus, r, d)
        if rae1.state.doorStatus[d] == 'cracked':
            rae1.do_command(ungrasp, r, o)
            res = SUCCESS
        else:
            res = FAILURE
            gui.Simulate("Robot %s is not able to unlatch %s\n" %(r, d))
    else:
        gui.Simulate("Robot %s is not in right position and orientation to unlatch %s\n" %(r, d))
        res = FAILURE
    return res

def ThrowWide_Method1(r, d, o):
    if ((rae1.state.loc[r], d) in rv.TOWARDSIDE and (d, 'left') in rv.SIDE and (d, 'rotates') in rv.TYPE and (d, o) in rv.HANDLE and rae1.state.doorStatus[d] == 'cracked'):
        rae1.do_command(grasp, r, o)
        rae1.do_command(pull, r, 'val1')
        rae1.do_command(moveBy, r, 'val2')
        res = SUCCESS
    else:
        gui.Simulate("Robot %s is not in right position and orientation to throw wide %s\n" %(r, d))
        res = FAILURE
    return res

def OpenDoor_Method1(r, d, o):
    if (rae1.state.loc[r], d) in rv.ADJACENT and (d, o) in rv.HANDLE:
        if rae1.state.reachable[r, o] == False:
            rae1.do_command(moveClose, r, o)
        if rae1.state.doorStatus[d] == 'unknown' or rae1.state.doorStatus[d] == 'closed' :
            rae1.do_task('unlatch', r, d, o)
        rae1.do_task('throwWide', r, d, o)
        res = SUCCESS
    else:
        gui.Simulate("%s not in right position to open door %s" %(r,d))
        res = FAILURE

    return res

rv = RV()
rae1.declare_commands(moveBy, pull, push, grasp, ungrasp, turn, moveClose, getStatus)
print('\n')
rae1.print_commands()

rae1.declare_methods('unlatch', Unlatch_Method1)
rae1.declare_methods('throwWide', ThrowWide_Method1)
rae1.declare_methods('openDoor', OpenDoor_Method1)
print('\n')
rae1.print_methods()

print('\n*********************************************************')
print("* Call rae1 on simple open door domain.")
print("* For a different amout of printout,  try verbosity(0), verbosity(1), or verbosity(2).")
print('*********************************************************\n')
