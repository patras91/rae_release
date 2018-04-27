__author__ = 'patras'

from domain_constants import *
import ape
import gui
from timer import globalTimer

'''A spring door closes automatically when not held. There are two robots
to carry objects and open doors. Each robot has only one arm with which it can
either hold the door or carry the object. The goal for the main robot is to find
an object and bring it to the hallway.'''

def SD_GETDOOR(l1, l2):
    if (l1, l2) in rv.DOORLOCATIONS:
        return rv.DOORLOCATIONS[l1, l2]
    else:
        return rv.DOORLOCATIONS[l2, l1]

# Using Dijsktra's algorithm
def SD_GETPATH(l0, l1):
    visitedDistances = {l0: 0}
    locs = list(rv.LOCATIONS)
    path = {}

    while locs:
        min_loc = None
        for loc in locs:
            if loc in visitedDistances:
                if min_loc is None:
                    min_loc = loc
                elif visitedDistances[loc] < visitedDistances[min_loc]:
                    min_loc = loc

        if min_loc is None:
            break

        locs.remove(min_loc)
        current_dist = visitedDistances[min_loc]

        for l in rv.EDGES[min_loc]:
            dist = current_dist + 1
            if l not in visitedDistances or dist < visitedDistances[l]:
                visitedDistances[l] = dist
                path[l] = min_loc

    l = l1
    path2 = {}
    while l != l0:
        path2[path[l]] = l
        l = path[l]

    return path2
#****************************************************************

def openDoor(r, d):
    ape.state.load.AcquireLock(r)
    ape.state.doorStatus.AcquireLock(d)
    if ape.state.doorStatus[d] == 'opened':
        gui.Simulate("Door %s is already open\n" %d)
        res = SUCCESS
    elif ape.state.load[r] == NIL and (ape.state.doorStatus[d] == 'closed' or ape.state.doorStatus[d] == 'closing'):
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('openDoor', start) == False):
	        pass
        gui.Simulate("Robot %s has opened door %s\n" %(r, d))
        ape.state.doorStatus[d] = 'opened'
        res = SUCCESS
    else:
        gui.Simulate("Robot %s is not free to open door %s or the door is not closed\n" %(r, d))
        res = FAILURE
    ape.state.load.ReleaseLock(r)
    ape.state.doorStatus.ReleaseLock(d)
    return res

ape.declare_prob(openDoor, [0.8, 0.2])
def openDoor_Sim(r, d, outcome):
    if outcome == 0:
        ape.state.doorStatus[d] = 'opened'
        res = SUCCESS
    else:
        res = FAILURE
    return res

def passDoor(r, d, l):
    ape.state.doorStatus.AcquireLock(d)
    ape.state.loc.AcquireLock(r)
    if ape.state.doorStatus[d] == 'opened' or ape.state.doorStatus[d] == 'held':
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('passDoor', start) == False):
	        pass
        gui.Simulate("Robot %s has passed the door %s\n" %(r, d))
        ape.state.loc[r] = l
        res = SUCCESS
    else:
        gui.Simulate("Robot %s is not able to pass door %s\n" %(r, d))
        res = FAILURE
    ape.state.loc.ReleaseLock(r)
    ape.state.doorStatus.ReleaseLock(d)
    return res

ape.declare_prob(passDoor, [0.8, 0.2])
def passDoor_Sim(r, d, l, outcome):
    if outcome == 0:
        ape.state.loc[r] = l
        res = SUCCESS
    else:
        res = FAILURE
    return res

def holdDoor(r, d):
    ape.state.doorStatus.AcquireLock(d)
    ape.state.load.AcquireLock(r)
    if (ape.state.doorStatus[d] == 'opened' or ape.state.doorStatus[d] == 'closing' or ape.state.doorStatus[d] == 'held') and ape.state.load[r] == NIL:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('holdDoor', start) == False):
	        pass
        gui.Simulate("Robot %s is holding the door %s\n" %(r, d))
        ape.state.load[r] = 'H'
        ape.state.doorStatus[d] = 'held'
        res = SUCCESS
    elif ape.state.doorStatus[d] == 'closed':
        gui.Simulate("Door %s is closed and cannot be held by %s\n" %(d, r))
        res = FAILURE
    elif ape.state.load[r] != NIL:
        gui.Simulate("Robot %s is not free to hold the door %s\n" %(r, d))
        res = FAILURE
    ape.state.doorStatus.ReleaseLock(d)
    ape.state.load.ReleaseLock(r)
    return res

ape.declare_prob(holdDoor, [0.8, 0.2])
def holdDoor_Sim(r, d, outcome):
    if outcome == 0:
        ape.state.load[r] = 'H'
        ape.state.doorStatus[d] = 'held'
        res = SUCCESS
    else:
        res = FAILURE
    return res

