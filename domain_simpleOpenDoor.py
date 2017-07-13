__author__ = 'patras'
from domain_constants import *
import rae1
import random

'''A simple example where a robot has to open a door. From Ch 3'''

#******************************************************
#commands controlling motion of the robot
def moveBy(r, lamda, state):
    print("Robot %s performs a motion defined by vector %s\n" %(r, lamda))
    return SUCCESS

def pull(r, lamda, state):
    print("Robot %s pulls its arm by vector %s\n" %(r, lamda))
    return SUCCESS

def push(r, lamda, state):
    print("Robot %s pushes its arm vector %s\n" %(r, lamda))
    return SUCCESS
#******************************************************

#******************************************************
#commands controlling movement of door handle by robot
def grasp(r, o, state):
    if state.reachable[r,o] == True:
        print("Robot %s has grasped handle %s\n" %(r, o))
        res = SUCCESS
    else:
        print("Robot %s cannot grasp handle %s because it is unreachable\n" %(r, o))
        res = FAILURE
    return res

def ungrasp(r, o, state):
    if state.reachable[r,o] == True:
        print("Robot %s has ungrasped handle %s\n" %(r, o))
        res = SUCCESS
    else:
        print("Robot %s cannot ungrasp handle %s because it is unreachable\n" %(r, o))
        res = FAILURE
    return res

def turn(r, o, alpha, state):
    if state.reachable[r,o] == True:
        print("Robot %s turns %s by %s\n" %(r, o, alpha))
        res = SUCCESS
    else:
        print("Robot %s cannot turn handle %s because it is unreachable\n" %(r, o))
        res = FAILURE
    return res
#******************************************************

def moveClose(r, o, state):
    if state.reachable[r,o] == False:
        print("Robot %s moves close to door handle %s\n" %(r, o))
        state.reachable[r,o] = True
        res = SUCCESS
    else:
        print("Robot %s is already close to handle %s\n" %(r, o))
        res = SUCCESS
    return res

def getStatus(r, d, state):
    print("Robot %s is monitoring the status of door %s\n" %(r, d))
    stat = random.choice(['closed', 'cracked'])
    print("Robot %s found it to be %s" %(r, stat))
    state.doorStatus[d] = stat
    return SUCCESS

def Unlatch_Method1(r, d, l, o, state, ipcArgs, stackid):
    if (state.loc[r] == l and (l,d) in TOWARDSIDE and (d,'left') in SIDE  and (d, 'rotates') in TYPE and (d, o) in HANDLE):
        rae1.do_command(grasp, r, o, state, ipcArgs, stackid)
        rae1.do_command(turn, r, o, 'alpha1', state, ipcArgs, stackid)
        rae1.do_command(pull, r, 'val1', state, ipcArgs, stackid)
        rae1.do_command(getStatus, r, d, state, ipcArgs, stackid)
        if state.doorStatus[d] == 'cracked':
            rae1.do_command(ungrasp, r, o, state, ipcArgs, stackid)
            res = SUCCESS
        else:
            res = FAILURE
            print("Robot %s is not able to unlatch %s\n" %(r, d))
    else:
        print("Robot %s is not in right position and orientation to unlatch %s using this method\n" %(r, d))
        res = FAILURE
    return res

def ThrowWide_Method1(r, d, l, o, state, ipcArgs, stackid):
    if (state.loc[r] == l and (l, d) in TOWARDSIDE and (d, 'left') in SIDE and (d, 'rotates') in TYPE and (d, o) in HANDLE):
        rae1.do_command(grasp, r, o, state, ipcArgs, stackid)
        rae1.do_command(pull, r, 'val1', state, ipcArgs, stackid)
        rae1.do_command(moveBy, r, 'val2', state, ipcArgs, stackid)
        res = SUCCESS
    else:
        print("Robot %s is not in right position and orientation to unlatch %s using this method\n" %(r, d))
        res = FAILURE
    return res

def OpenDoor_Method1(r, d, l, o, state, ipcArgs, stackid):
    if state.loc[r] == l and (l, d) in ADJACENT and (d, o) in HANDLE:
        if state.reachable[r, o] == False:
            rae1.do_command(moveClose, r, o, state, ipcArgs, stackid)
        if state.doorStatus[d] == 'unknown' or state.doorStatus[d] == 'closed' :
            rae1.do_task('unlatch', r, d, l, o, state, ipcArgs, stackid)
        rae1.do_task('throwWide', r, d, l, o, state, ipcArgs, stackid)
        res = SUCCESS
    else:
        print("%s not in right position to open door %s" %(r,d))
        res = FAILURE

    return res

def simpleOpenDoor_init():
    rae1.declare_commands(moveBy, pull, push, grasp, ungrasp, turn, moveClose, getStatus)
    print('\n')
    rae1.print_commands()

    rae1.declare_methods('unlatch', Unlatch_Method1)
    rae1.declare_methods('throwWide', ThrowWide_Method1)
    rae1.declare_methods('openDoor', OpenDoor_Method1)
    print('\n')
    rae1.print_methods()

    print('\n*********************************************************')
    print("* Call rae1 on simple open door using verbosity level 1.")
    print("* For a different amout of printout, try 0 or 2 instead.")
    print('*********************************************************\n')

    rae1.verbosity(0)

def simpleOpenDoor_run_1(ipcArgs, stackid):
    state = rae1.State()
    state.doorStatus = { 'd1':'unknown'}
    state.loc = {'r1':3}
    state.reachable = {('r1','o1'):False}

    rae1.rae1('openDoor', 'r1', 'd1', 3, 'o1', state, ipcArgs, stackid)

def simpleOpenDoor_run_2(ipcArgs, stackid):
    state = rae1.State()
    state.doorStatus = { 'd2':'unknown'}
    state.loc = {'r2':3}
    state.reachable = {('r2','o2'):False}

    rae1.rae1('openDoor', 'r2', 'd2', 3, 'o2', state, ipcArgs, stackid)