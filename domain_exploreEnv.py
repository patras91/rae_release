__author__ = 'patras'

from domain_constants import *
import rae1

'''A UAV and several robots explore environment and collect data.
UAV can only survey whereas robots can survey, monitor, screen, sample and process.
UAV can fly whereas a robot can only move on the ground. The UAV and robots have limited
charge and needs to be charged frequently. They also have a capacity of the amount of data
they can carry with them. They can store data in the base location. UAV needs to return to
base location every night.'''

def survey(r, l):
    e = rae1.state.load[r]
    if e not in EE_TYPE:
        print("%s does not have any equipment\n" %r)
        res = FAILURE
    elif rae1.state.loc[r] == l and EE_TYPE[e] == 'survey' and rae1.state.data[r] < 4:
        print("%s has surveyed the location %s\n" %(r, l))
        res = SUCCESS
        rae1.state.data[r] += 1
    elif rae1.state.loc[r] != l:
        print("%s is not in location %s\n" %(r, l))
        res = FAILURE
    elif EE_TYPE[e] != 'survey':
        print("%s is not the right equipment for survey\n" %e)
        res = FAILURE
    elif rae1.state.data[r] == 4:
        print("%s cannot store any more data\n" %r)
        res = FAILURE
    return res

def monitor(r, l):
    e = rae1.state.load[r]
    if e not in EE_TYPE:
        print("%s does not have any equipment\n" %r)
        res = FAILURE
    elif rae1.state.loc[r] == l and EE_TYPE[e] == 'monitor' and r != 'UAV' and rae1.state.data[r] < 4:
        print("%s has monitored the location\n" %r)
        res = SUCCESS
        rae1.state.data[r] += 1
    elif rae1.state.loc[r] != l:
        print("%s is not in location %s\n" %(r, l))
        res = FAILURE
    elif EE_TYPE[e] != 'monitor':
        print("%s is not the right equipment for monitor\n" %e)
        res = FAILURE
    elif r == 'UAV':
        print("UAV cannot monitor\n")
        res = FAILURE
    elif rae1.state.data[r] == 4:
        print("%s cannot store any more data\n" %r)
        res = FAILURE
    return res

def screen(r, l):
    e = rae1.state.load[r]
    if e not in EE_TYPE:
        print("%s does not have any equipment\n" %r)
        res = FAILURE
    elif rae1.state.loc[r] == l and EE_TYPE[e] == 'screen' and r != 'UAV' and rae1.state.data[r] < 4:
        print("%s has screened the location\n" %r)
        res = SUCCESS
        rae1.state.data[r] += 1
    elif rae1.state.loc[r] != l:
        print("%s is not in location %s\n" %(r, l))
        res = FAILURE
    elif EE_TYPE[e] != 'screen':
        print("%s is not the right equipment for screening\n" %e)
        res = FAILURE
    elif r == 'UAV':
        print("UAV cannot do screening\n")
        res = FAILURE
    elif rae1.state.data[r] == 4:
        print("%s cannot store any more data\n" %r)
        res = FAILURE
    return res

def sample(r, l):
    e = rae1.state.load[r]
    if e not in EE_TYPE:
        print("%s does not have any equipment\n" %r)
        res = FAILURE
    elif rae1.state.loc[r] == l and EE_TYPE[e] == 'sample' and r != 'UAV' and rae1.state.data[r] < 4:
        print("%s has sampled the location\n" %r)
        res = SUCCESS
        rae1.state.data[r] += 1
    elif rae1.state.loc[r] != l:
        print("%s is not in location %s\n" %(r, l))
        res = FAILURE
    elif EE_TYPE[e] != 'sample':
        print("%s is not the right equipment for sampling\n" %e)
        res = FAILURE
    elif r == 'UAV':
        print("UAV cannot do sampling\n")
        res = FAILURE
    elif rae1.state.data[r] == 4:
        print("%s cannot store any more data\n" %r)
        res = FAILURE
    return res

def process(r, l):
    e = rae1.state.load[r]
    if e not in EE_TYPE:
        print("%s does not have any equipment\n" %r)
        res = FAILURE
    elif rae1.state.loc[r] == l and EE_TYPE[e] == 'process' and r != 'UAV' and rae1.state.data[r] < 4:
        print("%s has processed the location\n" %r)
        res = SUCCESS
        rae1.state.data[r] += 1
    elif rae1.state.loc[r] != l:
        print("%s is not in location %s\n" %(r, l))
        res = FAILURE
    elif EE_TYPE[e] != 'process':
        print("%s is not the right equipment for process\n" %e)
        res = FAILURE
    elif r == 'UAV':
        print("UAV cannot do processing\n")
        res = FAILURE
    elif rae1.state.data[r] == 4:
        print("%s cannot store any more data\n" %r)
        res = FAILURE
    return res

