__author__ = 'patras'

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
from env_exploreEnv import *

'''Several UAVs and UGVs explore environment and collect data.
UAV can only survey whereas UGVs can survey, monitor, screen, sample and process.
UAV can fly whereas a UGV can only move on the ground. The UAV and UGVs have limited
charge and needs to be charged frequently. They also have a capacity of the amount of data
they can carry with them. They can store data in the base location.'''

# Using Dijsktra's algorithm
def EE_GETPATH(l0, l1):
    visitedDistances = {l0: 0}
    locs = list(rv.LOCATIONS)
    path = {}

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
            dist = current_dist + rv.EDGES[min_loc][l]
            if l not in visitedDistances or dist < visitedDistances[l]:
                visitedDistances[l] = dist
                path[l] = min_loc
    l = l1
    path2 = {}
    while l != l0:
        path2[path[l]] = l
        l = path[l]

    return path2

# Using Dijsktra's algorithm
def EE_GETDISTANCE(l0, l1):
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
            dist = current_dist + rv.EDGES[min_loc][l]
            if l not in visitedDistances or dist < visitedDistances[l]:
                visitedDistances[l] = dist

    return visitedDistances[l1]

def survey(r, l):
    state.load.AcquireLock(r)
    state.loc.AcquireLock(r)
    state.data.AcquireLock(r)
    e = state.load[r]
    if e not in rv.TYPE:
        gui.Simulate("%s does not have any equipment\n" %r)
        res = FAILURE
    elif state.loc[r] == l and rv.TYPE[e] == 'survey' and state.data[r] < 4:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('survey', start) == False):
            pass
        res = Sense('survey')
        if res == SUCCESS:
            state.data[r] += 1
            gui.Simulate("%s has surveyed the location %s\n" %(r, l))
        else:
            gui.Simulate("%s has failed to do survey %d due to an internal error.\n" %(r,l))
    elif state.loc[r] != l:
        gui.Simulate("%s is not in location %s\n" %(r, l))
        res = FAILURE
    elif rv.TYPE[e] != 'survey':
        gui.Simulate("%s is not the right equipment for survey\n" %e)
        res = FAILURE
    elif state.data[r] == 4:
        gui.Simulate("%s cannot store any more data\n" %r)
        res = FAILURE
    state.load.ReleaseLock(r)
    state.loc.ReleaseLock(r)
    state.data.ReleaseLock(r)
    return res

def monitor(r, l):
    state.load.AcquireLock(r)
    state.loc.AcquireLock(r)
    state.data.AcquireLock(r)
    e = state.load[r]
    if e not in rv.TYPE:
        gui.Simulate("%s does not have any equipment\n" %r)
        res = FAILURE
    elif state.loc[r] == l and rv.TYPE[e] == 'monitor' and r != 'UAV' and state.data[r] < 4:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('monitor', start) == False):
            pass
        res = Sense('monitor')
        if res == SUCCESS:
            gui.Simulate("%s has monitored the location\n" %r)
            state.data[r] += 1
        else:
            gui.Simulate("Monitoring has failed due to some internal error\n")
    elif state.loc[r] != l:
        gui.Simulate("%s is not in location %s\n" %(r, l))
        res = FAILURE
    elif rv.TYPE[e] != 'monitor':
        gui.Simulate("%s is not the right equipment for monitor\n" %e)
        res = FAILURE
    elif r == 'UAV':
        gui.Simulate("UAV cannot monitor\n")
        res = FAILURE
    elif state.data[r] == 4:
        gui.Simulate("%s cannot store any more data\n" %r)
        res = FAILURE
    state.load.ReleaseLock(r)
    state.loc.ReleaseLock(r)
    state.data.ReleaseLock(r)
    return res

def screen(r, l):
    state.load.AcquireLock(r)
    state.loc.AcquireLock(r)
    state.data.AcquireLock(r)
    e = state.load[r]
    if e not in rv.TYPE:
        gui.Simulate("%s does not have any equipment\n" %r)
        res = FAILURE
    elif state.loc[r] == l and rv.TYPE[e] == 'screen' and r != 'UAV' and state.data[r] < 4:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('screen', start) == False):
            pass
        res = Sense('screen')
        if res == SUCCESS:
            gui.Simulate("%s has screened the location\n" %r)
            state.data[r] += 1
        else:
            gui.Simulate("Screening failed due to some internal error\n")
    elif state.loc[r] != l:
        gui.Simulate("%s is not in location %s\n" %(r, l))
        res = FAILURE
    elif rv.TYPE[e] != 'screen':
        gui.Simulate("%s is not the right equipment for screening\n" %e)
        res = FAILURE
    elif r == 'UAV':
        gui.Simulate("UAV cannot do screening\n")
        res = FAILURE
    elif state.data[r] == 4:
        gui.Simulate("%s cannot store any more data\n" %r)
        res = FAILURE
    state.load.ReleaseLock(r)
    state.loc.ReleaseLock(r)
    state.data.ReleaseLock(r)
    return res

