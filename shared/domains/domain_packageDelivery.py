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
from timer import globalTimer
import globals

def fail():
    return FAILURE

# Using Dijsktra's algorithm
def PD_GETDISTANCE(l0, l1):
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

        for l in rv.EDGES[min_loc]:
            dist = current_dist + 1
            if l not in visitedDistances or dist < visitedDistances[l]:
                visitedDistances[l] = dist

    return visitedDistances[l1]

def Order_Method1(item, l, type):
    # order from item i of shipping type type, to location l
    ape.do_task('find', item)
    ape.do_task('pack', item)
    ape.do_task('deliver', item, l, type)

# Refinement methods for find

def Find_Method1(item):
    # search an online database
    loc_item = state.loc[item]
    if loc_item == UNK:
        ape.do_command(lookupDB, item, state.NationalDatabase)

def lookupDB(item, database):
    state.loc.AcquireLock(item)
    database.AcquireLock(item)
    start = globalTimer.GetTime()

    while(globalTimer.IsCommandExecutionOver('lookupDB', start) == False):
        pass

    res = Sense('lookupDB')
    if res == SUCCESS:
        gui.Simulate("Found item %s from database \n" % item)
        state.loc[item] = database[item]
    else:
        gui.Simulate("Database %database is down \n" % (item, database))

    state.NationalDatabase.ReleaseLock(item)
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

def Pack_Method1(item):
    ape.do_task('getRobot', state.loc[item])
    r = state.var1['temp']
    ape.do_command(moveRobot, r, state.loc[r], state.loc[item])
    ape.do_command(pickup, r, item)

    ape.do_task('getMachine', state.loc[r])
    m = state.var1['temp1']
    ape.do_command(moveRobot, r, state.loc[r], state.loc[m])
    ape.do_command(loadMachine, r, m, item)
    ape.do_command(wrap, m, item)

def moveRobot(r, l1, l2):
    state.loc.AcquireLock(r)

    if l1 == l2:
        gui.Simulate("Robot %s is already at location %s\n" %(r, l2))
        res = SUCCESS
    elif state.loc[r] == l1:
        start = globalTimer.GetTime()

        #TODO how to make the command durration dependent on distance
        while(globalTimer.IsCommandExecutionOver('moveRobot', start) == False):
           pass
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


def loadMachine(r, m, item):
    state.load.AcquireLock(r)
    state.loc.AcquireLock(r)
    state.loc.AcquireLock(m)
    state.loc.AcquireLock(item)

    if state.loc[r] != state.loc[m]:
        gui.Simulate("Robot %s isn't at machine %s" % (r, m))
        res = FAILURE
    else:
        start = globalTimer.GetTime()
        while (globalTimer.IsCommandExecutionOver('pickup', start) == False):
            pass

        res = Sense('load')

        if res == SUCCESS:
            gui.Simulate("Robot %s loaded machine %s with item %s\n" % (r, m, item))
            state.load[r] = NIL
            state.loc[item] = state.loc[m]
        else:
            gui.Simulate("Robot %s failed to load machine %s\n" % (r, m))

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
        gui.Simulate("Robot %s is acquired for a new task\n" % r)
        state.busy[r] = True
        res = SUCCESS

    state.load.ReleaseLock(r)
    state.busy.ReleaseLock(r)

    return res


def GetRobot_Method1(l):
    # return the robot which is nearest
    r0 = min(rv.ROBOTS, key=lambda r: PD_GETDISTANCE(state.loc[r], l))

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

def GetRobot_Method3(l):
    # return the one which is free
    gui.Simulate("Method not implemented")
    ape.do_command(fail)
'''

# Refinement methods for getMachine

def GetMachine_Method1(l):
    # return the machine closest to the sent location (robot's loc)
    m0 = min(rv.MACHINES, key=lambda m: PD_GETDISTANCE(state.loc[m], l))

    state.var1.AcquireLock('temp1')
    state.var1['temp1'] = m0
    state.var1.ReleaseLock('temp1')

    return SUCCESS

def wrap(m, item):
    state.loc.AcquireLock(m)
    state.loc.AcquireLock(item)

    if state.loc[m] != state.loc[item]:
        gui.Simulate("Machine %s not loaded with item %s\n" % (m,item))
        res = FAILURE
    else:
        start = globalTimer.GetTime()
        while (globalTimer.IsCommandExecutionOver('wrap', start) == False):
            pass

        res = Sense('wrap')

        if res == SUCCESS:
            gui.Simulate("Machine %s wrapped item %s\n" % (m, item))
        else:
            gui.Simulate("Machine %s jammed. Failed to wrap %s\n" % (m, item))

    state.loc.ReleaseLock(item)
    state.loc.ReleaseLock(m)

    return res

# Refinement methods for deliver

def Deliver_Method1(item, l, type):
    if type == 'slow':
        '''Search for the transport that minimizes the cost:
                there can be multiple methods fo doing this
        '''
        gui.Simulate("%s is an unsupported delivery type\n" % type)
        ape.do_command(fail)
    elif type == 'fast':
        ''' Search for the fastest flight/ground transportation
        '''
        ape.do_command(groundShip, item, l)
    else:
        gui.Simulate("%s is an unsupported delivery type\n" % type)
        ape.do_command(fail)

def groundShip(item, l):
    state.loc.AcquireLock(item)

    start = globalTimer.GetTime()
    while (globalTimer.IsCommandExecutionOver('groundShip', start) == False):
        pass

    res = Sense('wrap')

    if res == SUCCESS:
        gui.Simulate("Delivered item %s\n" % item)
        state.loc[item] = l
    else:
        gui.Simulate("Failed to deliver item %s\n" % item)

    state.loc.ReleaseLock

    return res

rv = RV()
ape.declare_commands([lookupDB, fail, moveRobot, wrap, pickup, acquireRobot, loadMachine, groundShip])

ape.declare_methods('order', Order_Method1)
ape.declare_methods('find', Find_Method1)
ape.declare_methods('pack', Pack_Method1)
ape.declare_methods('getRobot', GetRobot_Method1)
ape.declare_methods('getMachine', GetMachine_Method1)
ape.declare_methods('deliver', Deliver_Method1)


from env_packageDelivery import *


