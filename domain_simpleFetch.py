__author__ = 'patras'
import rae1
from domain_constants import *

'''A simple example where a robot has to fetch an object in a harbor and handle emergencies. From Ch 3'''

def moveTo(r, l, state):
    print("Robot %s has gone to location %d\n" %(r,l))
    state.loc[r] = l
    return SUCCESS

def take(r, o, l, state):
    if state.pos[o] == l:
        state.pos[o] = r
        state.load[r] = o
        print("Robot %s has taken object %s at location %d\n" %(r,o,l))
        res = SUCCESS
    else:
        print("Object %s is not at location %d\n" %(o,l))
        res = FAILURE
    return res

def put(r, o, l, state):
    if state.pos[o] == r:
        state.pos[o] = l
        state.load[r] = NIL
        print("Robot %s has put object %s at location %d\n" %(r,o,l))
        res = SUCCESS
    else:
        print("Object %s is not with robot %s\n" %(o,r))
        res = FAILURE
    return res

def perceive(l, state):
    if state.view[l] == False:
        for c in state.containers[l]:
            state.pos[c] = l
        state.view[l] = True
        print("Perceived location %d" %l)
    else:
        print("Already perceived\n")
    return SUCCESS

def addressEmergency(r, l, i, state):
    if state.loc[r] == l:
        print("Robot %s has addressed emergency %d" %(r, i))
        res = SUCCESS
    else:
        print("Robot %s has failed to address emergency %d" %(r, i))
        res = FAILURE
    return res

def Search(r, o, state):
    if state.pos[o] == UNK:
        for l in LOCATIONS:
            if state.view[l] == False:
                moveTo(r, l, state)
                perceive(l, state)
                if state.pos[o] == l:
                    take(r, o, l, state)
                    break
        res = SUCCESS
    else:
        print("Failed to search %s" %o)
        res = FAILURE
    return res

def Fetch(r, o, state):
    if state.pos[o] == UNK:
        Search(r, o, state)
    elif state.loc[r] == state.pos[o]:
        take(r, o, state.pos[o], state)
    else:
        moveTo(r, state.pos[o], state)
        take(r, o, state.pos[o], state)
    return SUCCESS

def Emergency(r, l, i, state):
    if state.emergencyHandling[r] == False:
        state.emergencyHandling[r] = True
        if state.load[r] != NIL:
            put(r, state.load[r], state.loc[r], state)
            moveTo(r, l, state)
            addressEmergency(r, l, i, state)
            res = SUCCESS
    else:
        print("%r is already busy handling another emergency\n" %r)
        res = FAILURE
    return res

def Harbour1():
    state = rae1.State()
    state.loc = {'r1' : 1}
    state.pos = {'o1' : UNK}
    state.load = {'r1' : NIL}
    state.view = {}
    state.containers = {1:[], 2:[], 3:[], 4:[], 5:['o1'], 6:[]}

    for l in LOCATIONS:
        state.view[l] = False
    state.emergencyHandling = {'r1' : False}

    Fetch('r1', 'o1', state)
    Emergency('r1', 2, 1, state)
    Fetch('r1', 'o1', state)