def sample(r, l):
    state.load.AcquireLock(r)
    state.loc.AcquireLock(r)
    state.data.AcquireLock(r)
    e = state.load[r]
    if e not in rv.TYPE:
        gui.Simulate("%s does not have any equipment\n" %r)
        res = FAILURE
    elif state.loc[r] == l and rv.TYPE[e] == 'sample' and r != 'UAV' and state.data[r] < 4:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('sample', start) == False):
            pass
        res = Sense('sample')
        if res == SUCCESS:
            gui.Simulate("%s has sampled the location\n" %r)
            state.data[r] += 1
        else:
            gui.Simulate("Sampling failed due to internal error\n")
    elif state.loc[r] != l:
        gui.Simulate("%s is not in location %s\n" %(r, l))
        res = FAILURE
    elif rv.TYPE[e] != 'sample':
        gui.Simulate("%s is not the right equipment for sampling\n" %e)
        res = FAILURE
    elif r == 'UAV':
        gui.Simulate("UAV cannot do sampling\n")
        res = FAILURE
    elif state.data[r] == 4:
        gui.Simulate("%s cannot store any more data\n" %r)
        res = FAILURE
    state.load.ReleaseLock(r)
    state.loc.ReleaseLock(r)
    state.data.ReleaseLock(r)
    return res

def process(r, l):
    state.load.AcquireLock(r)
    state.loc.AcquireLock(r)
    state.data.AcquireLock(r)
    e = state.load[r]
    if e not in rv.TYPE:
        gui.Simulate("%s does not have any equipment\n" %r)
        res = FAILURE
    elif state.loc[r] == l and rv.TYPE[e] == 'process' and r != 'UAV' and state.data[r] < 4:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('process', start) == False):
            pass
        res = Sense('process')
        if res == SUCCESS:
            gui.Simulate("%s has processed the location\n" %r)
            state.data[r] += 1
        else:
            gui.Simulate("Processing failed due to an internal error\n")
    elif state.loc[r] != l:
        gui.Simulate("%s is not in location %s\n" %(r, l))
        res = FAILURE
    elif rv.TYPE[e] != 'process':
        gui.Simulate("%s is not the right equipment for process\n" %e)
        res = FAILURE
    elif r == 'UAV':
        gui.Simulate("UAV cannot do processing\n")
        res = FAILURE
    elif state.data[r] == 4:
        gui.Simulate("%s cannot store any more data\n" %r)
        res = FAILURE
    state.load.ReleaseLock(r)
    state.loc.ReleaseLock(r)
    state.data.ReleaseLock(r)
    return res

def alienSpotted(l):
    gui.Simulate("An alien is spotted in location %s \n" %l)
    return SUCCESS

def handleAlien(r, l):
    if state.loc[r] == l:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('handleAlien', start) == False):
            pass
        gui.Simulate("Robot %s is negotiating with alien.\n" %r)
        res = SUCCESS
    else:
        gui.Simulate("Robot %s is not in alien's location\n" %r)
        res = FAILURE
    return res

def charge(r, c):
    state.loc.AcquireLock(r)
    state.pos.AcquireLock(c)
    if state.loc[r] == state.pos[c] or state.pos[c] == r:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('charge', start) == False):
            pass
        res = Sense('charge')
        if res == SUCCESS:
            state.charge.AcquireLock(r)
            state.charge[r] = 100
            gui.Simulate("%s is fully charged\n" %r)
            state.charge.ReleaseLock(r)
        else:
            gui.Simulate("Charging failed due to some internal error.\n")
    else:
        gui.Simulate("%s is not in the charger's location or it doesn't have the charger with it\n" %r)
        res = FAILURE
    state.loc.ReleaseLock(r)
    state.pos.ReleaseLock(c)
    return res

