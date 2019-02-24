__author__ = 'mason'

from domain_constants import *
import importlib
loader = importlib.find_loader('RAE1_and_RAEplan')
if loader is not None:
    import RAE1_and_RAEplan as ape
else:
    import ape1_and_apeplan as ape

from state import state
import gui
from timer import globalTimer, DURATION
import globals

def fail():
    return FAILURE

# Using Dijsktra's algorithm for ground distance
def OF_GETDISTANCE_GROUND(l0, l1):
    visitedDistances = {l0: 0}
    locs = list(rv.LOCATIONS)

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

        for l in rv.GROUND_EDGES[min_loc]:
            if min_loc < l:
                dist = current_dist + rv.GROUND_WEIGHTS[(min_loc, l)]
            else:
                dist = current_dist + rv.GROUND_WEIGHTS[(l, min_loc)]

            if l not in visitedDistances or dist < visitedDistances[l]:
                visitedDistances[l] = dist

    return visitedDistances[l1]


def wait():
    start = globalTimer.GetTime()
    while (globalTimer.IsCommandExecutionOver('wait', start) == False):
        pass

    return SUCCESS



def Order_Method1(itemClass, l):
    # order from item i of shipping type type, to location l
    print("start of Order_Method1")
    ape.do_task('find', itemClass)
    item = state.var1['temp2']
    ape.do_task('pack_redoer', item)

# Refinement methods for find


def Find_Method1(itemClass):
    # search an online database
    # take the location of the first object of the correct type
    print("Entered Find")
    for i in rv.OBJ_CLASS[itemClass]:
        if state.storedLoc[i] != NIL:
            item = i
            break

    ape.do_command(lookupDB, item)

    state.var1.AcquireLock('temp')
    state.var1['temp2'] = item
    state.var1.ReleaseLock('temp')

    return SUCCESS


def lookupDB(item):
    state.loc.AcquireLock(item)
    state.storedLoc.AcquireLock(item)

    start = globalTimer.GetTime()

    while(globalTimer.IsCommandExecutionOver('lookupDB', start) == False):
        pass

    res = Sense('lookupDB')
    if res == SUCCESS:
        gui.Simulate("Found item %s from database\n" % item)
        state.loc[item] = state.storedLoc[item]
        state.storedLoc[item] = NIL

    else:
        gui.Simulate("National database is down\n")

    state.storedLoc.ReleaseLock(item)
    state.loc.ReleaseLock(item)

    return res


'''
def Find_Method2(item):
    # search some local warehouse database
    gui.Simulate("Method not implemented")
    ape.do_command(fail)

def Find_Method3(item):
    # query a supplier of that item
    gui.Simulate("Method not implemented")
    ape.do_command(fail)
'''

# Refinement methods for pack

def Pack_Redoer(item):
    print("start of Pack_Redoer")
    while True:
        if ape.do_task('pack', item) == SUCCESS:
            break

    return SUCCESS


def Pack_Method1(item):
    print('Start of Pack')
    ape.do_task('getRobot', state.loc[item], rv.OBJ_WEIGHT[item])
    r = state.var1['temp']

    #TODO do I need to lock this?
    dist = OF_GETDISTANCE_GROUND(state.loc[r], state.loc[item])
    ape.do_command(moveRobot, r, state.loc[r], state.loc[item], dist)

    ape.do_command(pickup, r, item)

    ape.do_task('getMachine', state.loc[r])
    m = state.var1['temp1']

    # TODO do I need to lock this?
    dist = OF_GETDISTANCE_GROUND(state.loc[r], state.loc[m])
    ape.do_command(moveRobot, r, state.loc[r], state.loc[m], dist)

    while state.busy[m] != False:
        ape.do_command(wait)

    ape.do_command(loadMachine, r, m, item)
    ape.do_command(wrap, m, item)

    # now move item to the shipping doc
    ape.do_command(pickup, r, item)

    # TODO do I need to lock this?
    doc = rv.SHIPPING_DOC[rv.ROBOTS[r]]

    dist = OF_GETDISTANCE_GROUND(state.loc[r], doc)
    ape.do_command(moveRobot, r, state.loc[r], doc, dist)

    ape.do_command(putdown, r, item)
    ape.do_command(freeRobot, r)

    gui.Simulate("Item %s has been placed in the shipping doc\n" % item)

    print("EXITING PACK_METHOD1")

    return SUCCESS



