__author__ = 'patras'

'''A robot is searching for an object in the environment consisting of n locations.
It has a battery that needs to be recharged after some moves.
A move consumes 1/4 of the battery capacity.
Recharger is only at one location'''

from domain_constants import *
import importlib
loader = importlib.find_loader('RAE1_and_RAEplan')
if loader is not None:
    import RAE1_and_RAEplan as ape
else:
    import ape1_and_apeplan as ape
import gui
from state import state
from timer import globalTimer
import numpy 
import globals

commandProb = {
    'take': [0.8, 0.2],
    'put': [0.9, 0.1],
}

def Sense(cmd):
    if cmd == 'perceive':
        if globals.GetPlanningMode() == True:
            return 
        return

    #    if cmd in listCommandsDependingOnParams:
    #        # this code is specific for sensing command, 'perceive'
    #        loc = cmdArgs[0]
    #        pDict = commandProb[cmd][loc]
    #        res = []
    #        for obj in pDict:
    #            outcome = numpy.random.choice(len(pDict[obj]), 1, p=pDict[obj])
    #            if outcome[0] == 0:
    #                res.append(obj)
    #    else:
    p = commandProb[cmd]
    outcome = numpy.random.choice(len(p), 1, p=p)
    res = outcome[0]
    if res == 0:
        return SUCCESS
    else:
        return FAILURE

# Using Dijsktra's algorithm
def CR_GETDISTANCE(l0, l1):
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

def fail():
    return FAILURE

def take(r, o):
    state.load.AcquireLock(r)
    if state.load[r] == NIL:
        state.pos.AcquireLock(o)
        if state.loc[r] == state.pos[o]:
            start = globalTimer.GetTime()
            while(globalTimer.IsCommandExecutionOver('take', start) == False):
                pass
            res = Sense('take')
            if res == SUCCESS:
                gui.Simulate("Robot %s has picked up object %s\n" %(r, o))
                state.pos[o] = r
                state.load[r] = o
            else:
                gui.Simulate("Non-deterministic event has made the take command fail\n")
        else:
            gui.Simulate("Robot %s is not at object %s's location\n" %(r, o))
            res = FAILURE
        state.pos.ReleaseLock(o)
    else:
        gui.Simulate("Robot %s is not free to take anything\n" %r)
        res = FAILURE
    state.load.ReleaseLock(r)
    return res

def put(r, o):
    state.pos.AcquireLock(o)
    if state.pos[o] == r:
        start = globalTimer.GetTime()
        state.loc.AcquireLock(r)
        state.load.AcquireLock(r)
        while(globalTimer.IsCommandExecutionOver('put', start) == False):
            pass
        gui.Simulate("Robot %s has put object %s at location %d\n" %(r,o,state.loc[r]))
        state.pos[o] = state.loc[r]
        state.load[r] = NIL
        state.loc.ReleaseLock(r)
        state.load.ReleaseLock(r)
        res = SUCCESS
    else:
        gui.Simulate("Object %s is not with robot %s\n" %(o,r))
        res = FAILURE
    state.pos.ReleaseLock(o)
    return res

def put_Sim(r, o, outcome):
    if outcome == 0:
        state.pos[o] = state.loc[r]
        state.load[r] = NIL
        res = SUCCESS
    else:
        res = FAILURE
    return res

def charge(r, c):
    state.loc.AcquireLock(r)
    state.pos.AcquireLock(c)
    if state.loc[r] == state.pos[c] or state.pos[c] == r:
        state.charge.AcquireLock(r)
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('charge', start) == False):
            pass
        state.charge[r] = 4
        gui.Simulate("Robot %s is fully charged\n" %r)
        state.charge.ReleaseLock(r)
        res = SUCCESS
    else:
        gui.Simulate("Robot %s is not in the charger's location or it doesn't have the charger with it\n" %r)
        res = FAILURE
    state.loc.ReleaseLock(r)
    state.pos.ReleaseLock(c)
    return res

def GetProbability_charge(r, c):
    if state.loc[r] == state.pos[c] or state.pos[c] == r:
        return [0.8, 0.2]
    else:
        return [0.1, 0.9]

