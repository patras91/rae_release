__author__ = 'mason'

from domain_constants import *
import importlib
loader = importlib.find_loader('RAE1_and_RAEplan')
if loader is not None:
    import RAE1_and_RAEplan as ape
else:
    import ape1_and_apeplan as ape

from state import state, rv
import gui
from timer import globalTimer, DURATION
import GLOBALS
import itertools

def fail():
    return FAILURE

# Using Dijsktra's algorithm for ground distance
def OF_GETDISTANCE_GROUND(l0, l1):
    visitedDistances = {l0: 0}
    locs = list(rv.LOCATIONS)

    if l0 == UNK or l0 == NIL or l1 == UNK or l1 == NIL:
        return 10000

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


def Redoer(command, *args):
    i = 0
    while i < 3:
        if i > 0:
            gui.Simulate("--Redoing command-- %s\n" % command)

        state.var1.AcquireLock('redoId')
        localRedoId = state.var1['redoId']
        state.var1['redoId'] += 1
        state.var1.ReleaseLock('redoId')

        state.shouldRedo[localRedoId] = False
        ape.do_command(command, localRedoId, *args)

        if i > 0:
            gui.Simulate("--Finished redo-- %s\n" % command)

        if not state.shouldRedo.pop(localRedoId):
            break
        i += 1

    if i >= 3:
        return FAILURE

    return SUCCESS


def Order_Method1(orderList, m, objList):
    # wait if needed
    if len(orderList) != len(objList):
        ape.do_command(fail)

    while state.busy[m] != False:
        ape.do_command(wait)

    for i,objType in enumerate(orderList):
        # verify correct type
        if objList[i] not in state.OBJ_CLASS[objType]:
            ape.do_command(fail)

        # move to object, pick it up, load in machine
        ape.do_task('pickupAndLoad', objList[i], m)

    # TODO change name wrap to package
    ape.do_task('redoer', wrap, m, objList)
    package = state.var1['temp1']

    ape.do_task('unloadAndDeliver', m, package)

# TODO switch to correct version or write workaround
#Order_Method1.parameters = "[(m, objList,) for m in rv.MACHINES for objList in itertools.combinations(state.OBJECTS,keys())]"
Order_Method1.parameters = "[(m, [objList],) for m in rv.MACHINES for objList in state.OBJECTS.keys()]"


# for free r
def PickupAndLoad_Method1(o, m, r):
    ape.do_task('redoer', acquireRobot, r)

    dist = OF_GETDISTANCE_GROUND(state.loc[r], state.loc[o])
    ape.do_task('redoer', moveRobot, r, state.loc[r], state.loc[o], dist)

    ape.do_task('redoer', pickup, r, o)

    dist = OF_GETDISTANCE_GROUND(state.loc[r], state.loc[m])
    ape.do_task('redoer', moveRobot, r, state.loc[r], state.loc[m], dist)

    ape.do_task('redoer', loadMachine, r, m, o)

    ape.do_task('redoer', freeRobot, r)
PickupAndLoad_Method1.parameters = "[(r,) for r in rv.ROBOTS]"


# unload a package from the machine, move package to shipping doc
# for free r
def UnloadAndDeliver_Method1(m, package, r):
    ape.do_task('redoer', acquireRobot, r)

    dist = OF_GETDISTANCE_GROUND(state.loc[r], state.loc[m])
    ape.do_task('redoer', moveRobot, r, state.loc[r], state.loc[m], dist)

    # TODO: may want this to be a different method
    ape.do_task('redoer', pickup, r, package)

    doc = rv.SHIPPING_DOC[rv.ROBOTS[r]]

    dist = OF_GETDISTANCE_GROUND(state.loc[r], doc)
    ape.do_task('redoer', moveRobot, r, state.loc[r], doc, dist)

    ape.do_task('redoer', putdown, r, package)

    ape.do_task('redoer', freeRobot, r)

    gui.Simulate("Package %s has been delivered\n" % package)
UnloadAndDeliver_Method1.parameters = "[(r,) for r in rv.ROBOTS]"



