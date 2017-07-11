__author__ = 'patras'
from constants import *
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

def Unlatch(r, d, l, o, state):
    if (state.loc[r] == l and (l,d) in TOWARDSIDE and (d,'left') in SIDE  and (d, 'rotates') in TYPE and (d, o) in HANDLE):
        grasp(r, o, state)
        turn(r, o, 'alpha1', state)
        pull(r, 'val1', state)
        getStatus(r, d, state)
        if state.doorStatus[d] == 'cracked':
            ungrasp(r, o, state)
            res = SUCCESS
        else:
            res = FAILURE
            print("Robot %s is not able to unlatch %s\n" %(r, d))
    else:
        print("Robot %s is not in right position and orientation to unlatch %s using this method\n" %(r, d))
        res = FAILURE
    return res

def ThrowWide(r, d, l, o, state):
    if (state.loc[r] == l and (l, d) in TOWARDSIDE and (d, 'left') in SIDE and (d, 'rotates') in TYPE and (d, o) in HANDLE):
        grasp(r, o, state)
        pull(r, 'val1', state)
        moveBy(r, 'val2', state)
        res = SUCCESS
    else:
        print("Robot %s is not in right position and orientation to unlatch %s using this method\n" %(r, d))
        res = FAILURE
    return res

def OpenDoor(r, d, l, o, state):
    if state.loc[r] == l and (l, d) in ADJACENT and (d, o) in HANDLE:
        if state.reachable[r, o] == False:
            moveClose(r, o, state)
        if state.doorStatus[d] == 'unknown' or state.doorStatus[d] == 'closed' :
            Unlatch(r, d, l, o, state)
        ThrowWide(r, d, l, o, state)
        res = SUCCESS
    else:
        print("%s not in right position to open door %s" %(r,d))
        res = FAILURE

    return res

def RunOpenDoor1():
    state = rae1.State()
    state.doorStatus = { 'd2':'unknown'}
    state.loc = {'r1':3}
    state.reachable = {('r1','o2'):False}
    OpenDoor('r1', 'd2', 3, 'o2', state)
