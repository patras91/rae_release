__author__ = 'patras'

'''A robot is searching for an object in the environment consisting of n locations.
It has a battery that needs to be recharged after some moves.
A move consumes 1/4 of the battery capacity.
Recharger is only at one location'''

from domain_constants import *
import ape
import gui
from timer import globalTimer

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

def take(r, o):
    ape.state.load.AcquireLock(r)
    if ape.state.load[r] == NIL:
        ape.state.pos.AcquireLock(o)
        if ape.state.loc[r] == ape.state.pos[o]:
            start = globalTimer.GetTime()
            while(globalTimer.IsCommandExecutionOver('take', start) == False):
                pass
            gui.Simulate("Robot %s has picked up object %s\n" %(r, o))
            ape.state.pos[o] = r
            ape.state.load[r] = o
            res = SUCCESS
        else:
            gui.Simulate("Robot %s is not at object %s's location\n" %(r, o))
            res = FAILURE
        ape.state.pos.ReleaseLock(o)
    else:
        gui.Simulate("Robot %s is not free to take anything\n" %r)
        res = FAILURE
    ape.state.load.ReleaseLock(r)
    return res

def GetProbability_take(r, o):
    if ape.state.load[r] == NIL:
        if ape.state.loc[r] == ape.state.pos[o]:
            return [0.8, 0.2]
        else:
            return [0.1, 0.9]
    else:
        return [0.1, 0.9]

ape.declare_prob(take, GetProbability_take)
def take_Sim(r, o, outcome):
    if outcome == 0:
        ape.state.pos[o] = r
        ape.state.load[r] = o
        res = SUCCESS
    else:
        res = FAILURE
    return res

def put(r, o):
    ape.state.pos.AcquireLock(o)
    if ape.state.pos[o] == r:
        start = globalTimer.GetTime()
        ape.state.loc.AcquireLock(r)
        ape.state.load.AcquireLock(r)
        while(globalTimer.IsCommandExecutionOver('put', start) == False):
            pass
        gui.Simulate("Robot %s has put object %s at location %d\n" %(r,o,ape.state.loc[r]))
        ape.state.pos[o] = ape.state.loc[r]
        ape.state.load[r] = NIL
        ape.state.loc.ReleaseLock(r)
        ape.state.load.ReleaseLock(r)
        res = SUCCESS
    else:
        gui.Simulate("Object %s is not with robot %s\n" %(o,r))
        res = FAILURE
    ape.state.pos.ReleaseLock(o)
    return res

def GetProbability_put(r, o):
    if ape.state.pos[o] == r:
        return [0.9, 0.1]
    else:
        return [0.1, 0.9]

ape.declare_prob(put, GetProbability_put)
def put_Sim(r, o, outcome):
    if outcome == 0:
        ape.state.pos[o] = ape.state.loc[r]
        ape.state.load[r] = NIL
        res = SUCCESS
    else:
        res = FAILURE
    return res

def charge(r, c):
    ape.state.loc.AcquireLock(r)
    ape.state.pos.AcquireLock(c)
    if ape.state.loc[r] == ape.state.pos[c] or ape.state.pos[c] == r:
        ape.state.charge.AcquireLock(r)
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('charge', start) == False):
            pass
        ape.state.charge[r] = 4
        gui.Simulate("Robot %s is fully charged\n" %r)
        ape.state.charge.ReleaseLock(r)
        res = SUCCESS
    else:
        gui.Simulate("Robot %s is not in the charger's location or it doesn't have the charger with it\n" %r)
        res = FAILURE
    ape.state.loc.ReleaseLock(r)
    ape.state.pos.ReleaseLock(c)
    return res

def GetProbability_charge(r, c):
    if ape.state.loc[r] == ape.state.pos[c] or ape.state.pos[c] == r:
        return [0.8, 0.2]
    else:
        return [0.1, 0.9]

ape.declare_prob(charge, GetProbability_charge)
def charge_Sim(r, c, outcome):
    if outcome == 0:
        ape.state.charge[r] = 4
        res = SUCCESS
    else:
        res = FAILURE
    return res

def moveCharger(c, l):
    #start = globalTimer.GetTime()
    #while(globalTimer.IsCommandExecutionOver('moveCharger', start) == False):
    #	pass
    ape.state.pos.AcquireLock(c)
    gui.Simulate("Charger %s is moved to location %s\n" %(c,l))
    ape.state.pos[c] = l
    ape.state.pos.ReleaseLock(c)
    return SUCCESS

