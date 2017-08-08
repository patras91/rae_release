__author__ = 'patras'

'''A robot is searching for an object in the environment consisting of n locations.
It has a battery that needs to be recharged after some moves.
A move consumes 1/4 of the battery capacity.
Recharger is only at one location'''

from domain_constants import *
import rae1
import gui
from timer import globalTimer

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

def moveCharger(c, l):
    #start = globalTimer.GetTime()
    #while(globalTimer.IsCommandExecutionOver('moveCharger', start) == False):
	#	pass
    rae1.state.pos.AcquireLock(c)
    gui.Simulate("Charger %s is moved to location %s\n" %(c,l))
    rae1.state.pos[c] = l
    rae1.state.pos.ReleaseLock(c)
    return SUCCESS

def move(r, l1, l2, dist):
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

def MoveTo_Method1(r, l, stackid):
    x = rae1.state.loc[r]
    c = rae1.state.charge[r]
    dist = GETDISTANCE(x, l)
    if c >= dist:
        rae1.do_command(move, r, x, l, dist, stackid)
        res = SUCCESS
    else:
        gui.Simulate("Insufficient charge! only %.2f%%. Robot %s cannot move\n" %(c * 100 / 4, r))
        res = FAILURE
    return res

def Recharge_Method1(r, c, stackid):
    if rae1.state.loc[r] != rae1.state.pos[c] and rae1.state.pos[c] != r:
        rae1.do_task('moveTo', r, rae1.state.pos[c], stackid)
    rae1.do_command(charge, r, c, stackid)
    return SUCCESS

def Recharge_Method2(r, c, stackid):
    if rae1.state.loc[r] != rae1.state.pos[c] and rae1.state.pos[c] != r:
        rae1.do_task('moveTo', r, rae1.state.pos[c], stackid)

    rae1.do_command(charge, r, c, stackid)
    rae1.do_command(take, r, c, stackid)
    return SUCCESS

def Search_Method1(r, o, stackid):
    if rae1.state.pos[o] == UNK:
        toBePerceived = NIL
        for l in LOCATIONS_CHARGEABLEROBOT:
            if rae1.state.view[l] == False:
                toBePerceived = l
                break

        if toBePerceived != NIL:
            rae1.do_task('moveTo', r, toBePerceived, stackid)
            rae1.do_command(perceive, toBePerceived, stackid)
            if rae1.state.pos[o] == toBePerceived:
                if rae1.state.load[r] != NIL:
                    rae1.do_command(put, r, rae1.state.load[r], stackid)
                rae1.do_command(take, r, o, stackid)
            else:
                rae1.do_task('search', r, o, stackid)
            res = SUCCESS
        else:
            gui.Simulate("Failed to search %s" %o)
            res = FAILURE
    else:
        gui.Simulate("Position of %s is already known\n" %o)
        res = SUCCESS
    return res

def Search_Method2(r, o, stackid):
    if rae1.state.pos[o] == UNK:
        toBePerceived = NIL
        for l in LOCATIONS_CHARGEABLEROBOT:
            if rae1.state.view[l] == False:
                toBePerceived = l
                break

        if toBePerceived != NIL:
            Recharge_Method1(r, 'c1', stackid) # is this allowed?
            rae1.do_task('moveTo', r, toBePerceived, stackid)
            rae1.do_command(perceive, toBePerceived, stackid)
            if rae1.state.pos[o] == toBePerceived:
                if rae1.state.load[r] != NIL:
                    rae1.do_command(put, r, rae1.state.load[r], stackid)
                rae1.do_command(take, r, o, stackid)
            else:
                rae1.do_task('search', r, o, stackid)
            res = SUCCESS
        else:
            gui.Simulate("Failed to search %s" %o)
            res = FAILURE
    else:
        gui.Simulate("Position of %s is already known\n" %o)
        res = SUCCESS
    return res

def Fetch_Method1(r, o, stackid):
    pos_o = rae1.state.pos[o]
    if pos_o == UNK:
        rae1.do_task('search', r, o, stackid)
    elif rae1.state.loc[r] == pos_o:
        rae1.do_command(take, r, o, stackid)
    else:
        rae1.do_task('moveTo', r, pos_o,  stackid)
        rae1.do_command(take, r, o, stackid)
    return SUCCESS

def Fetch_Method2(r, o, stackid):
    pos_o = rae1.state.pos[o]
    if pos_o == UNK:
        rae1.do_task('search', r, o, stackid)
    elif rae1.state.loc[r] == pos_o:
        rae1.do_command(take, r, o, stackid)
    else:
        rae1.do_task('recharge', r, 'c1', stackid)
        rae1.do_task('moveTo', r, pos_o, stackid)
        rae1.do_command(take, r, o, stackid)
    return SUCCESS

def RelocateCharger_Method1(c, l, stackid):
    res = SUCCESS
    for r in rae1.state.charge:
        if rae1.state.charge[r] != 4:
            res = FAILURE

    if res == SUCCESS:
        rae1.do_command(moveCharger, c, l, stackid)
    else:
        gui.Simulate("Cannot move charger now, robots might need it\n")

    return res

def chargeableRobot_init():
    rae1.declare_commands(put, take, perceive, charge, move, moveCharger)
    print('\n')
    rae1.print_commands()

    rae1.declare_methods('search', Search_Method1, Search_Method2)
    rae1.declare_methods('fetch', Fetch_Method1, Fetch_Method2)
    rae1.declare_methods('recharge', Recharge_Method1, Recharge_Method2)
    rae1.declare_methods('moveTo', MoveTo_Method1)
    rae1.declare_methods('relocateCharger', RelocateCharger_Method1)
    print('\n')
    rae1.print_methods()

    print('\n*********************************************************')
    print("* Call rae1 on chargeable robot domain.")
    print("* For a different amout of printout, try verbosity(0), verbosity(1), or verbosity(2).")
    print('*********************************************************\n')

    rae1.state.loc = {'r1': 1}
    rae1.state.charge = {'r1':4}
    rae1.state.load = {'r1': NIL}
    rae1.state.pos = {'c1': 7, 'o1': UNK, 'o2': UNK}
    rae1.state.containers = {1:[], 2:['o2'], 3:[], 4:[], 5:['o1'], 6:[], 7:[], 8:[]}

    rae1.state.view = {}
    for l in LOCATIONS_CHARGEABLEROBOT:
        rae1.state.view[l] = False