def moveRobot(r, l1, l2, dist):
    state.loc.AcquireLock(r)

    if l1 == l2:
        gui.Simulate("Robot %s is already at location %s\n" %(r, l2))
        res = SUCCESS

    elif r in rv.ROBOTS and l2 not in rv.ROBOTS[r]:
        gui.Simulate("Robot %s can't leave the factory\n" % r)
        res = FAILURE

    elif r not in rv.ROBOTS and l2 not in rv.REPAIR_BOT[r]:
        gui.Simulate("Robot %s can't leave the factory\n" % r)
        res = FAILURE

    elif state.loc[r] == l1:
        res = Sense('moveRobot')

        if res == SUCCESS:
            gui.Simulate("Robot %s has moved from %d to %d\n" %(r, l1, l2))
            state.loc[r] = l2
        else:
            gui.Simulate("Robot %s failed to move due to some internal failure\n" %r)
    else:
        gui.Simulate("Robot %s is not in location %d\n" %(r, l1))
        res = FAILURE

    state.loc.ReleaseLock(r)

    return res


def pickup(r, item):
    state.load.AcquireLock(r)
    state.loc.AcquireLock(r)
    state.loc.AcquireLock(item)

    if state.load[r] != NIL:
        gui.Simulate("Robot %s is already carrying an object\n" % r)
        res = FAILURE
    elif state.loc[r] != state.loc[item]:
        gui.Simulate("Robot %s and item %s are in different locations" % (r, item))
        res = FAILURE
    elif rv.OBJ_WEIGHT[item] > rv.ROBOT_CAPACITY[r]:
        start = globalTimer.GetTime()
        while (globalTimer.IsCommandExecutionOver('pickup', start) == False):
            pass

        gui.Simulate("Item %s is too heavy for robot %s to pick up\n" % (item, r))
        res = FAILURE
    else:
        start = globalTimer.GetTime()
        while (globalTimer.IsCommandExecutionOver('pickup', start) == False):
            pass
        res = Sense('pickup')

        if res == SUCCESS:
            gui.Simulate("Robot %s picked up %s\n" % (r, item))
            # TODO not sure if I want the location of the item to be nil or r
            # Not sure what the consequences of them are, awkward if someone else
            # tries to find the item
            state.loc[item] = NIL
            state.load[r] = item
        else:
            gui.Simulate("Robot %s dropped item %s\n" % (r, item))

    state.loc.ReleaseLock(item)
    state.loc.ReleaseLock(r)
    state.load.ReleaseLock(r)

    return res


def putdown(r, item):
    state.load.AcquireLock(r)
    state.loc.AcquireLock(r)
    state.loc.AcquireLock(item)

    if state.load[r] != item:
        gui.Simulate("Robot %s is not carrying the object %s\n" % (r, item))
        res = FAILURE
    else:
        start = globalTimer.GetTime()
        while (globalTimer.IsCommandExecutionOver('putdown', start) == False):
            pass
        res = Sense('putdown')

        if res == SUCCESS:
            gui.Simulate("Robot %s put down %s at loc %s\n" % (r, item, state.loc[r]))
            state.loc[item] = state.loc[r]
            state.load[r] = NIL
        else:
            gui.Simulate("Robot %s failed to put down %s\n" % (r, item))

    state.loc.ReleaseLock(item)
    state.loc.ReleaseLock(r)
    state.load.ReleaseLock(r)

    return res


def loadMachine(r, m, item):
    state.load.AcquireLock(r)
    state.loc.AcquireLock(r)
    state.loc.AcquireLock(m)
    state.loc.AcquireLock(item)
    state.busy.AcquireLock(m)

    if state.loc[r] != state.loc[m]:
        gui.Simulate("Robot %s isn't at machine %s" % (r, m))
        res = FAILURE
    elif state.busy[m] != False:
        gui.Simulate("Machine %s is busy, can't be loaded" % m)
        res = FAILURE
    else:
        start = globalTimer.GetTime()
        while (globalTimer.IsCommandExecutionOver('loadMachine', start) == False):
            pass

        res = Sense('loadMachine')

        if res == SUCCESS:
            gui.Simulate("Robot %s loaded machine %s with item %s\n" % (r, m, item))
            state.load[r] = NIL
            state.loc[item] = state.loc[m]
            state.busy[m] = item
        else:
            gui.Simulate("Robot %s failed to load machine %s\n" % (r, m))

    state.busy.ReleaseLock(m)
    state.loc.ReleaseLock(item)
    state.loc.ReleaseLock(m)
    state.loc.ReleaseLock(r)
    state.load.ReleaseLock(r)

    return res