def GetProbability_moveCharger(c, l):
    return [1]

ape.declare_prob(moveCharger, GetProbability_moveCharger)
def moveCharger_Sim(c, l, outcome):
    ape.state.pos[c] = l
    return SUCCESS

def moveToEmergency(r, l1, l2, dist):
    ape.state.loc.AcquireLock(r)
    ape.state.charge.AcquireLock(r)
    if l1 == l2:
        gui.Simulate("Robot %s is already at location %s\n" %(r, l2))
        res = SUCCESS
    elif ape.state.loc[r] == l1 and ape.state.charge[r] >= dist:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('move', start) == False):
           pass
        gui.Simulate("Robot %s has moved from %d to %d\n" %(r, l1, l2))
        ape.state.loc[r] = l2
        ape.state.charge[r] = ape.state.charge[r] - dist
        res = SUCCESS
    elif ape.state.loc[r] != l1 and ape.state.charge[r] >= dist:
        gui.Simulate("Robot %s is not in location %d\n" %(r, l1))
        res = FAILURE
    elif ape.state.loc[r] == l1 and ape.state.charge[r] < dist:
        gui.Simulate("Robot %s does not have enough charge to move :(\n" %r)
        ape.state.charge[r] = 0 # should we do this?
        res = FAILURE
    else:
        gui.Simulate("Robot %s is not at location %s and it doesn't have enough charge!\n" %(r, l1))
        res = FAILURE
    ape.state.loc.ReleaseLock(r)
    ape.state.charge.ReleaseLock(r)
    if res == FAILURE:
        ape.state.emergencyHandling.AcquireLock(r)
        ape.state.emergencyHandling[r] = False
        ape.state.emergencyHandling.ReleaseLock(r)
    return res

def GetProbability_moveToEmergency(r, l1, l2, dist):
    if l1 == l2:
        return [0.8, 0.1, 0, 0.1, 0]
    elif ape.state.loc[r] == l1 and ape.state.charge[r] >= dist:
        return [0.1, 0.7, 0.1, 0.1, 0]
    elif ape.state.loc[r] != l1 and ape.state.charge[r] >= dist:
        return [0.1, 0.1, 0.6, 0.1, 0.1]
    elif ape.state.loc[r] == l1 and ape.state.charge[r] < dist:
        return [0.1, 0.1, 0.1, 0.5, 0.2]
    else:
        return [0.1, 0.1, 0.1, 0.1, 0.6]

ape.declare_prob(moveToEmergency, GetProbability_moveToEmergency)
def moveToEmergency_Sim(r, l1, l2, dist, outcome):
    if outcome == 0:
        res = SUCCESS
    elif outcome == 1:
        ape.state.loc[r] = l2
        ape.state.charge[r] = ape.state.charge[r] - dist
        res = SUCCESS
    elif outcome == 2:
        res = FAILURE
    elif outcome == 3:
        ape.state.charge[r] = 0 # should we do this?
        res = FAILURE
    else:
        res = FAILURE
    if res == FAILURE:
        ape.state.emergencyHandling[r] = False
    return res

def perceive(l):
    ape.state.view.AcquireLock(l)
    if ape.state.view[l] == False:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('perceive', start) == False):
            pass
        for c in ape.state.containers[l]:
            ape.state.pos.AcquireLock(c)
            ape.state.pos[c] = l
            ape.state.pos.ReleaseLock(c)
        ape.state.view[l] = True
        gui.Simulate("Perceived location %d\n" %l)
    else:
        gui.Simulate("Already perceived\n")
    ape.state.view.ReleaseLock(l)

    count = len(list(key for key in ape.state.view if ape.state.view[key] == True))
    total = len(rv.LOCATIONS)
    if count != total:
        for loc in rv.LOCATIONS:
            for obj in rv.OBJECTS:
                if ape.state.pos[obj] == UNK:
                    ape.UpdatePerceiveProb(perceive, loc, obj, 1/(total-count))
                elif ape.state.pos[obj] == loc:
                    ape.UpdatePerceiveProb(perceive, loc, obj, 1)
                else:
                    ape.UpdatePerceiveProb(perceive, loc, obj, 0)
    return SUCCESS