def releaseDoor(r, d):
    if ape.state.doorStatus[d] == 'held' and ape.state.load[r] == 'H':
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('releaseDoor', start) == False):
	        pass
        gui.Simulate("Robot %s has released the the door %s\n" %(r, d))
        ape.state.doorStatus[d] = 'closing'
        ape.state.load[r] = NIL
    else:
        gui.Simulate("Robot %s is not holding door %s\n" %(r, d))
    return SUCCESS

ape.declare_prob(releaseDoor, [1])
def releaseDoor_Sim(r, d, outcome):
    if ape.state.doorStatus[d] == 'held' and ape.state.load[r] == 'H':
        ape.state.doorStatus[d] = 'closing'
        ape.state.load[r] = NIL
    return SUCCESS

def move(r, l1, l2):
    ape.state.loc.AcquireLock(r)
    if l1 == l2:
        gui.Simulate("Robot %s is already at location %s\n" %(r, l2))
        res = SUCCESS
    elif ape.state.loc[r] == l1:
        if (l1, l2) in rv.DOORLOCATIONS or (l2, l1) in rv.DOORLOCATIONS:
            gui.Simulate("Robot %s cannot move. There is a spring door between %s and %s \n" %(r, l1, l2))
            res = FAILURE
        else:
            start = globalTimer.GetTime()
            while(globalTimer.IsCommandExecutionOver('move', start) == False):
                pass
            gui.Simulate("Robot %s has moved from %d to %d\n" %(r, l1, l2))
            ape.state.loc[r] = l2
            res = SUCCESS
    else:
        gui.Simulate("Invalid move by robot %s\n" %r)
        res = FAILURE
    ape.state.loc.ReleaseLock(r)
    return res

ape.declare_prob(move, [0.8, 0.2])
def move_Sim(r, l1, l2, outcome):
    if outcome == 0:
        ape.state.loc[r] = l2
        res = SUCCESS
    else:
        res = FAILURE
    return res

def put(r, o):
    ape.state.pos.AcquireLock(o)
    ape.state.load.AcquireLock(r)
    ape.state.loc.AcquireLock(r)
    if ape.state.pos[o] == r:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('put', start) == False):
	        pass
        ape.state.pos[o] = ape.state.loc[r]
        ape.state.load[r] = NIL
        gui.Simulate("Robot %s has put object %s at location %d\n" %(r,o,ape.state.loc[r]))
        res = SUCCESS
    else:
        gui.Simulate("Object %s is not with robot %s\n" %(o,r))
        res = FAILURE
    ape.state.pos.ReleaseLock(o)
    ape.state.load.ReleaseLock(r)
    ape.state.loc.ReleaseLock(r)
    return res

ape.declare_prob(put, [0.9, 0.1])
def put_Sim(r, o, outcome):
    if outcome == 0:
        ape.state.pos[o] = ape.state.loc[r]
        ape.state.load[r] = NIL
        res = SUCCESS
    else:
        res = FAILURE
    return res

def take(r, o):
    ape.state.pos.AcquireLock(o)
    ape.state.load.AcquireLock(r)
    ape.state.loc.AcquireLock(r)
    if ape.state.load[r] == NIL:
        if ape.state.loc[r] == ape.state.pos[o]:
            start = globalTimer.GetTime()
            while(globalTimer.IsCommandExecutionOver('take', start) == False):
	            pass
            gui.Simulate("Robot %s has picked up object %s\n" %(r, o))
            ape.state.pos[o] = r
            ape.state.load[r] = o
            res = SUCCESS
        elif ape.state.loc[r] != ape.state.pos[o]:
            gui.Simulate("Robot %s is not at object %s's location\n" %(r, o))
            res = FAILURE
    else:
        gui.Simulate("Robot %s is not free to take anything\n" %r)
        res = FAILURE
    ape.state.pos.ReleaseLock(o)
    ape.state.load.ReleaseLock(r)
    ape.state.loc.ReleaseLock(r)
    return res

ape.declare_prob(take, [0.9, 0.1])
def take_Sim(r, o, outcome):
    if outcome == 0:
        ape.state.pos[o] = r
        ape.state.load[r] = o
        res = SUCCESS
    else:
        res = FAILURE
    return res

def closeDoors():
    while(ape.state.done[0] == False):
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('closeDoors', start) == False):
            pass

        for d in rv.DOORS:
            ape.state.doorStatus.AcquireLock(d)
            if ape.state.doorStatus[d] == 'opened':
                ape.state.doorStatus[d] = 'closing'
                gui.Simulate("Door %s is closing\n" %d)
            elif ape.state.doorStatus[d] == 'closing' or ape.state.doorStatus[d] == 'closed':
                ape.state.doorStatus[d] = 'closed'
                gui.Simulate("Door %s is closed\n" %d)
            elif ape.state.doorStatus[d] == 'held':
                gui.Simulate("Door %s is %s, so it cannot be closed\n" %(d, ape.state.doorStatus[d]))
            ape.state.doorStatus.ReleaseLock(d)
    return SUCCESS

