__author__ = 'patras'

'''A robot is searching for an object in the environment consisting of n locations.
It has a battery that needs to be recharged after some moves.
A move consumes 1/4 of the battery capacity.
Recharger is only at one location'''

from domain_constants import *
import rae1

def take(r, o, state):
    if state.load[r] == NIL:
        if state.loc[r] == state.pos[o]:
            print("Robot %s has picked up object %d" %(r, o))
            state.pos[o] = r
            state.load[r] = o
            res = SUCCESS
        elif state.loc[r] != state.pos[o]:
            print("Robot %s is not at object %s's location\n" %(r, o))
            res = FAILURE
    else:
        print("Robot %s is not free to take anything\n" %r)
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

def charge(r, c, state):
    if state.loc[r] == state.pos[c] or state.pos[c] == r:
        state.charge[r] = 4
        print("Robot %s is fully charged\n" %r)
        res = SUCCESS
    else:
        print("Robot %s is not in the charger's location or it doesn't have the charger with it\n" %r)
        res = FAILURE
    return res

def move(r, l1, l2, dist, state):
    if l1 == l2:
        print("Robot %s is already at location %s\n" %(r, l2))
        res = SUCCESS
    elif state.loc[r] == l1 and state.charge[r] >= dist:
        print("Robot has moved from %d to %d\n" %(l1, l2))
        state.loc[r] = l2
        state.charge[r] = state.charge[r] - dist
        res = SUCCESS
    elif state.loc[r] != l1 and state.charge[r] >= dist:
        print("Robot %s is not in location %d\n" %(r, l1))
        res = FAILURE
    elif state.loc[r] == l1 and state.charge[r] < dist:
        print("Robot %s does not have enough charge to move :(\n" %r)
        state.charge[r] = 0 # should we do this?
        res = FAILURE
    else:
        print("Robot %s is not at location %s and it doesn't have enough charge!\n" %(r, l1))
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

def MoveTo_Method1(r, l, state):
    dist = GETDISTANCE(state.loc[r], l)
    if state.charge[r] >= dist:
        move(r, state.loc[r], l, dist, state)
        res = SUCCESS
    else:
        print("Insufficient charge! only %.2f%%. Robot %s cannot move\n" %(state.charge[r] * 100 / 4, r))
        res = FAILURE
    return res

def Recharge_Method1(r, c, state):
    if state.loc[r] != state.pos[c] and state.pos[c] != r:
        MoveTo_Method1(r, state.pos[c], state)
    charge(r, c, state)
    return SUCCESS

def Recharge_Method2(r, c, state):
    if state.loc[r] != state.pos[c] and state.pos[c] != r:
        MoveTo_Method1(r, state.pos[c], state)

    charge(r, c, state)
    take(r, c, state)
    return SUCCESS

def Search_Method1(r, o, state):
    if state.pos[o] == UNK:
        toBePerceived = NIL
        for l in LOCATIONS_CHARGEABLEROBOT:
            if state.view[l] == False:
                toBePerceived = l
                break

        if toBePerceived != NIL:
            MoveTo_Method1(r, toBePerceived, state)
            perceive(toBePerceived, state)
            if state.pos[o] == toBePerceived:
                if state.load[r] != NIL:
                    put(r, o, state)
                take(r, o, state)
            else:
                Search_Method2(r, o, state)
            res = SUCCESS
        else:
            print("Failed to search %s" %o)
            res = FAILURE
    else:
        print("Not using appropriate method for Search\n")
        res = FAILURE
    return res

def Search_Method2(r, o, state):
    if state.pos[o] == UNK:
        toBePerceived = NIL
        for l in LOCATIONS_CHARGEABLEROBOT:
            if state.view[l] == False:
                toBePerceived = l
                break

        if toBePerceived != NIL:
            Recharge_Method1(r, 'c1', state) # is this allowed?
            MoveTo_Method1(r, toBePerceived, state)
            perceive(toBePerceived, state)
            if state.pos[o] == toBePerceived:
                if state.load[r] != NIL:
                    put(r, o, state)
                take(r, o, state)
            else:
                Search_Method1(r, o, state)
            res = SUCCESS
        else:
            print("Failed to search %s" %o)
            res = FAILURE
    else:
        print("Not using appropriate method for Search\n")
        res = FAILURE
    return res

def Fetch_Method1(r, o, state):
    if state.pos[o] == UNK:
        Search_Method1(r, o, state)
    elif state.loc[r] == state.pos[o]:
        take(r, o, state.pos[o], state)
    else:
        MoveTo_Method1(r, state.pos[o], state)
        take(r, o, state.pos[o], state)
    return SUCCESS

def Fetch_Method2(r, o, state):
    if state.pos[o] == UNK:
        Search_Method1(r, o, state)
    elif state.loc[r] == state.pos[o]:
        take(r, o, state.pos[o], state)
    else:
        Recharge_Method1(r, 'c1', state)
        MoveTo_Method1(r, state.pos[o], state)
        take(r, o, state.pos[o], state)
    return SUCCESS

def RunChargeableRobot1():
    state = rae1.State()
    state.loc = {'r1': 1}
    state.charge = {'r1':4}
    state.load = {'r1': NIL}
    state.pos = {'c1': 7, 'o1': UNK}
    state.containers = {1:[], 2:[], 3:[], 4:[], 5:['o1'], 6:[], 7:[], 8:[]}

    state.view = {}
    for l in LOCATIONS_CHARGEABLEROBOT:
        state.view[l] = False

    #Fetch_Method1('r1', 'o1', state)
    Fetch_Method2('r1', 'o1', state)