p_perceive={}
def InitProb():
    for loc in rv.LOCATIONS:
        p_perceive[loc] = {}
        for obj in rv.OBJECTS:
            p = 1/len(rv.LOCATIONS)
            p_perceive[loc][obj] = [p, 1 - p]
    ape.declare_prob(perceive, p_perceive)

#def UpdatePerceiveProb():
#    p_perceive=[]
#    for i in range(0, rv.OBJECTCOUNT + 1):
#        p_perceive.append()

ape.AddCommandToSpecialList(perceive)

def perceive_Sim(l, outcome):
    ape.state.view[l] = True
    for obj in outcome:
        ape.state.pos[obj] = l
    return SUCCESS

def MoveTo_Method1(r, l):
    x = ape.state.loc[r]
    dist = CR_GETDISTANCE(x, l)
    if ape.state.charge[r] >= dist:
        ape.do_task('nonEmergencyMove', r, x, l, dist)
        res = SUCCESS
    else:
        gui.Simulate("Robot %s does not have enough charge to move\n" %(r))
        res = FAILURE
    return res

def move(r, l1, l2, dist):
    ape.state.emergencyHandling.AcquireLock(r)
    if ape.state.emergencyHandling[r] == False:
        ape.state.loc.AcquireLock(r)
        ape.state.charge.AcquireLock(r)
        if l1 == l2:
            gui.Simulate("Robot %s is already at location %s\n" %(r, l2))
            res = SUCCESS
        elif ape.state.loc[r] == l1 and ape.state.charge[r] >= dist:
            start = globalTimer.GetTime()
            while(globalTimer.IsCommandExecutionOver('move', start) == False):
               pass
            gui.Simulate("Robot %s has moved from %d to %d\n" %(r, l1, l2))
            ape.state.loc[r] = l2
            ape.state.charge[r] = ape.state.charge[r] - dist
            res = SUCCESS
        elif ape.state.loc[r] != l1 and ape.state.charge[r] >= dist:
            gui.Simulate("Robot %s is not in location %d\n" %(r, l1))
            res = FAILURE
        elif ape.state.loc[r] == l1 and ape.state.charge[r] < dist:
            gui.Simulate("Robot %s does not have enough charge to move :(\n" %r)
            #ape.state.charge[r] = 0 # should we do this?
            res = FAILURE
        else:
            gui.Simulate("Robot %s is not at location %s and it doesn't have enough charge!\n" %(r, l1))
            res = FAILURE
        ape.state.loc.ReleaseLock(r)
        ape.state.charge.ReleaseLock(r)
    else:
        gui.Simulate("Robot is addressing emergency so it cannot move.\n")
        res = FAILURE
    ape.state.emergencyHandling.ReleaseLock(r)
    return res

def GetProbability_move(r, l1, l2, dist):
    if ape.state.emergencyHandling[r] == False:
        if l1 == l2:
            return [0.7, 0.1, 0.1, 0.1]
        elif ape.state.loc[r] == l1 and ape.state.charge[r] >= dist:
            return [0.1, 0.7, 0.1, 0.1]
        elif ape.state.loc[r] != l1 and ape.state.charge[r] >= dist:
            return [0.1, 0.1, 0.7, 0.1]
        elif ape.state.loc[r] == l1 and ape.state.charge[r] < dist:
            return [0.1, 0.1, 0.1, 0.7]
        else:
            return [0.1, 0.1, 0.1, 0.7]
    else:
        return [0.1, 0.1, 0.1, 0.7]

ape.declare_prob(move, GetProbability_move)
def move_Sim(r, l1, l2, dist, outcome):
    if outcome == 0:
        res = SUCCESS
    elif outcome == 1:
        if ape.state.charge[r] - dist > 0:
            ape.state.loc[r] = l2 
            ape.state.charge[r] = ape.state.charge[r] - dist
            res = SUCCESS
        else:
            res = FAILURE
    elif outcome == 2:
        res = FAILURE
    elif outcome == 3:
        ape.state.charge[r] = 0 # should we do this?
        res = FAILURE
    return res