ape.declare_prob(closeDoors, [1])
def closeDoors_Sim(outcome):
    while(ape.state.done[0] == False):
        for d in rv.DOORS:
            if ape.state.doorStatus[d] == 'opened':
                ape.state.doorStatus[d] = 'closing'
            elif ape.state.doorStatus[d] == 'closing' or ape.state.doorStatus[d] == 'closed':
                ape.state.doorStatus[d] = 'closed'
    return SUCCESS

def MoveThroughDoorway_Method3(r, d, l):
    if ape.state.load[r] == NIL:
        ape.do_command(openDoor, r, d)
        ape.do_command(holdDoor, r, d)
        ape.do_command(passDoor, r, d, l)
        ape.do_command(releaseDoor, r, d)
        res = SUCCESS
    else:
        res = FAILURE
    return res

def Restore(r, loc, cargo):
    ape.do_task('moveTo', r, loc)
    if cargo != NIL:
        ape.do_command(take, r, cargo)

def MoveThroughDoorway_Method2(r, d, l):
    if ape.state.load[r] != NIL:
         params = GetHelp_Method1(r)
         if params == FAILURE:
             res = FAILURE
         else:
            r2, l2, cargo = params
            ape.do_command(openDoor, r2, d)
            ape.do_command(holdDoor, r2, d)
            ape.do_command(passDoor, r, d, l)
            ape.do_command(releaseDoor, r2, d)
            Restore(r2, l2, cargo)
            res = SUCCESS
    else:
        res = FAILURE
    return res

def MoveThroughDoorway_Method4(r, d, l):
    if ape.state.load[r] != NIL:
        obj = ape.state.load[r]
        if obj != 'H':
            ape.do_command(put, r, obj)
        else:
            gui.Simulate("%r is holding another door\n" %r)
            return FAILURE
        ape.do_command(openDoor, r, d)
        ape.do_command(take, r, obj)
        ape.do_command(passDoor, r, d, l)
        res = SUCCESS
    else:
        res = FAILURE
    return res

def MoveThroughDoorway_Method1(r, d, l):
    if ape.state.load[r] == NIL:
        ape.do_command(openDoor, r, d)
        ape.do_command(passDoor, r, d, l)
        res = SUCCESS
    else:
        res = FAILURE
    return res

def MoveTo_Method1(r, l):
    res = SUCCESS
    x = ape.state.loc[r]
    path = SD_GETPATH(x, l)
    if path == {}:
        gui.Simulate("Robot %s is already at location %s \n" %(r, l))
    else:
        lTemp = x
        lNext = path[lTemp]
        while(lTemp != l):
            lNext = path[lTemp]
            if (lTemp, lNext) in rv.DOORLOCATIONS or (lNext, lTemp) in rv.DOORLOCATIONS:
                d = SD_GETDOOR(lTemp, lNext)
                ape.do_task('moveThroughDoorway', r, d, lNext)
            else:
                ape.do_command(move, r, lTemp, lNext)
            if lNext != ape.state.loc[r]:
                res = FAILURE
                break
            else:
                lTemp = lNext
    return res

def GetHelp_Method1(r):
    if r == rv.ROBOTS[0]:
        r2 = rv.ROBOTS[1]
    else:
        r2 = rv.ROBOTS[0]

    for robo in rv.ROBOTS:
        if ape.state.load[robo] == NIL and robo != r:
            r2 = robo

    load_r = ape.state.load[r2]
    loc_r2 = ape.state.loc[r2]
    if load_r != NIL:
        if load_r != 'H':
            ape.do_command(put, r2, load_r)
        else:
            gui.Simulate("%s is holding another door\n" %r)
            return FAILURE
    ape.do_task('moveTo', r2, ape.state.loc[r])
    return r2, loc_r2, load_r

def Fetch_Method1(r, o, l):
    ape.do_task('moveTo', r, ape.state.pos[o])
    load_r = ape.state.load[r]
    if load_r != NIL:
        if load_r != 'H':
            ape.do_command(put, r, load_r)
        else:
            gui.Simulate("%s is holding another door\n" %r)
            return FAILURE
    ape.do_command(take, r, o)
    ape.do_task('moveTo', r, l)
    #ape.state.done[0] = True
    return SUCCESS

#def CloseDoors_Method1():
#    while ape.state.done == False:
#        ape.do_command(closeDoors)
#    return SUCCESS

rv = RV()
ape.declare_commands([openDoor, holdDoor, passDoor, releaseDoor, move, put, take],
                      [openDoor_Sim, holdDoor_Sim, passDoor_Sim, releaseDoor_Sim, move_Sim, put_Sim, take_Sim])

ape.declare_methods('fetch', Fetch_Method1)
ape.declare_methods('getHelp', GetHelp_Method1)
ape.declare_methods('moveTo', MoveTo_Method1)
ape.declare_methods('moveThroughDoorway', MoveThroughDoorway_Method1, MoveThroughDoorway_Method3, MoveThroughDoorway_Method4, MoveThroughDoorway_Method2)
#ape.declare_methods('closeDoors', CloseDoors_Method1)
