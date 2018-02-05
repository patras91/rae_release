__author__ = 'patras'

'''A robot is searching for an object in the environment consisting of n locations.
It has a battery that needs to be recharged after some moves.
A move consumes 1/4 of the battery capacity.
Recharger is only at one location'''

from domain_constants import *
import rae1
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
    rae1.state.load.AcquireLock(r)
    if rae1.state.load[r] == NIL:
        rae1.state.pos.AcquireLock(o)
        if rae1.state.loc[r] == rae1.state.pos[o]:
            start = globalTimer.GetTime()
            while(globalTimer.IsCommandExecutionOver('take', start) == False):
                pass
            gui.Simulate("Robot %s has picked up object %s\n" %(r, o))
            rae1.state.pos[o] = r
            rae1.state.load[r] = o
            res = SUCCESS
        else:
            gui.Simulate("Robot %s is not at object %s's location\n" %(r, o))
            res = FAILURE
        rae1.state.pos.ReleaseLock(o)
    else:
        gui.Simulate("Robot %s is not free to take anything\n" %r)
        res = FAILURE
    rae1.state.load.ReleaseLock(r)
    return res

def take_Sim(r, o):
    rae1.state.load.AcquireLock(r)
    if rae1.state.load[r] == NIL:
        rae1.state.pos.AcquireLock(o)
        if rae1.state.loc[r] == rae1.state.pos[o]:
            start = globalTimer.GetTime()
            while(globalTimer.IsCommandExecutionOver('take', start) == False):
                pass
            gui.Simulate("Robot %s has picked up object %s\n" %(r, o))
            rae1.state.pos[o] = r
            rae1.state.load[r] = o
            res = SUCCESS
        else:
            gui.Simulate("Robot %s is not at object %s's location\n" %(r, o))
            res = FAILURE
        rae1.state.pos.ReleaseLock(o)
    else:
        gui.Simulate("Robot %s is not free to take anything\n" %r)
        res = FAILURE
    rae1.state.load.ReleaseLock(r)
    return res

def put(r, o):
    rae1.state.pos.AcquireLock(o)
    if rae1.state.pos[o] == r:
        start = globalTimer.GetTime()
        rae1.state.loc.AcquireLock(r)
        rae1.state.load.AcquireLock(r)
        while(globalTimer.IsCommandExecutionOver('put', start) == False):
            pass
        gui.Simulate("Robot %s has put object %s at location %d\n" %(r,o,rae1.state.loc[r]))
        rae1.state.pos[o] = rae1.state.loc[r]
        rae1.state.load[r] = NIL
        rae1.state.loc.ReleaseLock(r)
        rae1.state.load.ReleaseLock(r)
        res = SUCCESS
    else:
        gui.Simulate("Object %s is not with robot %s\n" %(o,r))
        res = FAILURE
    rae1.state.pos.ReleaseLock(o)
    return res

def put_Sim(r, o):
    rae1.state.pos.AcquireLock(o)
    if rae1.state.pos[o] == r:
        start = globalTimer.GetTime()
        rae1.state.loc.AcquireLock(r)
        rae1.state.load.AcquireLock(r)
        while(globalTimer.IsCommandExecutionOver('put', start) == False):
            pass
        gui.Simulate("Robot %s has put object %s at location %d\n" %(r,o,rae1.state.loc[r]))
        rae1.state.pos[o] = rae1.state.loc[r]
        rae1.state.load[r] = NIL
        rae1.state.loc.ReleaseLock(r)
        rae1.state.load.ReleaseLock(r)
        res = SUCCESS
    else:
        gui.Simulate("Object %s is not with robot %s\n" %(o,r))
        res = FAILURE
    rae1.state.pos.ReleaseLock(o)
    return res