def move(r, l1, l2):
    state.loc.AcquireLock(r)
    state.charge.AcquireLock(r)
    dist = EE_GETDISTANCE(l1, l2)
    if l1 == l2:
        gui.Simulate("%s is already at location %s\n" %(r, l2))
        res = SUCCESS
    elif state.loc[r] == l1 and state.charge[r] >= dist:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('move', start) == False):
            pass
        res = Sense('move')
        if res == SUCCESS:
            gui.Simulate("%s has moved from %s to %s\n" %(r, l1, l2))
            state.loc[r] = l2
            state.charge[r] = state.charge[r] - dist
        else:
            gui.Simulate("Move failed due to an internal error.\n")
    elif state.loc[r] != l1 and state.charge[r] >= dist:
        gui.Simulate("%s is not in location %s\n" %(r, l1))
        res = FAILURE
    elif state.loc[r] == l1 and state.charge[r] < dist:
        gui.Simulate("%s does not have any charge to move :(\n" %r)
        res = FAILURE
    else:
        gui.Simulate("%s is not at location %s and it doesn't have enough charge!\n" %(r, l1))
        res = FAILURE
    state.loc.ReleaseLock(r)
    state.charge.ReleaseLock(r)
    return res

def fly(r, l1, l2):
    state.loc.AcquireLock(r)
    state.charge.AcquireLock(r)

    dist = EE_GETDISTANCE(l1, l2)
    if r != 'UAV':
        gui.Simulate("%s cannot fly\n" %r)
        res = FAILURE
    elif l1 == l2:
        gui.Simulate("%s is already at location %s\n" %(r, l2))
        res = SUCCESS
    elif state.loc[r] == l1 and state.charge[r] >= dist:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('fly', start) == False):
            pass
        res = Sense('fly')
        if res == SUCCESS:
            gui.Simulate("%s has flied from %s to %s\n" %(r, l1, l2))
            state.loc[r] = l2
            state.charge[r] = state.charge[r] - dist
        else:
            gui.Simulate("Flying failed due to an internal error.\n")
    elif state.loc[r] != l1 and state.charge[r] >= dist:
        gui.Simulate("%s is not in location %s\n" %(r, l1))
        res = FAILURE
    elif state.loc[r] == l1 and state.charge[r] < dist:
        gui.Simulate("%s does not have any charge to move :(\n" %r)
        res = FAILURE
    else:
        gui.Simulate("%s is not at location %s and it doesn't have enough charge!\n" %(r, l1))
        res = FAILURE
    state.loc.ReleaseLock(r)
    state.charge.ReleaseLock(r)
    return res

def take(r, o):
    state.load.AcquireLock(r)
    if state.load[r] == NIL:
        state.loc.AcquireLock(r)
        state.pos.AcquireLock(o)
        if state.loc[r] == state.pos[o]:
            start = globalTimer.GetTime()
            while(globalTimer.IsCommandExecutionOver('take', start) == False):
                pass
            res = Sense('take')
            if res == SUCCESS:
                gui.Simulate("%s has picked up %s\n" %(r, o))
                state.pos[o] = r
                state.load[r] = o
            else:
                gui.Simulate("Take failed due to an internal failure.\n")
        else:
            gui.Simulate("%s is not at %s's location\n" %(r, o))
            res = FAILURE
        state.loc.ReleaseLock(r)
        state.pos.ReleaseLock(o)
    else:
        gui.Simulate("%s is not free to take anything\n" %r)
        res = FAILURE
    state.load.ReleaseLock(r)
    return res

def put(r, o):
    state.loc.AcquireLock(r)
    state.pos.AcquireLock(o)
    if state.pos[o] == r:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('put', start) == False):
            pass
        res = Sense('put')
        if res == SUCCESS:
            state.pos[o] = state.loc[r]
            state.load[r] = NIL
            gui.Simulate("%s has put %s at location %s\n" %(r,o,state.loc[r]))
        else:
            gui.Simulate("put failed due to an internal error.\n")
    else:
        gui.Simulate("%s is not with %s\n" %(o,r))
        res = FAILURE
    state.loc.ReleaseLock(r)
    state.pos.ReleaseLock(o)
    return res

def deposit(r):
    state.loc.AcquireLock(r)
    state.data.AcquireLock(r)
    if state.loc[r] == 'base':
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('deposit', start) == False):
            pass
        res = Sense('deposit')
        if res == SUCCESS:
            gui.Simulate("%s has deposited data in the base\n" %r)
            state.data[r] = 0
        else:
            gui.Simulate("Deposit failed due to an internal error.\n")
    else:
        gui.Simulate("%s is not in base, so it cannot deposit data.\n" %r)
        res = FAILURE
    state.loc.ReleaseLock(r)
    state.data.ReleaseLock(r)
    return res