def charge_Sim(r, c, outcome):
    if outcome == 0:
        state.charge[r] = 4
        res = SUCCESS
    else:
        res = FAILURE
    return res

def moveCharger(c, l):
    #start = globalTimer.GetTime()
    #while(globalTimer.IsCommandExecutionOver('moveCharger', start) == False):
    #	pass
    state.pos.AcquireLock(c)
    gui.Simulate("Charger %s is moved to location %s\n" %(c,l))
    state.pos[c] = l
    state.pos.ReleaseLock(c)
    return SUCCESS

def GetProbability_moveCharger(c, l):
    return [1]

def moveCharger_Sim(c, l, outcome):
    state.pos[c] = l
    return SUCCESS

def moveToEmergency(r, l1, l2, dist):
    state.loc.AcquireLock(r)
    state.charge.AcquireLock(r)
    if l1 == l2:
        gui.Simulate("Robot %s is already at location %s\n" %(r, l2))
        res = SUCCESS
    elif state.loc[r] == l1 and state.charge[r] >= dist:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('move', start) == False):
           pass
        gui.Simulate("Robot %s has moved from %d to %d\n" %(r, l1, l2))
        state.loc[r] = l2
        state.charge[r] = state.charge[r] - dist
        res = SUCCESS
    elif state.loc[r] != l1 and state.charge[r] >= dist:
        gui.Simulate("Robot %s is not in location %d\n" %(r, l1))
        res = FAILURE
    elif state.loc[r] == l1 and state.charge[r] < dist:
        gui.Simulate("Robot %s does not have enough charge to move :(\n" %r)
        state.charge[r] = 0 # should we do this?
        res = FAILURE
    else:
        gui.Simulate("Robot %s is not at location %s and it doesn't have enough charge!\n" %(r, l1))
        res = FAILURE
    state.loc.ReleaseLock(r)
    state.charge.ReleaseLock(r)
    if res == FAILURE:
        state.emergencyHandling.AcquireLock(r)
        state.emergencyHandling[r] = False
        state.emergencyHandling.ReleaseLock(r)
    return res

def GetProbability_moveToEmergency(r, l1, l2, dist):
    if l1 == l2:
        return [0.8, 0.1, 0, 0.1, 0]
    elif state.loc[r] == l1 and state.charge[r] >= dist:
        return [0.1, 0.7, 0.1, 0.1, 0]
    elif state.loc[r] != l1 and state.charge[r] >= dist:
        return [0.1, 0.1, 0.6, 0.1, 0.1]
    elif state.loc[r] == l1 and state.charge[r] < dist:
        return [0.1, 0.1, 0.1, 0.5, 0.2]
    else:
        return [0.1, 0.1, 0.1, 0.1, 0.6]

def moveToEmergency_Sim(r, l1, l2, dist, outcome):
    if outcome == 0:
        res = SUCCESS
    elif outcome == 1:
        state.loc[r] = l2
        state.charge[r] = state.charge[r] - dist
        res = SUCCESS
    elif outcome == 2:
        res = FAILURE
    elif outcome == 3:
        state.charge[r] = 0 # should we do this?
        res = FAILURE
    else:
        res = FAILURE
    if res == FAILURE:
        state.emergencyHandling[r] = False
    return res

def perceive(l):
    state.view.AcquireLock(l)
    if state.view[l] == False:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('perceive', start) == False):
            pass
        Sense('perceive')
        for c in state.containers[l]:
            state.pos.AcquireLock(c)
            state.pos[c] = l
            state.pos.ReleaseLock(c)
        state.view[l] = True
        gui.Simulate("Perceived location %d\n" %l)
    else:
        gui.Simulate("Already perceived\n")
    state.view.ReleaseLock(l)

    count = len(list(key for key in state.view if state.view[key] == True))
    total = len(rv.LOCATIONS)
    if count != total:
        for loc in rv.LOCATIONS:
            for obj in rv.OBJECTS:
                pass
                #if state.pos[obj] == UNK:
                #    ape.UpdatePerceiveProb(perceive, loc, obj, 1/(total-count))
                #elif state.pos[obj] == loc:
                #    ape.UpdatePerceiveProb(perceive, loc, obj, 1)
                #else:
                #    ape.UpdatePerceiveProb(perceive, loc, obj, 0)
    return SUCCESS

