__author__ = 'patras'

'''A robot is searching for an object in the environment consisting of n locations.
It has a battery that needs to be recharged after some moves.
A move consumes 1/4 of the battery capacity.
Recharger is only at one location'''

from domain_constants import *
import rae1

def take(r, o):
    if rae1.state.load[r] == NIL:
        if rae1.state.loc[r] == rae1.state.pos[o]:
            print("Robot %s has picked up object %s" %(r, o))
            rae1.state.pos[o] = r
            rae1.state.load[r] = o
            res = SUCCESS
        elif rae1.state.loc[r] != rae1.state.pos[o]:
            print("Robot %s is not at object %s's location\n" %(r, o))
            res = FAILURE
    else:
        print("Robot %s is not free to take anything\n" %r)
        res = FAILURE
    return res

def put(r, o):
    if rae1.state.pos[o] == r:
        rae1.state.pos[o] = rae1.state.loc[r]
        rae1.state.load[r] = NIL
        print("Robot %s has put object %s at location %d\n" %(r,o,rae1.state.loc[r]))
        res = SUCCESS
    else:
        print("Object %s is not with robot %s\n" %(o,r))
        res = FAILURE
    return res

def charge(r, c):
    if rae1.state.loc[r] == rae1.state.pos[c] or rae1.state.pos[c] == r:
        rae1.state.charge[r] = 4
        print("Robot %s is fully charged\n" %r)
        res = SUCCESS
    else:
        print("Robot %s is not in the charger's location or it doesn't have the charger with it\n" %r)
        res = FAILURE
    return res

def moveCharger(c, l):
    print ("Charger %s is moved to location %s\n" %(c,l))
    rae1.state.pos[c] = l
    return SUCCESS

def move(r, l1, l2, dist):
    if l1 == l2:
        print("Robot %s is already at location %s\n" %(r, l2))
        res = SUCCESS
    elif rae1.state.loc[r] == l1 and rae1.state.charge[r] >= dist:
        print("Robot %s has moved from %d to %d\n" %(r, l1, l2))
        rae1.state.loc[r] = l2
        rae1.state.charge[r] = rae1.state.charge[r] - dist
        res = SUCCESS
    elif rae1.state.loc[r] != l1 and rae1.state.charge[r] >= dist:
        print("Robot %s is not in location %d\n" %(r, l1))
        res = FAILURE
    elif rae1.state.loc[r] == l1 and rae1.state.charge[r] < dist:
        print("Robot %s does not have enough charge to move :(\n" %r)
        rae1.state.charge[r] = 0 # should we do this?
        res = FAILURE
    else:
        print("Robot %s is not at location %s and it doesn't have enough charge!\n" %(r, l1))
        res = FAILURE
    return res

def perceive(l):
    if rae1.state.view[l] == False:
        for c in rae1.state.containers[l]:
            rae1.state.pos[c] = l
        rae1.state.view[l] = True
        print("Perceived location %d" %l)
    else:
        print("Already perceived\n")
    return SUCCESS

def MoveTo_Method1(r, l, stackid):
    dist = GETDISTANCE(rae1.state.loc[r], l)
    if rae1.state.charge[r] >= dist:
        rae1.do_command(move, r, rae1.state.loc[r], l, dist, stackid)
        res = SUCCESS
    else:
        print("Insufficient charge! only %.2f%%. Robot %s cannot move\n" %(rae1.state.charge[r] * 100 / 4, r))
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
            print("Failed to search %s" %o)
            res = FAILURE
    else:
        print("Position of %s is already known\n" %o)
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
            print("Failed to search %s" %o)
            res = FAILURE
    else:
        print("Position of %s is already known\n" %o)
        res = SUCCESS
    return res

def Fetch_Method1(r, o, stackid):
    if rae1.state.pos[o] == UNK:
        rae1.do_task('search', r, o, stackid)
    elif rae1.state.loc[r] == rae1.state.pos[o]:
        rae1.do_command(take, r, o, stackid)
    else:
        rae1.do_task('moveTo', r, rae1.state.pos[o],  stackid)
        rae1.do_command(take, r, o, stackid)
    return SUCCESS

def Fetch_Method2(r, o, stackid):
    if rae1.state.pos[o] == UNK:
        rae1.do_task('search', r, o, stackid)
    elif rae1.state.loc[r] == rae1.state.pos[o]:
        rae1.do_command(take, r, o, stackid)
    else:
        rae1.do_task('recharge', r, 'c1', stackid)
        rae1.do_task('moveTo', r, rae1.state.pos[o], stackid)
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
        print("Cannot move charger now, robots might need it\n")

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