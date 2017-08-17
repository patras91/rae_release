__author__ = 'patras'

from domain_constants import *
import rae1
import gui
from timer import globalTimer

'''A spring door closes automatically when not held. There are two robots
to carry objects and open doors. Each robot has only one arm with which it can
either hold the door or carry the object. The goal for the main robot is to find
an object and bring it to the hallway.'''

# The domain is as follows:
#_________________________
#|       |       |       |
#|   1   |   2   |   3   |
#|       |       |       |
#|--d1---|--d2---|--d3---|
#|       |       |       |
#|   4       5       6   |
#|_______|_______|_______|

def openDoor(r, d):
    rae1.state.load.AcquireLock(r)
    rae1.state.doorStatus.AcquireLock(d)
    if rae1.state.doorStatus[d] == 'opened':
        gui.Simulate("Door %s is already open\n" %d)
        res = SUCCESS
    elif rae1.state.load[r] == NIL and rae1.state.doorStatus[d] == 'closed':
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('openDoor', start) == False):
	        pass
        gui.Simulate("Robot %s has opened door %s\n" %(r, d))
        rae1.state.doorStatus[d] = 'opened'
        res = SUCCESS
    else:
        gui.Simulate("Robot %s is not free to open door %s or the door is not closed\n" %(r, d))
        res = FAILURE
    rae1.state.load.ReleaseLock(r)
    rae1.state.doorStatus.ReleaseLock(d)
    return res

def passDoor(r, d, l):
    rae1.state.doorStatus.AcquireLock(d)
    rae1.state.loc.AcquireLock(r)
    if rae1.state.doorStatus[d] == 'opened' or rae1.state.doorStatus[d] == 'held':
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('passDoor', start) == False):
	        pass
        gui.Simulate("Robot %s has passed the door %s\n" %(r, d))
        rae1.state.loc[r] = l
        res = SUCCESS
    else:
        gui.Simulate("Robot %s is not able to pass door %s\n" %(r, d))
        res = FAILURE
    rae1.state.loc.ReleaseLock(r)
    rae1.state.doorStatus.ReleaseLock(d)
    return res

def holdDoor(r, d):
    rae1.state.doorStatus.AcquireLock(d)
    rae1.state.load.AcquireLock(r)
    if (rae1.state.doorStatus[d] == 'opened' or rae1.state.doorStatus[d] == 'closing') and rae1.state.load[r] == NIL:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('holdDoor', start) == False):
	        pass
        gui.Simulate("Robot %s is holding the door %s\n" %(r, d))
        rae1.state.load[r] = 'H'
        rae1.state.doorStatus[d] = 'held'
        res = SUCCESS
    elif rae1.state.doorStatus[d] == 'closed':
        gui.Simulate("Door %s is closed and cannot be held by %s\n" %(d, r))
        res = FAILURE
    elif rae1.state.load[r] != NIL:
        gui.Simulate("Robot %s is not free to hold the door %s\n" %(r, d))
        res = FAILURE
    rae1.state.doorStatus.ReleaseLock(d)
    rae1.state.load.ReleaseLock(r)
    return res

def releaseDoor(r, d):
    if rae1.state.doorStatus[d] == 'held' and rae1.state.load[r] == 'H':
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('releaseDoor', start) == False):
	        pass
        gui.Simulate("Robot %s has released the the door %s\n" %(r, d))
        rae1.state.doorStatus[d] = 'closing'
        rae1.state.load[r] = NIL
    else:
        gui.Simulate("Robot %s is not holding door %s\n" %(r, d))
    return SUCCESS

def move(r, l1, l2):
    rae1.state.loc.AcquireLock(r)
    if l1 == l2:
        gui.Simulate("Robot %s is already at location %s\n" %(r, l2))
        res = SUCCESS
    elif rae1.state.loc[r] == l1:
        if (l1, l2) in DOORLOCATIONS_SPRINGDOOR or (l2, l1) in DOORLOCATIONS_SPRINGDOOR:
            gui.Simulate("Robot %s cannot move. There is a spring door between %s and %s \n" %(r, l1, l2))
            res = FAILURE
        else:
            start = globalTimer.GetTime()
            while(globalTimer.IsCommandExecutionOver('move', start) == False):
                pass
            gui.Simulate("Robot %s has moved from %d to %d\n" %(r, l1, l2))
            rae1.state.loc[r] = l2
            res = SUCCESS
    else:
        gui.Simulate("Invalid move by robot %s\n" %r)
        res = FAILURE
    rae1.state.loc.ReleaseLock(r)
    return res

def put(r, o):
    rae1.state.pos.AcquireLock(o)
    rae1.state.load.AcquireLock(r)
    rae1.state.loc.AcquireLock(r)
    if rae1.state.pos[o] == r:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('put', start) == False):
	        pass
        rae1.state.pos[o] = rae1.state.loc[r]
        rae1.state.load[r] = NIL
        gui.Simulate("Robot %s has put object %s at location %d\n" %(r,o,rae1.state.loc[r]))
        res = SUCCESS
    else:
        print("Object %s is not with robot %s\n" %(o,r))
        res = FAILURE
    rae1.state.pos.ReleaseLock(o)
    rae1.state.load.ReleaseLock(r)
    rae1.state.loc.ReleaseLock(r)
    return res