def charge(r, c):
    rae1.state.loc.AcquireLock(r)
    rae1.state.pos.AcquireLock(c)
    if rae1.state.loc[r] == rae1.state.pos[c] or rae1.state.pos[c] == r:
        rae1.state.charge.AcquireLock(r)
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('charge', start) == False):
            pass
        rae1.state.charge[r] = 4
        gui.Simulate("Robot %s is fully charged\n" %r)
        rae1.state.charge.ReleaseLock(r)
        res = SUCCESS
    else:
        gui.Simulate("Robot %s is not in the charger's location or it doesn't have the charger with it\n" %r)
        res = FAILURE
    rae1.state.loc.ReleaseLock(r)
    rae1.state.pos.ReleaseLock(c)
    return res

def charge_Sim(r, c):
    rae1.state.loc.AcquireLock(r)
    rae1.state.pos.AcquireLock(c)
    if rae1.state.loc[r] == rae1.state.pos[c] or rae1.state.pos[c] == r:
        rae1.state.charge.AcquireLock(r)
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('charge', start) == False):
            pass
        rae1.state.charge[r] = 4
        gui.Simulate("Robot %s is fully charged\n" %r)
        rae1.state.charge.ReleaseLock(r)
        res = SUCCESS
    else:
        gui.Simulate("Robot %s is not in the charger's location or it doesn't have the charger with it\n" %r)
        res = FAILURE
    rae1.state.loc.ReleaseLock(r)
    rae1.state.pos.ReleaseLock(c)
    return res

def moveCharger(c, l):
    #start = globalTimer.GetTime()
    #while(globalTimer.IsCommandExecutionOver('moveCharger', start) == False):
    #	pass
    rae1.state.pos.AcquireLock(c)
    gui.Simulate("Charger %s is moved to location %s\n" %(c,l))
    rae1.state.pos[c] = l
    rae1.state.pos.ReleaseLock(c)
    return SUCCESS

def moveCharger_Sim(c, l):
    #start = globalTimer.GetTime()
    #while(globalTimer.IsCommandExecutionOver('moveCharger', start) == False):
    #	pass
    rae1.state.pos.AcquireLock(c)
    gui.Simulate("Charger %s is moved to location %s\n" %(c,l))
    rae1.state.pos[c] = l
    rae1.state.pos.ReleaseLock(c)
    return SUCCESS

def moveToEmergency(r, l1, l2, dist):
    rae1.state.loc.AcquireLock(r)
    rae1.state.charge.AcquireLock(r)
    if l1 == l2:
        gui.Simulate("Robot %s is already at location %s\n" %(r, l2))
        res = SUCCESS
    elif rae1.state.loc[r] == l1 and rae1.state.charge[r] >= dist:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('move', start) == False):
           pass
        gui.Simulate("Robot %s has moved from %d to %d\n" %(r, l1, l2))
        rae1.state.loc[r] = l2
        rae1.state.charge[r] = rae1.state.charge[r] - dist
        res = SUCCESS
    elif rae1.state.loc[r] != l1 and rae1.state.charge[r] >= dist:
        gui.Simulate("Robot %s is not in location %d\n" %(r, l1))
        res = FAILURE
    elif rae1.state.loc[r] == l1 and rae1.state.charge[r] < dist:
        gui.Simulate("Robot %s does not have enough charge to move :(\n" %r)
        rae1.state.charge[r] = 0 # should we do this?
        res = FAILURE
    else:
        gui.Simulate("Robot %s is not at location %s and it doesn't have enough charge!\n" %(r, l1))
        res = FAILURE
    rae1.state.loc.ReleaseLock(r)
    rae1.state.charge.ReleaseLock(r)
    if res == FAILURE:
        rae1.state.emergencyHandling.AcquireLock(r)
        rae1.state.emergencyHandling[r] = False
        rae1.state.emergencyHandling.ReleaseLock(r)
    return res