# Refinement methods for getRobot

# TODO Maybe figure out how to wait for the robot
# to be not busy anymore, or drop object
def acquireRobot(r):
    state.busy.AcquireLock(r)
    state.load.AcquireLock(r)

    if state.busy[r] == True:
        gui.Simulate("Robot %s is busy\n" % r)
        res = FAILURE
    elif state.load[r] != NIL:
        gui.Simulate("Robot %s is carrying an object\n" % r)
        res = FAILURE
    else:
        start = globalTimer.GetTime()
        while (globalTimer.IsCommandExecutionOver('acquireRobot', start) == False):
            pass

        gui.Simulate("Robot %s is acquired for a new task\n" % r)
        state.busy[r] = True
        res = SUCCESS

    state.load.ReleaseLock(r)
    state.busy.ReleaseLock(r)

    return res


def freeRobot(r):
    state.busy.AcquireLock(r)
    state.load.AcquireLock(r)

    if state.load[r] != NIL:
        gui.Simulate("Robot %s is carrying an object\n" % r)
        res = FAILURE
    else:
        start = globalTimer.GetTime()
        while (globalTimer.IsCommandExecutionOver('freeRobot', start) == False):
            pass

        gui.Simulate("Robot %s is now free\n" % r)
        state.busy[r] = False
        res = SUCCESS

    state.load.ReleaseLock(r)
    state.busy.ReleaseLock(r)

    return res


#TODO could have a problem b/c not locking state.loc[r]
def GetRobot_Method1(l, c):
    print("start of GetRobot_Method1")
    # return the robot which is nearest
    r0 = min(list(rv.ROBOTS), key=lambda r: OF_GETDISTANCE_GROUND(state.loc[r], l))

    while state.busy[r0] != False:
        ape.do_command(wait)

    res = ape.do_command(acquireRobot, r0)

    state.var1.AcquireLock('temp')
    state.var1['temp'] = r0
    state.var1.ReleaseLock('temp')

    return res


'''
def GetRobot_Method2(l):
    # return the one which is already going to l or nearby areas
    gui.Simulate("Method not implemented")
    ape.do_command(fail)
'''


#TODO could have a problem b/c not locking state.busy[r]
def GetRobot_Method3(l, c):
    print("start of GetRobot_METHOD3")
    # return the one which is free, given it's in the factory
    r0 = NIL

    for r in list(rv.ROBOTS):
        if state.busy[r] == False and l in rv.ROBOTS[r]:
            r0 = r
            break

    if r0 == NIL:
        return FAILURE

    while state.busy[r0] != False:
        ape.do_command(wait)

    res = ape.do_command(acquireRobot, r0)

    state.var1.AcquireLock('temp')
    state.var1['temp'] = r0
    state.var1.ReleaseLock('temp')

    return res


def GetRobot_Method4(l, c):
    print("start of GetRobot_Method4")
    # return one which has a high enough capacity,
    # given it's in the factory
    r0 = NIL

    for r in list(rv.ROBOTS):
        if rv.ROBOT_CAPACITY[r] >= c and l in rv.ROBOTS[r]:
            r0 = r
            break

    if r0 == NIL:
        return FAILURE

    while state.busy[r0] != False:
        ape.do_command(wait)

    res = ape.do_command(acquireRobot, r0)

    state.var1.AcquireLock('temp')
    state.var1['temp'] = r0
    state.var1.ReleaseLock('temp')

    return res


# Refinement methods for getMachine

def GetMachine_Method1(l):
    print("start of GetMachine_1")
    # return the machine closest to the sent location (robot's loc)
    m0 = min(rv.MACHINES, key=lambda m: OF_GETDISTANCE_GROUND(state.loc[m], l))

    state.var1.AcquireLock('temp1')
    state.var1['temp1'] = m0
    state.var1.ReleaseLock('temp1')

    return SUCCESS


#TODO could have a problem b/c not locking state.busy[r]
def GetMachine_Method2(l):
    print("start of GetMachine_2")
    # return a machine that isn't busy and in the factory
    m0 = NIL

    for m in rv.MACHINES:
        if state.busy[m] == False and l in rv.MACHINES[m]:
            m0 = m
            break

    if m0 == NIL:
        return FAILURE

    state.var1.AcquireLock('temp1')
    state.var1['temp1'] = m0
    state.var1.ReleaseLock('temp1')

    return SUCCESS