def addressEmergency(r, l, i):
    ape.state.loc.AcquireLock(r)
    ape.state.emergencyHandling.AcquireLock(r)
    if ape.state.loc[r] == l:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('addressEmergency', start) == False):
            pass
        gui.Simulate("Robot %s has addressed emergency %d\n" %(r, i))
        res = SUCCESS
    else:
        gui.Simulate("Robot %s has failed to address emergency %d\n" %(r, i))
        res = FAILURE
    ape.state.emergencyHandling[r] = False
    ape.state.loc.ReleaseLock(r)
    ape.state.emergencyHandling.ReleaseLock(r)
    return res

def GetProbability_addressEmergency(r, l, i):
    if ape.state.loc[r] == l:
        return [0.8, 0.2]
    else:
        return [0.2, 0.8]

ape.declare_prob(addressEmergency, GetProbability_addressEmergency)
def addressEmergency_Sim(r, l, i, outcome):
    if outcome == 0:
        res = SUCCESS
    else:
        res = FAILURE
    ape.state.emergencyHandling[r] = False
    return res

def wait(r):
    while(ape.state.emergencyHandling[r] == True):
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('wait', start) == False):
            pass
        gui.Simulate("Robot %s is waiting for emergency to be over\n" %r)
    return SUCCESS

def GetProbability_wait(r):
    return [1]

ape.declare_prob(wait, GetProbability_wait)
def wait_Sim(r, outcome):
    ape.state.emergencyHandling[r] = False
    return SUCCESS

# def Recharge_Method1(r, c):
#     if ape.state.loc[r] != ape.state.pos[c] and ape.state.pos[c] != r:
#         if ape.state.pos[c] in rv.LOCATIONS:
#             ape.do_task('moveTo', r, ape.state.pos[c])
#         else:
#             gui.Simulate("%s cannot find charger %s\n" %(r, c))
#             return FAILURE
#     ape.do_command(charge, r, c)
#     return SUCCESS

# def Recharge_Method2(r, c):
#     if ape.state.loc[r] != ape.state.pos[c] and ape.state.pos[c] != r:
#         if ape.state.pos[c] in rv.LOCATIONS:
#             ape.do_task('moveTo', r, ape.state.pos[c])
#         else:
#             gui.Simulate("%s cannot find charger %s\n" %(r, c))
#             return FAILURE
#     ape.do_command(charge, r, c)
#     ape.do_command(take, r, c)
#     return SUCCESS

def Recharge_Method3(r, c):
    if ape.state.loc[r] != ape.state.pos[c] and ape.state.pos[c] != r:
        if ape.state.pos[c] in rv.LOCATIONS:
            ape.do_task('moveTo', r, ape.state.pos[c])
        else:
            robot = ape.state.pos[c]
            ape.do_command(put, robot, c)
            ape.do_task('moveTo', r, ape.state.pos[c])
    ape.do_command(charge, r, c)
    if ape.state.load[r] == NIL:
        ape.do_command(take, r, c)
    return SUCCESS

def Recharge_Method2(r, c):
    if ape.state.loc[r] != ape.state.pos[c] and ape.state.pos[c] != r:
        if ape.state.pos[c] in rv.LOCATIONS:
            ape.do_task('moveTo', r, ape.state.pos[c])
        else:
            robot = ape.state.pos[c]
            ape.do_command(put, robot, c)
            ape.do_task('moveTo', r, ape.state.pos[c])
    ape.do_command(charge, r, c)
    return SUCCESS

def Recharge_Method1(r, c):
    robot = NIL
    if ape.state.loc[r] != ape.state.pos[c] and ape.state.pos[c] != r:
        if ape.state.pos[c] in rv.LOCATIONS:
            ape.do_task('moveTo', r, ape.state.pos[c])
        else:
            robot = ape.state.pos[c]
            ape.do_command(put, robot, c)
            ape.do_task('moveTo', r, ape.state.pos[c])
    ape.do_command(charge, r, c)
    if robot != NIL and ape.state.load[robot] != NIL and ape.state.pos[robot] == ape.state.loc[c]:
        ape.do_command(take, robot, c)
    return SUCCESS