p_perceive={}
def InitProb():
    for loc in rv.LOCATIONS:
        p_perceive[loc] = {}
        for obj in rv.OBJECTS:
            p = 1/len(rv.LOCATIONS)
            p_perceive[loc][obj] = [p, 1 - p]
    #ape.declare_prob(perceive, p_perceive)

ape.AddCommandToSpecialList(perceive)

def perceive_Sim(l, outcome):
    state.view[l] = True
    for obj in outcome:
        state.pos[obj] = l
    return SUCCESS

def MoveTo_Method1(r, l):
    x = state.loc[r]
    dist = CR_GETDISTANCE(x, l)
    if state.charge[r] >= dist:
        ape.do_task('nonEmergencyMove', r, x, l, dist)
    else:
        gui.Simulate("Robot %s does not have enough charge to move\n" %(r))
        ape.do_command(fail)
    return SUCCESS

def move(r, l1, l2, dist):
    state.emergencyHandling.AcquireLock(r)
    if state.emergencyHandling[r] == False:
        state.loc.AcquireLock(r)
        state.charge.AcquireLock(r)
        if l1 == l2:
            gui.Simulate("Robot %s is already at location %s\n" %(r, l2))
            res = SUCCESS
        elif state.loc[r] == l1 and state.charge[r] >= dist:
            start = globalTimer.GetTime()
            while(globalTimer.IsCommandExecutionOver('move', start) == False):
               pass
            gui.Simulate("Robot %s has moved from %d to %d\n" %(r, l1, l2))
            state.loc[r] = l2
            state.charge[r] = state.charge[r] - dist
            res = SUCCESS
        elif state.loc[r] != l1 and state.charge[r] >= dist:
            gui.Simulate("Robot %s is not in location %d\n" %(r, l1))
            res = FAILURE
        elif state.loc[r] == l1 and state.charge[r] < dist:
            gui.Simulate("Robot %s does not have enough charge to move :(\n" %r)
            #state.charge[r] = 0 # should we do this?
            res = FAILURE
        else:
            gui.Simulate("Robot %s is not at location %s and it doesn't have enough charge!\n" %(r, l1))
            res = FAILURE
        state.loc.ReleaseLock(r)
        state.charge.ReleaseLock(r)
    else:
        gui.Simulate("Robot is addressing emergency so it cannot move.\n")
        res = FAILURE
    state.emergencyHandling.ReleaseLock(r)
    return res

def GetProbability_move(r, l1, l2, dist):
    if state.emergencyHandling[r] == False:
        if l1 == l2:
            return [0.7, 0.1, 0.1, 0.1]
        elif state.loc[r] == l1 and state.charge[r] >= dist:
            return [0.1, 0.7, 0.1, 0.1]
        elif state.loc[r] != l1 and state.charge[r] >= dist:
            return [0.1, 0.1, 0.7, 0.1]
        elif state.loc[r] == l1 and state.charge[r] < dist:
            return [0.1, 0.1, 0.1, 0.7]
        else:
            return [0.1, 0.1, 0.1, 0.7]
    else:
        return [0.1, 0.1, 0.1, 0.7]

def move_Sim(r, l1, l2, dist, outcome):
    if outcome == 0:
        res = SUCCESS
    elif outcome == 1:
        if state.charge[r] - dist > 0:
            state.loc[r] = l2 
            state.charge[r] = state.charge[r] - dist
            res = SUCCESS
        else:
            res = FAILURE
    elif outcome == 2:
        res = FAILURE
    elif outcome == 3:
        state.charge[r] = 0 # should we do this?
        res = FAILURE
    return res

def addressEmergency(r, l, i):
    state.loc.AcquireLock(r)
    state.emergencyHandling.AcquireLock(r)
    if state.loc[r] == l:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('addressEmergency', start) == False):
            pass
        gui.Simulate("Robot %s has addressed emergency %d\n" %(r, i))
        res = SUCCESS
    else:
        gui.Simulate("Robot %s has failed to address emergency %d\n" %(r, i))
        res = FAILURE
    state.emergencyHandling[r] = False
    state.loc.ReleaseLock(r)
    state.emergencyHandling.ReleaseLock(r)
    return res