def GetMachine_Method3(l):
    print("start of GetMachine_3")
    # selection of method1, but also repairs machine
    m0 = min(rv.MACHINES, key=lambda m: OF_GETDISTANCE_GROUND(state.loc[m], l))

    state.var1.AcquireLock('temp1')
    state.var1['temp1'] = m0
    state.var1.ReleaseLock('temp1')

    ape.do_task('fixMachine', m0)

    return SUCCESS


def GetMachine_Method4(l):
    print("start of GetMachine_4")
    # selection of method2, but also repairs machine
    m0 = NIL

    for m in rv.MACHINES:
        if state.busy[m] == False and l in rv.MACHINES[m]:
            m0 = m
            break

    if m0 == NIL:
        return FAILURE

    state.var1.AcquireLock('temp1')
    state.var1['temp1'] = m0
    state.var1.ReleaseLock('temp1')

    ape.do_task('fixMachine', m0)

    return SUCCESS


def wrap(m, item):
    state.loc.AcquireLock(m)
    state.loc.AcquireLock(item)
    state.busy.AcquireLock(m)
    state.numUses.AcquireLock(m)

    if state.loc[m] != state.loc[item]:
        gui.Simulate("Machine %s not loaded with item %s\n" % (m,item))
        res = FAILURE
    elif state.busy[m] != item:
        gui.Simulate("Machine %s is busy\n" % m)
        res = FAILURE
    else:
        start = globalTimer.GetTime()
        while (globalTimer.IsCommandExecutionOver('wrap', start) == False):
            pass

        state.numUses[m] += 1
        res = SenseWrap(state.numUses[m])

        if res == SUCCESS:
            gui.Simulate("Machine %s wrapped item %s\n" % (m, item))
            state.busy[m] = False
        else:
            gui.Simulate("Machine %s jammed. Failed to wrap %s\n" % (m, item))

    state.numUses.ReleaseLock(m)
    state.busy.ReleaseLock(m)
    state.loc.ReleaseLock(item)
    state.loc.ReleaseLock(m)

    return res


# TODO add another method for this
def FixMachine_Method1(m):
    print("start of FixMachine")
    # return the one which is free, given it's in the factory
    rf0 = NIL

    for r in list(rv.REPAIR_BOT):
        if state.busy[r] == False and state.loc[m] in rv.REPAIR_BOT[r]:
            rf0 = r
            break

    if rf0 == NIL:
        return FAILURE

    ape.do_command(acquireRobot, rf0)

    # move the robot to the machine
    dist = OF_GETDISTANCE_GROUND(state.loc[r], state.loc[m])
    ape.do_command(moveRobot, r, state.loc[r], state.loc[m], dist)

    # repair thte machine
    ape.do_command(repair, r, m)

    return SUCCESS


def repair(r, m):
    state.loc.AcquireLock(m)
    state.loc.AcquireLock(r)
    state.busy.AcquireLock(m)
    state.numUses.AcquireLock(m)

    if state.loc[m] != state.loc[r]:
        gui.Simulate("%s is not in same location as %s\n" % (r,m))
        res = FAILURE
    elif state.busy[m] != False:
        gui.Simulate("Machine %s is busy\n" % m)
        res = FAILURE
    else:
        start = globalTimer.GetTime()
        while (globalTimer.IsCommandExecutionOver('repair', start) == False):
            pass

        res = Sense('repair')

        if res == SUCCESS:
            gui.Simulate("Robot %s repaired machine %s\n" % (r, m))
            state.numUses[m] /= 2
        else:
            gui.Simulate("Machine %s wasn't repaired\n" % m)

    state.numUses.ReleaseLock(m)
    state.busy.ReleaseLock(m)
    state.loc.ReleaseLock(r)
    state.loc.ReleaseLock(m)

    return res



rv = RV()
ape.declare_commands([lookupDB, fail, wrap, pickup, acquireRobot,
                      loadMachine, moveRobot, freeRobot, putdown,
                      repair, wait])

ape.declare_methods('order', Order_Method1)
ape.declare_methods('find', Find_Method1)
ape.declare_methods('pack', Pack_Method1)
ape.declare_methods('pack_redoer', Pack_Redoer)
ape.declare_methods('getRobot', GetRobot_Method1, GetRobot_Method3, GetRobot_Method4)
ape.declare_methods('getMachine', GetMachine_Method1, GetMachine_Method2, GetMachine_Method3, GetMachine_Method4)

ape.declare_methods('fixMachine', FixMachine_Method1)


from env_orderFulfillment import *