def take(r, o):
    rae1.state.pos.AcquireLock(o)
    rae1.state.load.AcquireLock(r)
    rae1.state.loc.AcquireLock(r)
    if rae1.state.load[r] == NIL:
        if rae1.state.loc[r] == rae1.state.pos[o]:
            start = globalTimer.GetTime()
            while(globalTimer.IsCommandExecutionOver('take', start) == False):
	            pass
            gui.Simulate("Robot %s has picked up object %s\n" %(r, o))
            rae1.state.pos[o] = r
            rae1.state.load[r] = o
            res = SUCCESS
        elif rae1.state.loc[r] != rae1.state.pos[o]:
            gui.Simulate("Robot %s is not at object %s's location\n" %(r, o))
            res = FAILURE
    else:
        print("Robot %s is not free to take anything\n" %r)
        res = FAILURE
    rae1.state.pos.ReleaseLock(o)
    rae1.state.load.ReleaseLock(r)
    rae1.state.loc.ReleaseLock(r)
    return res

def closeDoors():
    start = globalTimer.GetTime()
    while(globalTimer.IsCommandExecutionOver('closeDoors', start) == False):
        pass
    for d in ['d1', 'd2', 'd3']:
        rae1.state.doorStatus.AcquireLock(d)
        if rae1.state.doorStatus[d] == 'opened':
            rae1.state.doorStatus[d] = 'closing'
            gui.Simulate("Door %s is closing\n" %d)
        elif rae1.state.doorStatus[d] == 'closing' or rae1.state.doorStatus[d] == 'closed':
            rae1.state.doorStatus[d] = 'closed'
            gui.Simulate("Door %s is closed\n" %d)
        elif rae1.state.doorStatus[d] == 'held':
            gui.Simulate("Door %s is %s, so it cannot be closed\n" %(d, rae1.state.doorStatus[d]))
        rae1.state.doorStatus.ReleaseLock(d)
    return SUCCESS

def MoveThroughDoorway_Method3(r, d, l):
    if rae1.state.load[r] == NIL:
        rae1.do_command(openDoor, r, d)
        rae1.do_command(holdDoor, r, d)
        rae1.do_command(passDoor, r, d, l)
        rae1.do_command(releaseDoor, r, d)
        res = SUCCESS
    else:
        res = FAILURE
    return res

def MoveThroughDoorway_Method2(r, d, l):
    if rae1.state.load[r] != NIL:
        rae1.do_task('getHelp', r)
        rae1.do_command(openDoor, 'r2', d)
        rae1.do_command(holdDoor, 'r2', d)
        rae1.do_command(passDoor, r, d, l)
        rae1.do_command(releaseDoor, 'r2', d)
        res = SUCCESS
    else:
        res = FAILURE
    return res

def MoveThroughDoorway_Method1(r, d, l):
    if rae1.state.load[r] == NIL:
        rae1.do_command(openDoor, r, d)
        rae1.do_command(passDoor, r, d, l)
        res = SUCCESS
    else:
        res = FAILURE
    return res

def MoveTo_Method1(r, l):
    res = SUCCESS
    x = rae1.state.loc[r]
    path = GETPATH_SPRINGDOOR(x, l)
    if path == {}:
        gui.Simulate("Robot %s is already at location %s \n" %(r, l))
    else:
        lTemp = x
        lNext = path[lTemp]
        while(lTemp != l):
            lNext = path[lTemp]
            if (lTemp, lNext) in DOORLOCATIONS_SPRINGDOOR or (lNext, lTemp) in DOORLOCATIONS_SPRINGDOOR:
                d = GETDOOR_SPRINGDOOR(lTemp, lNext)
                rae1.do_task('moveThroughDoorway', r, d, lNext)
            else:
                rae1.do_command(move, r, lTemp, lNext)
            if lNext != rae1.state.loc[r]:
                res = FAILURE
                break
            else:
                lTemp = lNext
    return res

def GetHelp_Method1(r):
    load_r = rae1.state.load['r2']
    if load_r != NIL:
        rae1.do_command(put, 'r2', load_r)
    rae1.do_task('moveTo', 'r2', rae1.state.loc[r])
    return SUCCESS

def Fetch_Method1(r, o, l):
    rae1.do_task('moveTo', r, rae1.state.pos[o])
    load_r = rae1.state.load[r]
    if load_r != NIL:
        rae1.do_command(put, r, load_r)
    rae1.do_command(take, r, o)
    rae1.do_task('moveTo', r, l)
    rae1.state.done = True
    return SUCCESS

def CloseDoors_Method1():
    while rae1.state.done == False:
        rae1.do_command(closeDoors)
    return SUCCESS

def springDoor_init():
    rae1.declare_commands(openDoor, holdDoor, passDoor, releaseDoor, move, put, take, closeDoors)
    print('\n')
    rae1.print_commands()

    rae1.declare_methods('fetch', Fetch_Method1)
    rae1.declare_methods('getHelp', GetHelp_Method1)
    rae1.declare_methods('moveTo', MoveTo_Method1)
    rae1.declare_methods('moveThroughDoorway', MoveThroughDoorway_Method1, MoveThroughDoorway_Method2, MoveThroughDoorway_Method3)
    rae1.declare_methods('closeDoors', CloseDoors_Method1)

    print('\n')
    rae1.print_methods()

    print('\n*********************************************************')
    print("* Call rae1 on spring door domain.")
    print("* For a different amout of printout,  try verbosity(0), verbosity(1), or verbosity(2).")
    print('*********************************************************\n')

    rae1.state.load = {'r1': NIL, 'r2': NIL}
    rae1.state.doorStatus = {'d1': 'closed', 'd2': 'closed', 'd3': 'closed' }
    rae1.state.loc = {'r1': 1, 'r2': 2}
    rae1.state.pos = {'o1': 3}
    rae1.state.done = False