def GetProbability_addressEmergency(r, l, i):
    if state.loc[r] == l:
        return [0.8, 0.2]
    else:
        return [0.2, 0.8]

def addressEmergency_Sim(r, l, i, outcome):
    if outcome == 0:
        res = SUCCESS
    else:
        res = FAILURE
    state.emergencyHandling[r] = False
    return res

def wait(r):
    while(state.emergencyHandling[r] == True):
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('wait', start) == False):
            pass
        gui.Simulate("Robot %s is waiting for emergency to be over\n" %r)
    return SUCCESS

def GetProbability_wait(r):
    return [1]

def wait_Sim(r, outcome):
    state.emergencyHandling[r] = False
    return SUCCESS

# def Recharge_Method1(r, c):
#     if state.loc[r] != state.pos[c] and state.pos[c] != r:
#         if state.pos[c] in rv.LOCATIONS:
#             ape.do_task('moveTo', r, state.pos[c])
#         else:
#             gui.Simulate("%s cannot find charger %s\n" %(r, c))
#             return FAILURE
#     ape.do_command(charge, r, c)
#     return SUCCESS

# def Recharge_Method2(r, c):
#     if state.loc[r] != state.pos[c] and state.pos[c] != r:
#         if state.pos[c] in rv.LOCATIONS:
#             ape.do_task('moveTo', r, state.pos[c])
#         else:
#             gui.Simulate("%s cannot find charger %s\n" %(r, c))
#             return FAILURE
#     ape.do_command(charge, r, c)
#     ape.do_command(take, r, c)
#     return SUCCESS

def Recharge_Method3(r, c):
    if state.loc[r] != state.pos[c] and state.pos[c] != r:
        if state.pos[c] in rv.LOCATIONS:
            ape.do_task('moveTo', r, state.pos[c])
        else:
            robot = state.pos[c]
            ape.do_command(put, robot, c)
            ape.do_task('moveTo', r, state.pos[c])
    ape.do_command(charge, r, c)
    if state.load[r] == NIL:
        ape.do_command(take, r, c)
    return SUCCESS

def Recharge_Method2(r, c):
    if state.loc[r] != state.pos[c] and state.pos[c] != r:
        if state.pos[c] in rv.LOCATIONS:
            ape.do_task('moveTo', r, state.pos[c])
        else:
            robot = state.pos[c]
            ape.do_command(put, robot, c)
            ape.do_task('moveTo', r, state.pos[c])
    ape.do_command(charge, r, c)
    return SUCCESS

def Recharge_Method1(r, c):
    robot = NIL
    if state.loc[r] != state.pos[c] and state.pos[c] != r:
        if state.pos[c] in rv.LOCATIONS:
            ape.do_task('moveTo', r, state.pos[c])
        else:
            robot = state.pos[c]
            ape.do_command(put, robot, c)
            ape.do_task('moveTo', r, state.pos[c])
    ape.do_command(charge, r, c)
    if robot != NIL and state.load[robot] != NIL and state.pos[robot] == state.loc[c]:
        ape.do_command(take, robot, c)
    return SUCCESS

def Search_Method1(r, o):
    if state.pos[o] == UNK:
        toBePerceived = NIL
        for l in rv.LOCATIONS:
            if state.view[l] == False:
                toBePerceived = l
                break

        if toBePerceived != NIL:
            ape.do_task('moveTo', r, toBePerceived)
            ape.do_command(perceive, toBePerceived)
            if state.pos[o] == toBePerceived:
                if state.load[r] != NIL:
                    ape.do_command(put, r, state.load[r])
                ape.do_command(take, r, o)
            else:
                ape.do_task('search', r, o)
            res = SUCCESS
        else:
            gui.Simulate("Failed to search %s" %o)
            res = FAILURE
    else:
        gui.Simulate("Position of %s is already known\n" %o)
        res = SUCCESS
    return res