def moveToEmergency_Sim(r, l1, l2, dist):
    rae1.state.loc.AcquireLock(r)
    rae1.state.charge.AcquireLock(r)
    if l1 == l2:
        gui.Simulate("Robot %s is already at location %s\n" %(r, l2))
        res = SUCCESS
    elif rae1.state.loc[r] == l1 and rae1.state.charge[r] >= dist:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('move', start) == False):
           pass
        gui.Simulate("Robot %s has moved from %d to %d\n" %(r, l1, l2))
        rae1.state.loc[r] = l2
        rae1.state.charge[r] = rae1.state.charge[r] - dist
        res = SUCCESS
    elif rae1.state.loc[r] != l1 and rae1.state.charge[r] >= dist:
        gui.Simulate("Robot %s is not in location %d\n" %(r, l1))
        res = FAILURE
    elif rae1.state.loc[r] == l1 and rae1.state.charge[r] < dist:
        gui.Simulate("Robot %s does not have enough charge to move :(\n" %r)
        rae1.state.charge[r] = 0 # should we do this?
        res = FAILURE
    else:
        gui.Simulate("Robot %s is not at location %s and it doesn't have enough charge!\n" %(r, l1))
        res = FAILURE
    rae1.state.loc.ReleaseLock(r)
    rae1.state.charge.ReleaseLock(r)
    if res == FAILURE:
        rae1.state.emergencyHandling.AcquireLock(r)
        rae1.state.emergencyHandling[r] = False
        rae1.state.emergencyHandling.ReleaseLock(r)
    return res

def perceive(l):
    rae1.state.view.AcquireLock(l)
    if rae1.state.view[l] == False:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('perceive', start) == False):
            pass
        for c in rae1.state.containers[l]:
            rae1.state.pos.AcquireLock(c)
            rae1.state.pos[c] = l
            rae1.state.pos.ReleaseLock(c)
        rae1.state.view[l] = True
        gui.Simulate("Perceived location %d\n" %l)
    else:
        gui.Simulate("Already perceived\n")
    rae1.state.view.ReleaseLock(l)
    return SUCCESS

def perceive_Sim(l):
    rae1.state.view.AcquireLock(l)
    if rae1.state.view[l] == False:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('perceive', start) == False):
            pass
        for c in rae1.state.containers[l]:
            rae1.state.pos.AcquireLock(c)
            rae1.state.pos[c] = l
            rae1.state.pos.ReleaseLock(c)
        rae1.state.view[l] = True
        gui.Simulate("Perceived location %d\n" %l)
    else:
        gui.Simulate("Already perceived\n")
    rae1.state.view.ReleaseLock(l)
    return SUCCESS

def MoveTo_Method1(r, l):
    x = rae1.state.loc[r]
    dist = CR_GETDISTANCE(x, l)
    rae1.do_task('nonEmergencyMove', r, x, l, dist)
    res = SUCCESS
    return res

def move(r, l1, l2, dist):
    rae1.state.emergencyHandling.AcquireLock(r)
    if rae1.state.emergencyHandling[r] == False:
        rae1.state.loc.AcquireLock(r)
        rae1.state.charge.AcquireLock(r)
        if l1 == l2:
            gui.Simulate("Robot %s is already at location %s\n" %(r, l2))
            res = SUCCESS
        elif rae1.state.loc[r] == l1 and rae1.state.charge[r] >= dist:
            start = globalTimer.GetTime()
            while(globalTimer.IsCommandExecutionOver('move', start) == False):
               pass
            gui.Simulate("Robot %s has moved from %d to %d\n" %(r, l1, l2))
            rae1.state.loc[r] = l2
            rae1.state.charge[r] = rae1.state.charge[r] - dist
            res = SUCCESS
        elif rae1.state.loc[r] != l1 and rae1.state.charge[r] >= dist:
            gui.Simulate("Robot %s is not in location %d\n" %(r, l1))
            res = FAILURE
        elif rae1.state.loc[r] == l1 and rae1.state.charge[r] < dist:
            gui.Simulate("Robot %s does not have enough charge to move :(\n" %r)
            rae1.state.charge[r] = 0 # should we do this?
            res = FAILURE
        else:
            gui.Simulate("Robot %s is not at location %s and it doesn't have enough charge!\n" %(r, l1))
            res = FAILURE
        rae1.state.loc.ReleaseLock(r)
        rae1.state.charge.ReleaseLock(r)
    else:
        gui.Simulate("Robot is addressing emergency so it cannot move.\n")
        res = FAILURE
    rae1.state.emergencyHandling.ReleaseLock(r)
    return res