def charge(r, c):
    if rae1.state.loc[r] == rae1.state.pos[c] or rae1.state.pos[c] == r:
        rae1.state.charge[r] = 4
        print("Robot %s is fully charged\n" %r)
        res = SUCCESS
    else:
        print("%s is not in the charger's location or it doesn't have the charger with it\n" %r)
        res = FAILURE
    return res

def move(r, l1, l2):
    dist = EE_GETDISTANCE(l1, l2)
    if l1 == l2:
        print("%s is already at location %s\n" %(r, l2))
        res = SUCCESS
    elif rae1.state.loc[r] == l1 and rae1.state.charge[r] >= dist:
        print("%s has moved from %s to %s\n" %(r, l1, l2))
        rae1.state.loc[r] = l2
        rae1.state.charge[r] = rae1.state.charge[r] - dist
        res = SUCCESS
    elif rae1.state.loc[r] != l1 and rae1.state.charge[r] >= dist:
        print("%s is not in location %s\n" %(r, l1))
        res = FAILURE
    elif rae1.state.loc[r] == l1 and rae1.state.charge[r] < dist:
        print("%s does not have any charge to move :(\n" %r)
        res = FAILURE
    else:
        print("%s is not at location %s and it doesn't have enough charge!\n" %(r, l1))
        res = FAILURE
    return res

def fly(r, l1, l2):
    dist = EE_GETDISTANCE(l1, l2)
    if r != 'UAV':
        print("%s cannot fly\n" %r)
        res = FAILURE
    elif l1 == l2:
        print("%s is already at location %s\n" %(r, l2))
        res = SUCCESS
    elif rae1.state.loc[r] == l1 and rae1.state.charge[r] >= dist:
        print("%s has flied from %d to %d\n" %(r, l1, l2))
        rae1.state.loc[r] = l2
        rae1.state.charge[r] = rae1.state.charge[r] - dist
        res = SUCCESS
    elif rae1.state.loc[r] != l1 and rae1.state.charge[r] >= dist:
        print("%s is not in location %d\n" %(r, l1))
        res = FAILURE
    elif rae1.state.loc[r] == l1 and rae1.state.charge[r] < dist:
        print("%s does not have any charge to move :(\n" %r)
        res = FAILURE
    else:
        print("%s is not at location %s and it doesn't have enough charge!\n" %(r, l1))
        res = FAILURE
    return res

def take(r, o):
    if rae1.state.load[r] == NIL:
        if rae1.state.loc[r] == rae1.state.pos[o]:
            print("%s has picked up %s" %(r, o))
            rae1.state.pos[o] = r
            rae1.state.load[r] = o
            res = SUCCESS
        elif rae1.state.loc[r] != rae1.state.pos[o]:
            print("%s is not at %s's location\n" %(r, o))
            res = FAILURE
    else:
        print("%s is not free to take anything\n" %r)
        res = FAILURE
    return res

def put(r, o):
    if rae1.state.pos[o] == r:
        rae1.state.pos[o] = rae1.state.loc[r]
        rae1.state.load[r] = NIL
        print("%s has put %s at location %s\n" %(r,o,rae1.state.loc[r]))
        res = SUCCESS
    else:
        print("%s is not with robot %s\n" %(o,r))
        res = FAILURE
    return res

def deposit(r):
    if rae1.state.loc[r] == 'base':
        print("%s has deposited data in the base\n" %r)
        rae1.state.data[r] = 0
        res = SUCCESS
    else:
        print("%s is not in base, so it cannot deposit data.\n" %r)
        res = FAILURE
    return res

def transferData(r1, r2):
    if rae1.state.loc[r1] != rae1.state.loc[r2]:
        print("%s and %s are not in same location.\n" %(r1, r2))
        res = FAILURE
    elif rae1.state.data[r2] + rae1.state.data[r1] <= 4:
        print("%s transfered data to %s\n" %(r1, r2))
        rae1.state.data[r2] += rae1.state.data[r1]
        rae1.state.data[r1] = 0
        res = SUCCESS
    elif rae1.state.data[r2] < 4:
        t = 4 - rae1.state.data[r2]
        rae1.state.data[r2] = 4
        rae1.state.data[r1] -= t
        res = SUCCESS
    return res