def transferData(r1, r2):
    state.loc.AcquireLock(r1)
    state.loc.AcquireLock(r2)
    state.data.AcquireLock(r1)
    state.data.AcquireLock(r2)

    if state.loc[r1] != state.loc[r2]:
        gui.Simulate("%s and %s are not in same location.\n" %(r1, r2))
        res = FAILURE
    elif state.data[r2] + state.data[r1] <= 4:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('transferData', start) == False):
            pass
        res = Sense('transferData')
        if res == SUCCESS:
            gui.Simulate("%s transfered data to %s\n" %(r1, r2))
            state.data[r2] += state.data[r1]
            state.data[r1] = 0
        else:
            gui.Simulate("Transfer data failed due to an internal error.\n")

    elif state.data[r2] < 4:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('transferData', start) == False):
            pass
        res = Sense('transferData')
        if res == SUCCESS:
            t = 4 - state.data[r2]
            state.data[r2] = 4
            state.data[r1] -= t
            gui.Simulate("%s transfered data to %s\n" %(r1, r2))
        else:
            gui.Simulate("Transfer data failed due to an internal error.\n")

    state.loc.ReleaseLock(r1)
    state.loc.ReleaseLock(r2)
    state.data.ReleaseLock(r1)
    state.data.ReleaseLock(r2)
    return res

def Explore_Method1(r, activity, l):
    ape.do_task('getEquipment', r, activity)
    ape.do_task('moveTo', r, l)
    if activity == 'survey':
        ape.do_command(survey, r, l)
    elif activity == 'monitor':
        ape.do_command(monitor, r, l)
    elif activity == 'screen':
        ape.do_command(screen, r, l)
    elif activity == 'sample':
        ape.do_command(sample, r, l)
    elif activity == 'process':
        ape.do_command(process, r, l)

def GetEquipment_Method1(r, activity):
    if state.load[r] != rv.EQUIPMENT[activity]:
        ape.do_task('moveTo', r, state.pos[rv.EQUIPMENT[activity]])
        ape.do_command(take, r, rv.EQUIPMENT[activity])

def GetEquipment_Method2(r, activity):
    if state.load[r] != rv.EQUIPMENT[activity]:
        ape.do_task('moveTo', r, state.pos[rv.EQUIPMENT[activity]])
        state.load.AcquireLock(r)
        if state.load[r] != NIL:
            x = state.load[r]
            state.load.ReleaseLock(r)
            ape.do_command(put, r, x)
        else:
            state.load.ReleaseLock(r)
        ape.do_command(take, r, rv.EQUIPMENT[activity])

def GetEquipment_Method3(r, activity):
    if state.load[r] != rv.EQUIPMENT[activity]:
        loc = state.pos[rv.EQUIPMENT[activity]]
        if loc not in rv.LOCATIONS:
            robo = loc
            ape.do_task('moveTo', r, state.loc[robo])
            state.load.AcquireLock(r)
            if state.load[r] != NIL:
                x = state.load[r]
                state.load.ReleaseLock(r)
                ape.do_command(put, r, x)
            else:
                state.load.ReleaseLock(r)
            ape.do_command(put, robo, rv.EQUIPMENT[activity])
            ape.do_command(take, r, rv.EQUIPMENT[activity])
        else:
            ape.do_command(fail)

def MoveTo_MethodHelper(r, l):
    path = EE_GETPATH(state.loc[r], l)
    if path == {}:
        gui.Simulate("%s is already at location %s \n" %(r, l))
    else:
        lTemp = state.loc[r]
        if lTemp not in path:
            gui.Simulate("%s is out of its path to %s\n" %(r, l))
            ape.do_command(fail)
        else:
            while(lTemp != l):
                lNext = path[lTemp]
                ape.do_command(move, r, lTemp, lNext)
                if lNext != state.loc[r]:
                    gui.Simulate("%s is out of its path to %s\n" %(r, l))
                    ape.do_command(fail)
                else:
                    lTemp = lNext

def MoveTo_Method1(r, l):
    if l not in rv.LOCATIONS:
        gui.Simulate("%s is trying to go to an invalid location\n" %r)
        ape.do_command(fail)
    else:
        MoveTo_MethodHelper(r, l)

def MoveTo_Method2(r, l):
    if l not in rv.LOCATIONS:
        gui.Simulate("%s is trying to go to an invalid location\n" %r)
        ape.do_command(fail)
    else:
        dist = EE_GETDISTANCE(state.loc[r], l)
        if state.charge[r] >= dist:
            MoveTo_MethodHelper(r, l)
        else:
            ape.do_task('recharge', r)
            ape.do_task('moveTo', r, l)

def FlyTo_Method1(r, l):
    if r == 'UAV':
        ape.do_command(fly, r, state.loc[r], l)
    else:
        gui.Simulate("%s is not a UAV. So, it cannot fly\n" %r)
        ape.do_command(fail)