def moveRobot(redoId, r, l1, l2, dist):
    state.loc.AcquireLock(r)
    state.shouldRedo.AcquireLock(redoId)

    if l1 == l2:
        gui.Simulate("Robot %s is already at location %s\n" %(r, l2))
        res = SUCCESS
        state.shouldRedo[redoId] = False

    elif state.loc[r] == l1:
        res = Sense('moveRobot')

        if res == SUCCESS:
            gui.Simulate("Robot %s has moved from %d to %d\n" %(r, l1, l2))
            state.loc[r] = l2
            state.shouldRedo[redoId] = False
        else:
            gui.Simulate("Robot %s failed to move due to some internal failure\n" %r)
            state.shouldRedo[redoId] = True
            res = SUCCESS
    else:
        gui.Simulate("Robot %s is not in location %d\n" %(r, l1))
        res = FAILURE
        state.shouldRedo[redoId] = False

    state.shouldRedo.ReleaseLock(redoId)
    state.loc.ReleaseLock(r)

    return res


def pickup(redoId, r, item):
    state.load.AcquireLock(r)
    state.loc.AcquireLock(r)
    print(state.loc)
    print(item in state.loc)
    state.loc.AcquireLock(item)
    state.shouldRedo.AcquireLock(redoId)

    if state.load[r] != NIL:
        gui.Simulate("Robot %s is already carrying an object\n" % r)
        res = FAILURE
        state.shouldRedo[redoId] = False
    elif state.loc[r] != state.loc[item]:
        gui.Simulate("Robot %s and item %s are in different locations\n" % (r, item))
        res = FAILURE
        state.shouldRedo[redoId] = False
    elif state.OBJ_WEIGHT[item] > rv.ROBOT_CAPACITY[r]:
        start = globalTimer.GetTime()
        while (globalTimer.IsCommandExecutionOver('pickup', start) == False):
            pass

        gui.Simulate("Item %s is too heavy for robot %s to pick up\n" % (item, r))
        res = FAILURE
        state.shouldRedo[redoId] = False
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
            state.shouldRedo[redoId] = False
        else:
            gui.Simulate("Robot %s dropped item %s\n" % (r, item))
            res = SUCCESS
            state.shouldRedo[redoId] = True

    state.shouldRedo.ReleaseLock(redoId)
    state.loc.ReleaseLock(item)
    state.loc.ReleaseLock(r)
    state.load.ReleaseLock(r)

    return res


def putdown(redoId, r, item):
    state.load.AcquireLock(r)
    state.loc.AcquireLock(r)
    state.loc.AcquireLock(item)
    state.shouldRedo.AcquireLock(redoId)

    if state.load[r] != item:
        gui.Simulate("Robot %s is not carrying the object %s\n" % (r, item))
        res = FAILURE
        state.shouldRedo[redoId] = False
    else:
        start = globalTimer.GetTime()
        while (globalTimer.IsCommandExecutionOver('putdown', start) == False):
            pass
        res = Sense('putdown')

        if res == SUCCESS:
            gui.Simulate("Robot %s put down %s at loc %s\n" % (r, item, state.loc[r]))
            state.loc[item] = state.loc[r]
            state.load[r] = NIL
            state.shouldRedo[redoId] = False
        else:
            gui.Simulate("Robot %s failed to put down %s\n" % (r, item))
            res = SUCCESS
            state.shouldRedo[redoId] = True

    state.shouldRedo.ReleaseLock(redoId)
    state.loc.ReleaseLock(item)
    state.loc.ReleaseLock(r)
    state.load.ReleaseLock(r)

    return res


def loadMachine(redoId, r, m, item):
    state.load.AcquireLock(r)
    state.loc.AcquireLock(r)
    state.loc.AcquireLock(m)
    state.loc.AcquireLock(item)
    state.busy.AcquireLock(m)
    state.shouldRedo.AcquireLock(redoId)

    if state.loc[r] != state.loc[m]:
        gui.Simulate("Robot %s isn't at machine %s" % (r, m))
        res = FAILURE
        state.shouldRedo[redoId] = False
    else:
        start = globalTimer.GetTime()
        while (globalTimer.IsCommandExecutionOver('loadMachine', start) == False):
            pass

        res = Sense('loadMachine')

        if res == SUCCESS:
            gui.Simulate("Robot %s loaded machine %s with item %s\n" % (r, m, item))
            state.load[r] = NIL
            state.loc[item] = state.loc[m]

            # TODO look at this
            if state.busy[m] in state.OBJECTS:
                state.busy[m] = state.busy[m].append(item)
            else:
                state.busy[m] = [item]
            state.shouldRedo[redoId] = False
        else:
            gui.Simulate("Robot %s failed to load machine %s\n" % (r, m))
            res = SUCCESS
            state.shouldRedo[redoId] = True

    state.shouldRedo.ReleaseLock(redoId)
    state.busy.ReleaseLock(m)
    state.loc.ReleaseLock(item)
    state.loc.ReleaseLock(m)
    state.loc.ReleaseLock(r)
    state.load.ReleaseLock(r)

    return res