def Explore_Method2(r, activity, l, stackid):
    rae1.do_task('getEquipment', r, activity, stackid)
    rae1.do_task('moveTo', r, l, stackid)
    if activity == 'survey':
        rae1.do_command(survey, r, l, stackid)
    elif activity == 'monitor':
        rae1.do_command(monitor, r, l, stackid)
    elif activity == 'screen':
        rae1.do_command(screen, r, l, stackid)
    elif activity == 'sample':
        rae1.do_command(sample, r, l, stackid)
    elif activity == 'process':
        rae1.do_command(process, r, l, stackid)
    rae1.do_task('depositData', r, 'base', stackid)
    return SUCCESS

def Explore_Method1(r, activity, l, stackid):
    rae1.do_task('getEquipment', r, activity, stackid)
    rae1.do_task('moveTo', r, l, stackid)
    if activity == 'survey':
        rae1.do_command(survey, r, l, stackid)
    elif activity == 'monitor':
        rae1.do_command(monitor, r, l, stackid)
    elif activity == 'screen':
        rae1.do_command(screen, r, l, stackid)
    elif activity == 'sample':
        rae1.do_command(sample, r, l, stackid)
    elif activity == 'process':
        rae1.do_command(process, r, l, stackid)
    return SUCCESS

def GetEquipment_Method1(r, activity, stackid):
    if rae1.state.load[r] != EE_EQUIPMENT[activity]:
        rae1.do_task('moveTo', r, rae1.state.pos[EE_EQUIPMENT[activity]], stackid)
        rae1.do_command(take, r, EE_EQUIPMENT[activity], stackid)
    return SUCCESS

def GetEquipment_Method2(r, activity, stackid):
    if rae1.state.load[r] != EE_EQUIPMENT[activity]:
        rae1.do_task('moveTo', r, rae1.state.pos[EE_EQUIPMENT[activity]], stackid)
        rae1.do_command(put, r, rae1.state.load[r], stackid)
        rae1.do_command(take, r, EE_EQUIPMENT[activity], stackid)
    return SUCCESS

def MoveTo_Method1(r, l, stackid):
    res = SUCCESS
    path = EE_GETPATH(rae1.state.loc[r], l)
    if path == {}:
        print("%s is already at location %s \n" %(r, l))
    else:
        lTemp = rae1.state.loc[r]
        lNext = path[lTemp]
        while(lTemp != l):
            lNext = path[lTemp]
            rae1.do_command(move, r, lTemp, lNext, stackid)
            if lTemp == rae1.state.loc[r]:
                res = FAILURE
                break
            else:
                lTemp = rae1.state.loc[r]
    return res

def MoveTo_Method2(r, l, stackid):
    dist = EE_GETDISTANCE(rae1.state.loc[r], l)
    if rae1.state.charge[r] >= dist:
        path = EE_GETPATH(rae1.state.loc[r], l)
        if path == {}:
            print("%s is already at location %s \n" %(r, l))
            res = SUCCESS
        else:
            lTemp = rae1.state.loc[r]
            lNext = path[lTemp]
            while(lTemp != l):
                lNext = path[lTemp]
                rae1.do_command(move, r, lTemp, lNext, stackid)
                if lTemp == rae1.state.loc[r]:
                    res = FAILURE
                    break
                else:
                    lTemp = rae1.state.loc[r]
            res = SUCCESS
    else:
        print("Insufficient charge! only %.2f%%. Robot %s cannot move\n" %(rae1.state.charge[r] * 100 / 75, r))
        res = FAILURE
    return res

def MoveTo_Method3(r, l, stackid):
    res = SUCCESS
    dist = EE_GETDISTANCE(rae1.state.loc[r], l)
    if rae1.state.charge[r] >= dist:
        path = EE_GETPATH(rae1.state.loc[r], l)
        if path == {}:
            print("%s is already at location %s \n" %(r, l))
        else:
            lTemp = rae1.state.loc[r]
            lNext = path[lTemp]
            while(lTemp != l):
                lNext = path[lTemp]
                rae1.do_command(move, r, lTemp, lNext, stackid)
                if lTemp == rae1.state.loc[r]:
                    res = FAILURE
                    break
                else:
                    lTemp = rae1.state.loc[r]
    else:
        rae1.do_task('recharge', r, stackid)
        rae1.do_task('moveTo', r, l, stackid)
    return res

def FlyTo_Method1(r, l, stackid):
    if r == 'UAV':
        rae1.do_command(fly, r, rae1.state.loc[r], l, stackid)
        res = SUCCESS
    else:
        print("%s is not a UAV. So, it cannot fly\n" %r)
        res = FAILURE
    return res

