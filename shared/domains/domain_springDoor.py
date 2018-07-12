__author__ = 'patras'

from domain_constants import *
import importlib
loader = importlib.find_loader('RAE1_and_RAEplan')
if loader is not None:
    import RAE1_and_RAEplan as ape
else:
    import ape1_and_apeplan as ape

from state import state
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
    state.load.AcquireLock(r)
    state.doorStatus.AcquireLock(d)
    if state.doorStatus[d] == 'opened':
        gui.Simulate("Door %s is already open\n" %d)
        res = SUCCESS
    elif state.load[r] == NIL and (state.doorStatus[d] == 'closed' or state.doorStatus[d] == 'closing'):
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('openDoor', start) == False):
	        pass
        gui.Simulate("Robot %s has opened door %s\n" %(r, d))
        state.doorStatus[d] = 'opened'
        res = SUCCESS
    else:
        gui.Simulate("Robot %s is not free to open door %s or the door is not closed\n" %(r, d))
        res = FAILURE
    state.load.ReleaseLock(r)
    state.doorStatus.ReleaseLock(d)
    return res

def GetProbability_openDoor(r, d):
    if state.doorStatus[d] == 'opened':
        return [1, 0]
    elif state.load[r] == NIL and (state.doorStatus[d] == 'closed' or state.doorStatus[d] == 'closing'):
        return [0.8, 0.2]
    else:
        return [0.1, 0.9]


def openDoor_Sim(r, d, outcome):
    if outcome == 0:
        state.doorStatus[d] = 'opened'
        res = SUCCESS
    else:
        res = FAILURE
    return res

def passDoor(r, d, l):
    state.doorStatus.AcquireLock(d)
    state.loc.AcquireLock(r)
    if state.doorStatus[d] == 'opened' or state.doorStatus[d] == 'held':
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('passDoor', start) == False):
	        pass
        gui.Simulate("Robot %s has passed the door %s\n" %(r, d))
        state.loc[r] = l
        res = SUCCESS
    else:
        gui.Simulate("Robot %s is not able to pass door %s\n" %(r, d))
        res = FAILURE
    state.loc.ReleaseLock(r)
    state.doorStatus.ReleaseLock(d)
    return res

def GetProbability_passDoor(r, d, l):
    if state.doorStatus[d] == 'opened' or state.doorStatus[d] == 'held':
        return [0.8, 0.2]
    else:
        return [0.1, 0.9]

def passDoor_Sim(r, d, l, outcome):
    if outcome == 0:
        state.loc[r] = l
        res = SUCCESS
    else:
        res = FAILURE
    return res

def holdDoor(r, d):
    state.doorStatus.AcquireLock(d)
    state.load.AcquireLock(r)
    if (state.doorStatus[d] == 'opened' or state.doorStatus[d] == 'closing' or state.doorStatus[d] == 'held') and state.load[r] == NIL:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('holdDoor', start) == False):
	        pass
        gui.Simulate("Robot %s is holding the door %s\n" %(r, d))
        state.load[r] = 'H'
        state.doorStatus[d] = 'held'
        res = SUCCESS
    elif state.doorStatus[d] == 'closed':
        gui.Simulate("Door %s is closed and cannot be held by %s\n" %(d, r))
        res = FAILURE
    elif state.load[r] != NIL:
        gui.Simulate("Robot %s is not free to hold the door %s\n" %(r, d))
        res = FAILURE
    state.doorStatus.ReleaseLock(d)
    state.load.ReleaseLock(r)
    return res

def GetProbability_holdDoor(r, d):
    if (state.doorStatus[d] == 'opened' or state.doorStatus[d] == 'closing' or state.doorStatus[d] == 'held') and state.load[r] == NIL:
        return [0.8, 0.2]
    elif state.doorStatus[d] == 'closed':
        return [0.1, 0.9]
    elif state.load[r] != NIL:
        return [0.1, 0.9]

def holdDoor_Sim(r, d, outcome):
    if outcome == 0:
        state.load[r] = 'H'
        state.doorStatus[d] = 'held'
        res = SUCCESS
    else:
        res = FAILURE
    return res