def move_Sim(r, l1, l2, dist):
    rae1.state.emergencyHandling.AcquireLock(r)
    if rae1.state.emergencyHandling[r] == False:
        rae1.state.loc.AcquireLock(r)
        rae1.state.charge.AcquireLock(r)
        if l1 == l2:
            gui.Simulate("Robot %s is already at location %s\n" %(r, l2))
            res = SUCCESS
        elif rae1.state.loc[r] == l1 and rae1.state.charge[r] >= dist:
            start = globalTimer.GetTime()
            while(globalTimer.IsCommandExecutionOver('move', start) == False):
               pass
            gui.Simulate("Robot %s has moved from %d to %d\n" %(r, l1, l2))
            rae1.state.loc[r] = l2
            rae1.state.charge[r] = rae1.state.charge[r] - dist
            res = SUCCESS
        elif rae1.state.loc[r] != l1 and rae1.state.charge[r] >= dist:
            gui.Simulate("Robot %s is not in location %d\n" %(r, l1))
            res = FAILURE
        elif rae1.state.loc[r] == l1 and rae1.state.charge[r] < dist:
            gui.Simulate("Robot %s does not have enough charge to move :(\n" %r)
            rae1.state.charge[r] = 0 # should we do this?
            res = FAILURE
        else:
            gui.Simulate("Robot %s is not at location %s and it doesn't have enough charge!\n" %(r, l1))
            res = FAILURE
        rae1.state.loc.ReleaseLock(r)
        rae1.state.charge.ReleaseLock(r)
    else:
        gui.Simulate("Robot is addressing emergency so it cannot move.\n")
        res = FAILURE
    rae1.state.emergencyHandling.ReleaseLock(r)
    return res

def addressEmergency(r, l, i):
    rae1.state.loc.AcquireLock(r)
    rae1.state.emergencyHandling.AcquireLock(r)
    if rae1.state.loc[r] == l:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('addressEmergency', start) == False):
            pass
        gui.Simulate("Robot %s has addressed emergency %d\n" %(r, i))
        res = SUCCESS
    else:
        gui.Simulate("Robot %s has failed to address emergency %d\n" %(r, i))
        res = FAILURE
    rae1.state.emergencyHandling[r] = False
    rae1.state.loc.ReleaseLock(r)
    rae1.state.emergencyHandling.ReleaseLock(r)
    return res

def addressEmergency_Sim(r, l, i):
    rae1.state.loc.AcquireLock(r)
    rae1.state.emergencyHandling.AcquireLock(r)
    if rae1.state.loc[r] == l:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('addressEmergency', start) == False):
            pass
        gui.Simulate("Robot %s has addressed emergency %d\n" %(r, i))
        res = SUCCESS
    else:
        gui.Simulate("Robot %s has failed to address emergency %d\n" %(r, i))
        res = FAILURE
    rae1.state.emergencyHandling[r] = False
    rae1.state.loc.ReleaseLock(r)
    rae1.state.emergencyHandling.ReleaseLock(r)
    return res

def wait(r):
    while(rae1.state.emergencyHandling[r] == True):
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('wait', start) == False):
            pass
        gui.Simulate("Robot %s is waiting for emergency to be over\n" %r)
    return SUCCESS

def wait_Sim(r):
    start = globalTimer.GetTime()
    while(globalTimer.IsCommandExecutionOver('wait', start) == False):
        pass
    gui.Simulate("Robot %s is waiting for emergency to be over\n" %r)
    rae1.state.emergencyHandling.AcquireLock(r)
    rae1.state.emergencyHandling[r] = False
    rae1.state.emergencyHandling.ReleaseLock(r)

    return SUCCESS