def Search_Method1(r, o):
    if ape.state.pos[o] == UNK:
        toBePerceived = NIL
        for l in rv.LOCATIONS:
            if ape.state.view[l] == False:
                toBePerceived = l
                break

        if toBePerceived != NIL:
            ape.do_task('moveTo', r, toBePerceived)
            ape.do_command(perceive, toBePerceived)
            if ape.state.pos[o] == toBePerceived:
                if ape.state.load[r] != NIL:
                    ape.do_command(put, r, ape.state.load[r])
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
    if ape.state.pos[o] == UNK:
        toBePerceived = NIL
        for l in rv.LOCATIONS:
            if ape.state.view[l] == False:
                toBePerceived = l
                break

        if toBePerceived != NIL:
            ape.do_task('recharge', r, 'c1') # is this allowed?
            ape.do_task('moveTo', r, toBePerceived)
            ape.do_command(perceive, toBePerceived)
            if ape.state.pos[o] == toBePerceived:
                if ape.state.load[r] != NIL:
                    ape.do_command(put, r, ape.state.load[r])
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
    pos_o = ape.state.pos[o]
    if pos_o == UNK:
        ape.do_task('search', r, o)
    elif ape.state.loc[r] == pos_o:
        if ape.state.load[r] != NIL:
            ape.do_command(put, r, ape.state.load[r])
        ape.do_command(take, r, o)
    else:
        ape.do_task('moveTo', r, pos_o)
        if ape.state.load[r] != NIL:
            ape.do_command(put, r, ape.state.load[r])
        ape.do_command(take, r, o)
    return SUCCESS

def Fetch_Method2(r, o):
    pos_o = ape.state.pos[o]
    if pos_o == UNK:
        ape.do_task('search', r, o)
    elif ape.state.loc[r] == pos_o:
        if ape.state.load[r] != NIL:
            ape.do_command(put, r, ape.state.load[r])
        ape.do_command(take, r, o)
    else:
        ape.do_task('recharge', r, 'c1')
        ape.do_task('moveTo', r, pos_o)
        if ape.state.load[r] != NIL:
            ape.do_command(put, r, ape.state.load[r])
        ape.do_command(take, r, o)
    return SUCCESS

def RelocateCharger(c, l):
    res = SUCCESS
    for r in ape.state.charge:
        if ape.state.charge[r] != 4:
            res = FAILURE

    if res == SUCCESS:
        moveCharger(c, l)
    else:
        gui.Simulate("Cannot move charger now, robots might need it\n")

    return res

def Emergency_Method1(r, l, i):
    if ape.state.emergencyHandling[r] == False:
        ape.state.emergencyHandling[r] = True
        load_r = ape.state.load[r]
        if load_r != NIL:
            ape.do_command(put, r, load_r, ape.state.loc[r])
        l1 = ape.state.loc[r]
        dist = CR_GETDISTANCE(l1, l)
        ape.do_command(moveToEmergency, r, l1, l, dist)
        ape.do_command(addressEmergency, r, l, i)
        res = SUCCESS
    else:
        gui.Simulate("%r is already busy handling another emergency\n" %r)
        res = FAILURE
    return res

# def NonEmergencyMove_Method1(r, l1, l2, dist):
#     if ape.state.emergencyHandling[r] == False:
#         ape.do_command(move, r, l1, l2, dist)
#         res = SUCCESS
#     else:
#         gui.Simulate("Move failed, trying to do a non emergency move for a robot handling emergency\n")
#         res = FAILURE
#     return res

def NonEmergencyMove_Method1(r, l1, l2, dist):
    if ape.state.emergencyHandling[r] == False:
        ape.do_command(move, r, l1, l2, dist)
    else:
        ape.do_command(wait, r)
        ape.do_command(move, r, l1, l2, dist)
    return SUCCESS

rv = RV()
ape.declare_commands([put, take, perceive, charge, move, moveCharger, moveToEmergency, addressEmergency, wait],
                      [put_Sim, take_Sim, perceive_Sim, charge_Sim, move_Sim, moveCharger_Sim, moveToEmergency_Sim, addressEmergency_Sim, wait_Sim])

ape.declare_methods('search', Search_Method1, Search_Method2)
ape.declare_methods('fetch', Fetch_Method1, Fetch_Method2)
ape.declare_methods('recharge', Recharge_Method2, Recharge_Method3, Recharge_Method1)
ape.declare_methods('moveTo', MoveTo_Method1)
ape.declare_methods('emergency', Emergency_Method1)
ape.declare_methods('nonEmergencyMove', NonEmergencyMove_Method1)
#ape.declare_methods('relocateCharger', RelocateCharger_Method1)