def FlyTo_Method2(r, l, stackid):
    dist = GETDISTANCE(rae1.state.loc[r], l)
    if r == 'UAV':
        if rae1.state.charge[r] >= dist:
            rae1.do_command(fly, r, rae1.state.loc[r], l, dist, stackid)
            res = SUCCESS
        else:
            print("Insufficient charge! only %.2f%%. Robot %s cannot move\n" %(rae1.state.charge[r] * 100 / 75, r))
            res = FAILURE
    else:
        print("%s is not a UAV. So, it cannot fly\n" %r)
        res = FAILURE
    return res

def FlyTo_Method3(r, l, stackid):
    dist = GETDISTANCE(rae1.state.loc[r], l)
    if r == 'UAV':
        if rae1.state.charge[r] >= dist:
            rae1.do_command(fly, r, rae1.state.loc[r], l, dist, stackid)
            res = SUCCESS
        else:
            rae1.do_task('recharge', r, stackid)
            rae1.do_task('moveTo', r, l, stackid)
            res = SUCCESS
    else:
        print("%s is not a UAV. So, it cannot fly\n" %r)
        res = FAILURE
    return res

def DepositData_Method1(r, stackid):
    if rae1.state.data[r] > 0:
        rae1.do_task('moveTo', r, 'base', stackid)
        rae1.do_command(deposit, r, stackid)
    else:
        print("%s has no data to deposit.\n" %r)
    return SUCCESS

def DepositData_Method2(r, stackid):
    if rae1.state.data[r] > 0:
        rae1.do_task('flyTo', 'UAV', rae1.state.loc[r], stackid)
        rae1.do_command(transferData, r, 'UAV', stackid)
        rae1.do_task('flyTo', 'UAV', 'base', stackid)
        rae1.do_command(deposit, 'UAV', stackid)
    else:
        print("%s has no data to deposit.\n" %r)
    return SUCCESS

def Recharge_Method1(r, stackid):
    c = 'c1'
    if rae1.state.pos[c] not in EE_LOCATIONS and rae1.state.pos[c] != r:
        print("%s cannot find charger %s\n" %(r, c))
        res = FAILURE
    elif rae1.state.loc[r] != rae1.state.pos[c] and rae1.state.pos[c] != r:
        rae1.do_task('moveTo', r, rae1.state.pos[c], stackid)
        rae1.do_command(charge, r, c, stackid)
        res = SUCCESS
    else:
        rae1.do_command(charge, r, c, stackid)
        res = SUCCESS
    return res

def Recharge_Method2(r, stackid):
    c = 'c1'
    if rae1.state.pos[c] not in EE_LOCATIONS and rae1.state.pos[c] != r:
        print("%s cannot find charger %s\n" %(r, c))
        res = FAILURE
    elif rae1.state.loc[r] != rae1.state.pos[c] and rae1.state.pos[c] != r:
        rae1.do_task('moveTo', r, rae1.state.pos[c], stackid)
        rae1.do_command(charge, r, c, stackid)
        rae1.do_command(take, r, c, stackid)
        res = SUCCESS
    else:
        rae1.do_command(charge, r, c, stackid)
        rae1.do_command(take, r, c, stackid)
        res = SUCCESS
    return res

def exploreEnv_init():
    rae1.declare_commands(survey, monitor, screen, sample, process, charge, move, put, take, fly, deposit, transferData)
    print('\n')
    rae1.print_commands()

    rae1.declare_methods('explore', Explore_Method1, Explore_Method2)
    rae1.declare_methods('getEquipment', GetEquipment_Method1, GetEquipment_Method2)
    rae1.declare_methods('moveTo', MoveTo_Method1, MoveTo_Method2, MoveTo_Method3)
    rae1.declare_methods('flyTo', FlyTo_Method1, FlyTo_Method2, FlyTo_Method3)
    rae1.declare_methods('recharge', Recharge_Method1, Recharge_Method2)
    rae1.declare_methods('depositData', DepositData_Method1, DepositData_Method2)
    print('\n')
    rae1.print_methods()

    print('\n*********************************************************')
    print("* Call rae1 on environment exploration domain.")
    print("* For a different amout of printout, try verbosity(0), verbosity(1), or verbosity(2).")
    print('*********************************************************\n')

    rae1.state.loc = {'r1': 'base', 'UAV': 'base'}
    rae1.state.charge = {'r1':75, 'UAV': 75}
    rae1.state.data = {'r1': 0, 'UAV': 0}
    rae1.state.load = {'r1': NIL, 'UAV': NIL}
    rae1.state.pos = {'c1': 'base', 'e1': 'base', 'e2': 'base', 'e3': 'base', 'e4': 'base', 'e5': 'base'}