# def Recharge_Method1(r, c):
#     if rae1.state.loc[r] != rae1.state.pos[c] and rae1.state.pos[c] != r:
#         if rae1.state.pos[c] in rv.LOCATIONS:
#             rae1.do_task('moveTo', r, rae1.state.pos[c])
#         else:
#             gui.Simulate("%s cannot find charger %s\n" %(r, c))
#             return FAILURE
#     rae1.do_command(charge, r, c)
#     return SUCCESS

# def Recharge_Method2(r, c):
#     if rae1.state.loc[r] != rae1.state.pos[c] and rae1.state.pos[c] != r:
#         if rae1.state.pos[c] in rv.LOCATIONS:
#             rae1.do_task('moveTo', r, rae1.state.pos[c])
#         else:
#             gui.Simulate("%s cannot find charger %s\n" %(r, c))
#             return FAILURE
#     rae1.do_command(charge, r, c)
#     rae1.do_command(take, r, c)
#     return SUCCESS

def Recharge_Method3(r, c):
    if rae1.state.loc[r] != rae1.state.pos[c] and rae1.state.pos[c] != r:
        if rae1.state.pos[c] in rv.LOCATIONS:
            rae1.do_task('moveTo', r, rae1.state.pos[c])
        else:
            robot = rae1.state.pos[c]
            rae1.do_command(put, robot, c)
            rae1.do_task('moveTo', r, rae1.state.pos[c])
    rae1.do_command(charge, r, c)
    rae1.do_command(take, r, c)
    return SUCCESS

def Recharge_Method2(r, c):
    if rae1.state.loc[r] != rae1.state.pos[c] and rae1.state.pos[c] != r:
        if rae1.state.pos[c] in rv.LOCATIONS:
            rae1.do_task('moveTo', r, rae1.state.pos[c])
        else:
            robot = rae1.state.pos[c]
            rae1.do_command(put, robot, c)
            rae1.do_task('moveTo', r, rae1.state.pos[c])
    rae1.do_command(charge, r, c)
    return SUCCESS

def Recharge_Method1(r, c):
    robot = NIL
    if rae1.state.loc[r] != rae1.state.pos[c] and rae1.state.pos[c] != r:
        if rae1.state.pos[c] in rv.LOCATIONS:
            rae1.do_task('moveTo', r, rae1.state.pos[c])
        else:
            robot = rae1.state.pos[c]
            rae1.do_command(put, robot, c)
            rae1.do_task('moveTo', r, rae1.state.pos[c])
    rae1.do_command(charge, r, c)
    if robot != NIL:
        rae1.do_command(take, robot, c)
    return SUCCESS

def Search_Method1(r, o):
    if rae1.state.pos[o] == UNK:
        toBePerceived = NIL
        for l in rv.LOCATIONS:
            if rae1.state.view[l] == False:
                toBePerceived = l
                break

        if toBePerceived != NIL:
            rae1.do_task('moveTo', r, toBePerceived)
            rae1.do_command(perceive, toBePerceived)
            if rae1.state.pos[o] == toBePerceived:
                if rae1.state.load[r] != NIL:
                    rae1.do_command(put, r, rae1.state.load[r])
                rae1.do_command(take, r, o)
            else:
                rae1.do_task('search', r, o)
            res = SUCCESS
        else:
            gui.Simulate("Failed to search %s" %o)
            res = FAILURE
    else:
        gui.Simulate("Position of %s is already known\n" %o)
        res = SUCCESS
    return res

def Search_Method2(r, o):
    if rae1.state.pos[o] == UNK:
        toBePerceived = NIL
        for l in rv.LOCATIONS:
            if rae1.state.view[l] == False:
                toBePerceived = l
                break

        if toBePerceived != NIL:
            Recharge_Method1(r, 'c1') # is this allowed?
            rae1.do_task('moveTo', r, toBePerceived)
            rae1.do_command(perceive, toBePerceived)
            if rae1.state.pos[o] == toBePerceived:
                if rae1.state.load[r] != NIL:
                    rae1.do_command(put, r, rae1.state.load[r])
                rae1.do_command(take, r, o)
            else:
                rae1.do_task('search', r, o)
            res = SUCCESS
        else:
            gui.Simulate("Failed to search %s" %o)
            res = FAILURE
    else:
        gui.Simulate("Position of %s is already known\n" %o)
        res = SUCCESS
    return res

