__author__ = 'patras'

from domain_constants import *
import rae1

'''A spring door closes automatically when not held. There are two robots
to carry objects and open doors. Each robot has only one arm with which it can
either hold the door or carry the object. The goal for the main robot is to find
an object and bring it to the hallway.'''

def openDoor(r, d, state):
    if state.load[r] == NIL:
        print("Robot %s has opened door %s\n" %(r, d))
        state.doorStatus[d] = 'opened'
        res = SUCCESS
    else:
        print("Robot %s is not free to open door %s\n" %(r, d))
        res = FAILURE
    return res

def passDoor(r, d, l, state):
    if state.doorStatus[d] == 'held':
        print("Robot %s has passed the door %s\n" %(r, d))
        state.loc[r] = l
        res = SUCCESS
    else:
        print("Robot %s is not able to pass door %s\n" %(r, d))
        res = FAILURE
    return res

def holdDoor(r, d, state):
    if state.doorStatus[d] == 'opened' and state.load[r] == NIL:
        print("Robot %s is holding the door %s\n" %(r, d))
        state.load[r] = 'H'
        state.doorStatus[d] = 'held'
        res = SUCCESS
    elif state.doorStatus[d] == 'closed':
        print("Door %s is closed and cannot be held by %s\n" %(d, r))
        res = FAILURE
    elif state.load[r] != NIL:
        print("Robot %s is not free to hold the door %s\n" %(r, d))
        res = FAILURE
    return res

def releaseDoor(r, d, state):
    if state.doorStatus[d] == 'held' and state.load[r] == 'H':
        print("Robot %s has released the the door %s\n" %(r, d))
        state.doorStatus[d] = 'closed'
        state.load[r] = NIL
    else:
        print("Robot %s is not holding door %s\n" %(r, d))
    return SUCCESS

def move(r, l1, l2, state):
    if l1 == l2:
        print("Robot %s is already at location %s\n" %(r, l2))
        res = SUCCESS
    elif state.loc[r] == l1:
        if (l1, l2) in DOORLOCATIONS_SPRINGDOOR or (l2, l1) in DOORLOCATIONS_SPRINGDOOR:
            print("Robot %s cannot move. There is a spring door between %s and %s \n" %(r, l1, l2))
            res = FAILURE
        else:
            print("Robot %s has moved from %d to %d\n" %(r, l1, l2))
            state.loc[r] = l2
            res = SUCCESS
    else:
        print("Invalid move by robot %s\n" %r)
        res = FAILURE
    return res

def put(r, o, state):
    if state.pos[o] == r:
        state.pos[o] = state.loc[r]
        state.load[r] = NIL
        print("Robot %s has put object %s at location %d\n" %(r,o,state.loc[r]))
        res = SUCCESS
    else:
        print("Object %s is not with robot %s\n" %(o,r))
        res = FAILURE
    return res

def take(r, o, state):
    if state.load[r] == NIL:
        if state.loc[r] == state.pos[o]:
            print("Robot %s has picked up object %s" %(r, o))
            state.pos[o] = r
            state.load[r] = o
            res = SUCCESS
        elif state.loc[r] != state.pos[o]:
            print("Robot %s is not at object %s's location\n" %(r, o))
            res = FAILURE
    else:
        print("Robot %s is not free to take anything\n" %r)
    return res

def MoveThroughDoorway_Method1(r, d, l, state):
    if state.load[r] == NIL:
        openDoor(r, d, state)
        holdDoor(r, d, state)
        passDoor(r, d, l, state)
        releaseDoor(r, d, state)
        res = SUCCESS
    else:
        res = FAILURE
    return res

def MoveThroughDoorway_Method2(r, d, l, state):
    if state.load[r] != NIL:
        GetHelp_Method1(r, state)
        openDoor('r2', d, state)
        holdDoor('r2', d, state)
        passDoor(r, d, l, state)
        releaseDoor('r2', d, state)
        res = SUCCESS
    else:
        res = FAILURE
    return res

def MoveTo_Method1(r, l, state):
    res = SUCCESS

    path = GETPATH_SPRINGDOOR(state.loc[r], l)
    lTemp = state.loc[r]
    lNext = path[lTemp]
    while(lTemp != l):
        lNext = path[lTemp]
        if (lTemp, lNext) in DOORLOCATIONS_SPRINGDOOR or (lNext, lTemp) in DOORLOCATIONS_SPRINGDOOR:
            d = GETDOOR_SPRINGDOOR(lTemp, lNext)
            MoveThroughDoorway_Method1(r, d, lNext, state)
        else:
            move(r, lTemp, lNext, state)
        if lTemp == state.loc[r]:
            print("MoveTo method has failed\n")
            res = FAILURE
            break
        else:
            lTemp = state.loc[r]

    return res

def GetHelp_Method1(r, state):
    if state.load['r2'] != NIL:
        put('r2', state.load['r2'], state)
    MoveTo_Method1('r2', state.loc[r], state)
    return SUCCESS

def Fetch_Method1(r, o, l, state):
    MoveTo_Method1(r, state.pos[o], state)
    if state.load[r] != NIL:
        put(r, o, state)
    take(r, o, state)
    MoveTo_Method1(r, l, state)

def RunSpringDoor1():
    state = rae1.State()
    state.load = {}
    state.load['r1'] = NIL
    state.doorStatus = {'d1': 'closed', 'd2': 'closed', 'd3': 'closed' }
    state.loc = {'r1': 1, 'r2': 2}
    state.pos = {'o1': 3}

    Fetch_Method1('r1', 'o1', 5, state)