# to be not busy anymore, or drop object
def acquireRobot(redoId, r):
    state.busy.AcquireLock(r)
    state.load.AcquireLock(r)
    state.shouldRedo.AcquireLock(redoId)

    state.shouldRedo[redoId] = False

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

    state.shouldRedo.ReleaseLock(redoId)
    state.load.ReleaseLock(r)
    state.busy.ReleaseLock(r)

    return res


def freeRobot(redoId, r):
    state.busy.AcquireLock(r)
    state.load.AcquireLock(r)
    state.shouldRedo.AcquireLock(redoId)

    state.shouldRedo[redoId] = False

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

    state.shouldRedo.ReleaseLock(redoId)
    state.load.ReleaseLock(r)
    state.busy.ReleaseLock(r)

    return res


def wrap(redoId, m, objList):
    state.loc.AcquireLock(m)
    state.busy.AcquireLock(m)
    state.numUses.AcquireLock(m)
    state.shouldRedo.AcquireLock(redoId)

    res = SUCCESS
    weight = 0

    for obj in objList:
        weight += state.OBJ_WEIGHT[obj]
        if obj not in state.busy[m]:
            gui.Simulate("Machine %s not loaded with item %s\n" % (m, obj))
            res = FAILURE
            state.shouldRedo[redoId] = False

            state.shouldRedo.ReleaseLock(redoId)
            state.numUses.ReleaseLock(m)
            state.busy.ReleaseLock(m)
            state.loc.ReleaseLock(m)

            return res


    if state.busy[m] == False:
        gui.Simulate("Machine %s is busy\n" % m)
        res = FAILURE
        state.shouldRedo[redoId] = False
    else:
        start = globalTimer.GetTime()
        while (globalTimer.IsCommandExecutionOver('wrap', start) == False):
            pass

        state.numUses[m] += 1
        res = SenseWrap(state.numUses[m])

        if res == SUCCESS:
            # TODO better, unique name
            packageName = hash(frozenset(objList))

            # TODO race condition?
            for item in objList:
                state.OBJECTS.remove(item)

            state.OBJECTS[packageName] = None
            state.loc[packageName] = state.loc[m]
            state.OBJ_WEIGHT[packageName] = weight


            state.var1.AcquireLock('temp1')
            state.var1['temp1'] = packageName
            state.var1.ReleaseLock('temp1')

            gui.Simulate("Machine %s wrapped package %s\n" % (m, packageName))
            state.busy[m] = False
            state.shouldRedo[redoId] = False


        else:
            gui.Simulate("Machine %s jammed. Failed to wrap %s\n" % (m, item))
            state.shouldRedo[redoId] = True
            # set res to success for return
            res = SUCCESS

    state.shouldRedo.ReleaseLock(redoId)
    state.numUses.ReleaseLock(m)
    state.busy.ReleaseLock(m)
    state.loc.ReleaseLock(m)

    return res




# TODO get correct params
ape.declare_task('order', 'orderList')
ape.declare_task('pickupAndLoad', 'o', 'm')
ape.declare_task('unloadAndDeliver', 'm', 'package')
ape.declare_task('redoer', 'command')

ape.declare_methods('order', Order_Method1)
ape.declare_methods('pickupAndLoad', PickupAndLoad_Method1)
ape.declare_methods('unloadAndDeliver', UnloadAndDeliver_Method1)
ape.declare_methods('redoer', Redoer)

ape.declare_commands([fail, wrap, pickup, acquireRobot,
                      loadMachine, moveRobot, freeRobot, putdown,
                      wait])


from env_orderFulfillment import *