def FlyTo_Method2(r, l):
    dist = EE_GETDISTANCE(state.loc[r], l)
    if r == 'UAV':
        if state.charge[r] >= dist:
            ape.do_command(fly, r, state.loc[r], l)
        else:
            ape.do_task('recharge', r)
            ape.do_task('flyTo', r, l)
    else:
        gui.Simulate("%s is not a UAV. So, it cannot fly\n" %r)
        ape.do_command(fail)

def DepositData_Method1(r):
    if state.data[r] > 0:
        ape.do_task('moveTo', r, 'base')
        ape.do_command(deposit, r)
    else:
        gui.Simulate("%s has no data to deposit.\n" %r)

def DepositData_Method2(r):
    if state.data[r] > 0:
        if r != 'UAV':
            ape.do_task('flyTo', 'UAV', state.loc[r])
            ape.do_command(transferData, r, 'UAV')
        ape.do_task('flyTo', 'UAV', 'base')
        ape.do_command(deposit, 'UAV')
    else:
        gui.Simulate("%s has no data to deposit.\n" %r)

def Recharge_Method1(r):
    c = 'c1'
    if state.pos[c] not in rv.LOCATIONS and state.pos[c] != r:
        gui.Simulate("%s cannot find charger %s\n" %(r, c))
        ape.do_command(fail)
    elif state.loc[r] != state.pos[c] and state.pos[c] != r:
        dist = EE_GETDISTANCE(state.loc[r], state.pos[c])
        if state.charge[r] >= dist:
            ape.do_task('moveTo', r, state.pos[c])
            ape.do_command(charge, r, c)
        else:
            gui.Simulate("%s is stranded without any possibility of charging\n" %r)
            ape.do_command(fail)
    else:
        ape.do_command(charge, r, c)

def Recharge_Method2(r):
    c = 'c1'
    if state.pos[c] not in rv.LOCATIONS and state.pos[c] != r:
        gui.Simulate("%s cannot find charger %s\n" %(r, c))
        ape.do_command(fail)
    elif state.loc[r] != state.pos[c] and state.pos[c] != r:
        dist = EE_GETDISTANCE(state.loc[r], state.pos[c])
        if state.charge[r] >= dist:
            ape.do_task('moveTo', r, state.pos[c])
            ape.do_command(charge, r, c)
            ape.do_command(take, r, c)
        else:
            gui.Simulate("%s is stranded without any possibility of charging\n" %r)
            ape.do_command(fail)
    else:
        ape.do_command(charge, r, c)
        ape.do_command(take, r, c)

def DoActivities_Method1(r, actList):
    for act in actList:
        ape.do_task('explore', r, act[0], act[1])
        ape.do_task('depositData', r)

def DoActivities_Method2(r, actList):
    for act in actList:
        ape.do_task('explore', r, act[0], act[1])
    ape.do_task('depositData', r)

def DoActivities_Method3(r, actList):
    for act in actList:
        ape.do_task('explore', r, act[0], act[1])
        ape.do_task('depositData', r)
        ape.do_task('recharge', r)

def DoActivities_Method4(r, actList):
    for act in actList:
        ape.do_task('explore', r, act[0], act[1])
        ape.do_task('recharge', r)
    ape.do_task('depositData', r)

def HandleEmergency_Method1(r, l):
    ape.do_task('recharge', r)
    ape.do_task('moveTo', r, l)
    ape.do_command(handleAlien, r, l)

def HandleEmergency_Method2(r, l):
    ape.do_task('moveTo', r, l)
    ape.do_command(handleAlien, r, l)

rv = RV()
ape.declare_commands([
    survey, 
    monitor, 
    screen, 
    sample, 
    process, 
    charge, 
    move, 
    put, 
    take, 
    fly, 
    deposit, 
    transferData, 
    handleAlien])
                      
ape.declare_methods('explore', Explore_Method1)
ape.declare_methods('getEquipment', GetEquipment_Method1, GetEquipment_Method2, GetEquipment_Method3)
ape.declare_methods('moveTo', MoveTo_Method1)
ape.declare_methods('flyTo', FlyTo_Method1)
ape.declare_methods('recharge', Recharge_Method1, Recharge_Method2)
ape.declare_methods('depositData', DepositData_Method1, DepositData_Method2)
ape.declare_methods('doActivities', DoActivities_Method2, DoActivities_Method4, DoActivities_Method1, DoActivities_Method3)
ape.declare_methods('handleEmergency', HandleEmergency_Method2, HandleEmergency_Method1)


