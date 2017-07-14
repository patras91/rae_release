__author__ = 'patras'

from domain_constants import *
import rae1

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
    if (state.doorStatus[d] == 'opened' or state.doorStatus[d] == 'closing') and state.load[r] == NIL:
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
        state.doorStatus[d] = 'closing'
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

def closeDoors(state):
    for d in ['d1', 'd2', 'd3']:
        if state.doorStatus[d] == 'opened':
            state.doorStatus[d] = 'closing'
            print("Door %s is closing\n" %d)
        elif state.doorStatus[d] == 'closing' or state.doorStatus[d] == 'closed':
            state.doorStatus[d] = 'closed'
            print("Door %s is closed\n" %d)
        elif state.doorStatus[d] == 'held':
            print("Door %s is %s, so it cannot be closed\n" %(d, state.doorStatus[d]))
    return SUCCESS

def MoveThroughDoorway_Method3(r, d, l, state, ipcArgs, stackid):
    if state.load[r] == NIL:
        rae1.do_command(openDoor, r, d, state, ipcArgs, stackid)
        rae1.do_command(holdDoor, r, d, state, ipcArgs, stackid)
        rae1.do_command(passDoor, r, d, l, state, ipcArgs, stackid)
        rae1.do_command(releaseDoor, r, d, state, ipcArgs, stackid)
        res = SUCCESS
    else:
        res = FAILURE
    return res

def MoveThroughDoorway_Method2(r, d, l, state, ipcArgs, stackid):
    if state.load[r] != NIL:
        rae1.do_task('getHelp', r, state, ipcArgs, stackid)
        rae1.do_command(openDoor, 'r2', d, state, ipcArgs, stackid)
        rae1.do_command(holdDoor, 'r2', d, state, ipcArgs, stackid)
        rae1.do_command(passDoor, r, d, l, state, ipcArgs, stackid)
        rae1.do_command(releaseDoor, 'r2', d, state, ipcArgs, stackid)
        res = SUCCESS
    else:
        res = FAILURE
    return res

def MoveThroughDoorway_Method1(r, d, l, state, ipcArgs, stackid):
    if state.load[r] == NIL:
        rae1.do_command(openDoor, r, d, state, ipcArgs, stackid)
        rae1.do_command(passDoor, r, d, l, state, ipcArgs, stackid)
        res = SUCCESS
    else:
        res = FAILURE
    return res

def MoveTo_Method1(r, l, state, ipcArgs, stackid):
    res = SUCCESS
    path = GETPATH_SPRINGDOOR(state.loc[r], l)
    if path == {}:
        print("Robot %s is already at location %s \n" %(r, l))
    else:
        lTemp = state.loc[r]
        lNext = path[lTemp]
        while(lTemp != l):
            lNext = path[lTemp]
            if (lTemp, lNext) in DOORLOCATIONS_SPRINGDOOR or (lNext, lTemp) in DOORLOCATIONS_SPRINGDOOR:
                d = GETDOOR_SPRINGDOOR(lTemp, lNext)
                rae1.do_task('moveThroughDoorway', r, d, lNext, state, ipcArgs, stackid)
            else:
                rae1.do_command(move, r, lTemp, lNext, state, ipcArgs, stackid)
            if lTemp == state.loc[r]:
                res = FAILURE
                break
            else:
                lTemp = state.loc[r]

    return res

def GetHelp_Method1(r, state, ipcArgs, stackid):
    if state.load['r2'] != NIL:
        rae1.do_command(put, 'r2', state.load['r2'], state, ipcArgs, stackid)
    rae1.do_task('moveTo', 'r2', state.loc[r], state, ipcArgs, stackid)
    return SUCCESS

def Fetch_Method1(r, o, l, state, ipcArgs, stackid):
    rae1.do_task('moveTo', r, state.pos[o], state, ipcArgs, stackid)
    if state.load[r] != NIL:
        rae1.do_command(put, r, o, state, ipcArgs, stackid)
    rae1.do_command(take, r, o, state, ipcArgs, stackid)
    rae1.do_task('moveTo', r, l, state, ipcArgs, stackid)
    state.done = True
    return SUCCESS

def CloseDoors_Method1(state, ipcArgs, stackid):
    while state.done == False:
        rae1.do_command(closeDoors, state, ipcArgs, stackid)
    return SUCCESS

def springDoor_run_1(state, ipcArgs, stackid):
    rae1.rae1('fetch', 'r1', 'o1', 5, state, ipcArgs, stackid)

def springDoor_run_3(state, ipcArgs, stackid):
    rae1.rae1('closeDoors', state, ipcArgs, stackid)

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
    print("* Call rae1 on spring door using verbosity level 1.")
    print("* For a different amout of printout, try 0 or 2 instead.")
    print('*********************************************************\n')

    rae1.verbosity(0)

    state = rae1.State()
    state.load = {'r1': NIL, 'r2': NIL}
    state.doorStatus = {'d1': 'closed', 'd2': 'closed', 'd3': 'closed' }
    state.loc = {'r1': 1, 'r2': 2}
    state.pos = {'o1': 3}
    state.done = False

    return state