def Search_Method2(r, o):
    if state.pos[o] == UNK:
        toBePerceived = NIL
        for l in rv.LOCATIONS:
            if state.view[l] == False:
                toBePerceived = l
                break

        if toBePerceived != NIL:
            ape.do_task('recharge', r, 'c1') # is this allowed?
            ape.do_task('moveTo', r, toBePerceived)
            ape.do_command(perceive, toBePerceived)
            if state.pos[o] == toBePerceived:
                if state.load[r] != NIL:
                    ape.do_command(put, r, state.load[r])
                ape.do_command(take, r, o)
            else:
                ape.do_task('search', r, o)
            res = SUCCESS
        else:
            gui.Simulate("Failed to search %s" %o)
            res = FAILURE
    else:
        gui.Simulate("Position of %s is already known\n" %o)
        res = SUCCESS
    return res

def Fetch_Method1(r, o):
    pos_o = state.pos[o]
    if pos_o == UNK:
        ape.do_task('search', r, o)
    elif state.loc[r] == pos_o:
        if state.load[r] != NIL:
            ape.do_command(put, r, state.load[r])
        ape.do_command(take, r, o)
    else:
        ape.do_task('moveTo', r, pos_o)
        if state.load[r] != NIL:
            ape.do_command(put, r, state.load[r])
        ape.do_command(take, r, o)
    return SUCCESS

def Fetch_Method2(r, o):
    pos_o = state.pos[o]
    if pos_o == UNK:
        ape.do_task('search', r, o)
    elif state.loc[r] == pos_o:
        if state.load[r] != NIL:
            ape.do_command(put, r, state.load[r])
        ape.do_command(take, r, o)
    else:
        ape.do_task('recharge', r, 'c1')
        ape.do_task('moveTo', r, pos_o)
        if state.load[r] != NIL:
            ape.do_command(put, r, state.load[r])
        ape.do_command(take, r, o)
    return SUCCESS

def RelocateCharger(c, l):
    res = SUCCESS
    for r in state.charge:
        if state.charge[r] != 4:
            res = FAILURE

    if res == SUCCESS:
        moveCharger(c, l)
    else:
        gui.Simulate("Cannot move charger now, robots might need it\n")

    return res

def Emergency_Method1(r, l, i):
    if state.emergencyHandling[r] == False:
        state.emergencyHandling[r] = True
        load_r = state.load[r]
        if load_r != NIL:
            ape.do_command(put, r, load_r, state.loc[r])
        l1 = state.loc[r]
        dist = CR_GETDISTANCE(l1, l)
        ape.do_command(moveToEmergency, r, l1, l, dist)
        ape.do_command(addressEmergency, r, l, i)
        res = SUCCESS
    else:
        gui.Simulate("%r is already busy handling another emergency\n" %r)
        res = FAILURE
    return res

# def NonEmergencyMove_Method1(r, l1, l2, dist):
#     if state.emergencyHandling[r] == False:
#         ape.do_command(move, r, l1, l2, dist)
#         res = SUCCESS
#     else:
#         gui.Simulate("Move failed, trying to do a non emergency move for a robot handling emergency\n")
#         res = FAILURE
#     return res

def NonEmergencyMove_Method1(r, l1, l2, dist):
    if state.emergencyHandling[r] == False:
        ape.do_command(move, r, l1, l2, dist)
    else:
        ape.do_command(wait, r)
        ape.do_command(move, r, l1, l2, dist)
    return SUCCESS

rv = RV()
ape.declare_commands([put, take, perceive, charge, move, moveCharger, moveToEmergency, addressEmergency, wait, fail])

ape.declare_methods('search', Search_Method1, Search_Method2)
ape.declare_methods('fetch', Fetch_Method1, Fetch_Method2)
ape.declare_methods('recharge', Recharge_Method2) # Recharge_Method3, Recharge_Method1)
ape.declare_methods('moveTo', MoveTo_Method1)
ape.declare_methods('emergency', Emergency_Method1)
ape.declare_methods('nonEmergencyMove', NonEmergencyMove_Method1)

#ape.declare_methods('relocateCharger', RelocateCharger_Method1)