def releaseDoor(r, d):
    if state.doorStatus[d] == 'held' and state.load[r] == 'H':
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('releaseDoor', start) == False):
	        pass
        gui.Simulate("Robot %s has released the the door %s\n" %(r, d))
        state.doorStatus[d] = 'closing'
        state.load[r] = NIL
    else:
        gui.Simulate("Robot %s is not holding door %s\n" %(r, d))
    return SUCCESS

def GetProbability_releaseDoor(r, d):
    return [1]

def releaseDoor_Sim(r, d, outcome):
    if state.doorStatus[d] == 'held' and state.load[r] == 'H':
        state.doorStatus[d] = 'closing'
        state.load[r] = NIL
    return SUCCESS

def move(r, l1, l2):
    state.loc.AcquireLock(r)
    if l1 == l2:
        gui.Simulate("Robot %s is already at location %s\n" %(r, l2))
        res = SUCCESS
    elif state.loc[r] == l1:
        if (l1, l2) in rv.DOORLOCATIONS or (l2, l1) in rv.DOORLOCATIONS:
            gui.Simulate("Robot %s cannot move. There is a spring door between %s and %s \n" %(r, l1, l2))
            res = FAILURE
        else:
            start = globalTimer.GetTime()
            while(globalTimer.IsCommandExecutionOver('move', start) == False):
                pass
            gui.Simulate("Robot %s has moved from %d to %d\n" %(r, l1, l2))
            state.loc[r] = l2
            res = SUCCESS
    else:
        gui.Simulate("Invalid move by robot %s\n" %r)
        res = FAILURE
    state.loc.ReleaseLock(r)
    return res

def GetProbability_move(r, l1, l2):
    if l1 == l2:
        return [0.9, 0.1]
    elif state.loc[r] == l1:
        if (l1, l2) in rv.DOORLOCATIONS or (l2, l1) in rv.DOORLOCATIONS:
            return [0.3, 0.7]
        else:
            return [0.9, 0.1]
    else:
        return [0.1, 0.9]

def move_Sim(r, l1, l2, outcome):
    if outcome == 0:
        state.loc[r] = l2
        res = SUCCESS
    else:
        res = FAILURE
    return res

def put(r, o):
    state.pos.AcquireLock(o)
    state.load.AcquireLock(r)
    state.loc.AcquireLock(r)
    if state.pos[o] == r:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('put', start) == False):
	        pass
        state.pos[o] = state.loc[r]
        state.load[r] = NIL
        gui.Simulate("Robot %s has put object %s at location %d\n" %(r,o,state.loc[r]))
        res = SUCCESS
    else:
        gui.Simulate("Object %s is not with robot %s\n" %(o,r))
        res = FAILURE
    state.pos.ReleaseLock(o)
    state.load.ReleaseLock(r)
    state.loc.ReleaseLock(r)
    return res

def GetProbability_put(r, o):
    if state.pos[o] == r:
        return [0.9, 0.1]
    else:
        return [0.4, 0.6]

def put_Sim(r, o, outcome):
    if outcome == 0:
        state.pos[o] = state.loc[r]
        state.load[r] = NIL
        res = SUCCESS
    else:
        res = FAILURE
    return res

def take(r, o):
    state.pos.AcquireLock(o)
    state.load.AcquireLock(r)
    state.loc.AcquireLock(r)
    if state.load[r] == NIL:
        if state.loc[r] == state.pos[o]:
            start = globalTimer.GetTime()
            while(globalTimer.IsCommandExecutionOver('take', start) == False):
	            pass
            gui.Simulate("Robot %s has picked up object %s\n" %(r, o))
            state.pos[o] = r
            state.load[r] = o
            res = SUCCESS
        elif state.loc[r] != state.pos[o]:
            gui.Simulate("Robot %s is not at object %s's location\n" %(r, o))
            res = FAILURE
    else:
        gui.Simulate("Robot %s is not free to take anything\n" %r)
        res = FAILURE
    state.pos.ReleaseLock(o)
    state.load.ReleaseLock(r)
    state.loc.ReleaseLock(r)
    return res

def GetProbability_take(r, o):
    if state.load[r] == NIL:
        if state.loc[r] == state.pos[o]:
            return [0.9, 0.1]
        elif state.loc[r] != state.pos[o]:
            return [0.1, 0.9]
    else:
        return [0.1, 0.9]