def Fetch_Method1(r, o):
    pos_o = rae1.state.pos[o]
    if pos_o == UNK:
        rae1.do_task('search', r, o)
    elif rae1.state.loc[r] == pos_o:
        if rae1.state.load[r] != NIL:
            rae1.do_command(put, r, rae1.state.load[r])
        rae1.do_command(take, r, o)
    else:
        rae1.do_task('moveTo', r, pos_o)
        if rae1.state.load[r] != NIL:
            rae1.do_command(put, r, rae1.state.load[r])
        rae1.do_command(take, r, o)
    return SUCCESS

def Fetch_Method2(r, o):
    pos_o = rae1.state.pos[o]
    if pos_o == UNK:
        rae1.do_task('search', r, o)
    elif rae1.state.loc[r] == pos_o:
        if rae1.state.load[r] != NIL:
            rae1.do_command(put, r, rae1.state.load[r])
        rae1.do_command(take, r, o)
    else:
        rae1.do_task('recharge', r, 'c1')
        rae1.do_task('moveTo', r, pos_o)
        if rae1.state.load[r] != NIL:
            rae1.do_command(put, r, rae1.state.load[r])
        rae1.do_command(take, r, o)
    return SUCCESS

def RelocateCharger(c, l):
    res = SUCCESS
    for r in rae1.state.charge:
        if rae1.state.charge[r] != 4:
            res = FAILURE

    if res == SUCCESS:
        moveCharger(c, l)
    else:
        gui.Simulate("Cannot move charger now, robots might need it\n")

    return res

def Emergency_Method1(r, l, i):
    if rae1.state.emergencyHandling[r] == False:
        rae1.state.emergencyHandling[r] = True
        load_r = rae1.state.load[r]
        if load_r != NIL:
            rae1.do_command(put, r, load_r, rae1.state.loc[r])
        l1 = rae1.state.loc[r]
        dist = CR_GETDISTANCE(l1, l)
        rae1.do_command(moveToEmergency, r, l1, l, dist)
        rae1.do_command(addressEmergency, r, l, i)
        res = SUCCESS
    else:
        gui.Simulate("%r is already busy handling another emergency\n" %r)
        res = FAILURE
    return res

# def NonEmergencyMove_Method1(r, l1, l2, dist):
#     if rae1.state.emergencyHandling[r] == False:
#         rae1.do_command(move, r, l1, l2, dist)
#         res = SUCCESS
#     else:
#         gui.Simulate("Move failed, trying to do a non emergency move for a robot handling emergency\n")
#         res = FAILURE
#     return res

def NonEmergencyMove_Method1(r, l1, l2, dist):
    if rae1.state.emergencyHandling[r] == False:
        rae1.do_command(move, r, l1, l2, dist)
    else:
        rae1.do_command(wait, r)
        rae1.do_command(move, r, l1, l2, dist)
    return SUCCESS

rv = RV()
rae1.declare_commands([put, take, perceive, charge, move, moveCharger, moveToEmergency, addressEmergency, wait],
                      [put_Sim, take_Sim, perceive_Sim, charge_Sim, move_Sim, moveCharger_Sim, moveToEmergency_Sim, addressEmergency_Sim, wait_Sim])


rae1.declare_methods('search', Search_Method1, Search_Method2)
rae1.declare_methods('fetch', Fetch_Method1, Fetch_Method2)
rae1.declare_methods('recharge', Recharge_Method2, Recharge_Method3, Recharge_Method1)
rae1.declare_methods('moveTo', MoveTo_Method1)
rae1.declare_methods('emergency', Emergency_Method1)
rae1.declare_methods('nonEmergencyMove', NonEmergencyMove_Method1)
#rae1.declare_methods('relocateCharger', RelocateCharger_Method1)