def take_Sim(r, o, outcome):
    if outcome == 0:
        state.pos[o] = r
        state.load[r] = o
        res = SUCCESS
    else:
        res = FAILURE
    return res

def closeDoors():
    while(state.done[0] == False):
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('closeDoors', start) == False):
            pass

        for d in rv.DOORS:
            state.doorStatus.AcquireLock(d)
            if state.doorStatus[d] == 'opened':
                state.doorStatus[d] = 'closing'
                gui.Simulate("Door %s is closing\n" %d)
            elif state.doorStatus[d] == 'closing' or state.doorStatus[d] == 'closed':
                state.doorStatus[d] = 'closed'
                gui.Simulate("Door %s is closed\n" %d)
            elif state.doorStatus[d] == 'held':
                gui.Simulate("Door %s is %s, so it cannot be closed\n" %(d, state.doorStatus[d]))
            state.doorStatus.ReleaseLock(d)
    return SUCCESS

def GetProbability_closeDoors():
    return [1]

def closeDoors_Sim(outcome):
    while(state.done[0] == False):
        for d in rv.DOORS:
            if state.doorStatus[d] == 'opened':
                state.doorStatus[d] = 'closing'
            elif state.doorStatus[d] == 'closing' or state.doorStatus[d] == 'closed':
                state.doorStatus[d] = 'closed'
    return SUCCESS

def MoveThroughDoorway_Method3(r, d, l):
    if state.load[r] == NIL:
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
    if state.load[r] != NIL:
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
    if state.load[r] != NIL:
        obj = state.load[r]
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
    if state.load[r] == NIL:
        ape.do_command(openDoor, r, d)
        ape.do_command(passDoor, r, d, l)
        res = SUCCESS
    else:
        res = FAILURE
    return res

def MoveTo_Method1(r, l):
    res = SUCCESS
    x = state.loc[r]
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
            if lNext != state.loc[r]:
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
        if state.load[robo] == NIL and robo != r:
            r2 = robo

    load_r2 = state.load[r2]
    loc_r2 = state.loc[r2]
    if load_r2 != NIL:
        if load_r2 != 'H':
            ape.do_command(put, r2, load_r2)
        else:
            gui.Simulate("%s is holding another door\n" %r2)
            return FAILURE
    ape.do_task('moveTo', r2, state.loc[r])
    return r2, loc_r2, load_r2

def Fetch_Method1(r, o, l):
    ape.do_task('moveTo', r, state.pos[o])
    load_r = state.load[r]
    if load_r != NIL:
        if load_r != 'H':
            ape.do_command(put, r, load_r)
        else:
            gui.Simulate("%s is holding another door\n" %r)
            return FAILURE
    ape.do_command(take, r, o)
    ape.do_task('moveTo', r, l)
    #state.done[0] = True
    return SUCCESS

def Recover_Method1(r):
    o = state.load[r]
    if o != NIL and state.pos[o] == UNK:
        ape.do_command(senseLoc, o)
        if state.pos[o] == state.loc[r]:
            state.do_command(take, r, o)
        else:
            state.do_task('moveTo', r, state.pos[o])
            state.do_command(take, r, o)
        return SUCCESS
    else:
        return FAILURE

def Recover_Method2(r):
    state.do_command(senseStatus, r)
    if state.robotStatus[r] == 'broken':
        state.do_command(repair, r)
    return SUCCESS

#def CloseDoors_Method1():
#    while state.done == False:
#        ape.do_command(closeDoors)
#    return SUCCESS


rv = RV()
ape.declare_commands([
    openDoor, 
    holdDoor, 
    passDoor, 
    releaseDoor, 
    move, 
    put, 
    take],)

ape.declare_methods('fetch', Fetch_Method1)
ape.declare_methods('getHelp', GetHelp_Method1)
ape.declare_methods('moveTo', MoveTo_Method1)
ape.declare_methods('moveThroughDoorway',
    MoveThroughDoorway_Method1,
    MoveThroughDoorway_Method3,
    MoveThroughDoorway_Method4,
    MoveThroughDoorway_Method2)

#events
ape.declare_methods('collide', Recover_Method1, Recover_Method2)

#ape.declare_methods('closeDoors', CloseDoors_Method1)


