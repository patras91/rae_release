__author__ = 'patras'

from domain_constants import *
import ape
import gui
from timer import globalTimer


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
    ape.state.load.AcquireLock(r)
    ape.state.loc.AcquireLock(r)
    ape.state.data.AcquireLock(r)
    e = ape.state.load[r]
    if e not in rv.TYPE:
        gui.Simulate("%s does not have any equipment\n" %r)
        res = FAILURE
    elif ape.state.loc[r] == l and rv.TYPE[e] == 'survey' and ape.state.data[r] < 4:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('survey', start) == False):
            pass
        gui.Simulate("%s has surveyed the location %s\n" %(r, l))
        res = SUCCESS
        ape.state.data[r] += 1
    elif ape.state.loc[r] != l:
        gui.Simulate("%s is not in location %s\n" %(r, l))
        res = FAILURE
    elif rv.TYPE[e] != 'survey':
        gui.Simulate("%s is not the right equipment for survey\n" %e)
        res = FAILURE
    elif ape.state.data[r] == 4:
        gui.Simulate("%s cannot store any more data\n" %r)
        res = FAILURE
    ape.state.load.ReleaseLock(r)
    ape.state.loc.ReleaseLock(r)
    ape.state.data.ReleaseLock(r)
    return res

def GetProbability_survey(r, l):
    e = ape.state.load[r]
    if e not in rv.TYPE:
        return [0.1, 0.9]
    elif ape.state.loc[r] == l and rv.TYPE[e] == 'survey' and ape.state.data[r] < 4:
        return [0.7,0.3]
    elif ape.state.loc[r] != l:
        return [0.1, 0.9]
    elif rv.TYPE[e] != 'survey':
        return [0.1, 0.9]
    elif ape.state.data[r] == 4:
        return [0.05, 0.95]

ape.declare_prob(survey, GetProbability_survey)

def survey_Sim(r, l, outcome):
    if outcome == 0:
        res = SUCCESS
        ape.state.data[r] += 1
    elif outcome == 1:
        res = FAILURE
    return res

def monitor(r, l):
    ape.state.load.AcquireLock(r)
    ape.state.loc.AcquireLock(r)
    ape.state.data.AcquireLock(r)
    e = ape.state.load[r]
    if e not in rv.TYPE:
        gui.Simulate("%s does not have any equipment\n" %r)
        res = FAILURE
    elif ape.state.loc[r] == l and rv.TYPE[e] == 'monitor' and r != 'UAV' and ape.state.data[r] < 4:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('monitor', start) == False):
            pass
        gui.Simulate("%s has monitored the location\n" %r)
        res = SUCCESS
        ape.state.data[r] += 1
    elif ape.state.loc[r] != l:
        gui.Simulate("%s is not in location %s\n" %(r, l))
        res = FAILURE
    elif rv.TYPE[e] != 'monitor':
        gui.Simulate("%s is not the right equipment for monitor\n" %e)
        res = FAILURE
    elif r == 'UAV':
        gui.Simulate("UAV cannot monitor\n")
        res = FAILURE
    elif ape.state.data[r] == 4:
        gui.Simulate("%s cannot store any more data\n" %r)
        res = FAILURE
    ape.state.load.ReleaseLock(r)
    ape.state.loc.ReleaseLock(r)
    ape.state.data.ReleaseLock(r)
    return res

def GetProbability_monitor(r, l):
    e = ape.state.load[r]
    if e not in rv.TYPE:
        return [0.1, 0.9]
    elif ape.state.loc[r] == l and rv.TYPE[e] == 'monitor' and r != 'UAV' and ape.state.data[r] < 4:
        return [0.7, 0.3]
    elif ape.state.loc[r] != l:
        return [0.1, 0.9]
    elif rv.TYPE[e] != 'monitor':
        return [0.1, 0.9]
    elif r == 'UAV':
        return [0.1, 0.9]
    elif ape.state.data[r] == 4:
        return [0.1, 0.9]
    return res

ape.declare_prob(monitor, GetProbability_monitor)
def monitor_Sim(r, l, outcome):
    if outcome == 0:
        res = SUCCESS
        ape.state.data[r] += 1
    elif outcome == 1:
        res = FAILURE
    return res

def screen(r, l):
    ape.state.load.AcquireLock(r)
    ape.state.loc.AcquireLock(r)
    ape.state.data.AcquireLock(r)
    e = ape.state.load[r]
    if e not in rv.TYPE:
        gui.Simulate("%s does not have any equipment\n" %r)
        res = FAILURE
    elif ape.state.loc[r] == l and rv.TYPE[e] == 'screen' and r != 'UAV' and ape.state.data[r] < 4:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('screen', start) == False):
            pass
        gui.Simulate("%s has screened the location\n" %r)
        res = SUCCESS
        ape.state.data[r] += 1
    elif ape.state.loc[r] != l:
        gui.Simulate("%s is not in location %s\n" %(r, l))
        res = FAILURE
    elif rv.TYPE[e] != 'screen':
        gui.Simulate("%s is not the right equipment for screening\n" %e)
        res = FAILURE
    elif r == 'UAV':
        gui.Simulate("UAV cannot do screening\n")
        res = FAILURE
    elif ape.state.data[r] == 4:
        gui.Simulate("%s cannot store any more data\n" %r)
        res = FAILURE
    ape.state.load.ReleaseLock(r)
    ape.state.loc.ReleaseLock(r)
    ape.state.data.ReleaseLock(r)
    return res

def GetProbability_screen(r, l):
    e = ape.state.load[r]
    if e not in rv.TYPE:
        return [0.1, 0.9]
    elif ape.state.loc[r] == l and rv.TYPE[e] == 'screen' and r != 'UAV' and ape.state.data[r] < 4:
        return [0.7, 0.3]
    elif ape.state.loc[r] != l:
        return [0.1, 0.9]
    elif rv.TYPE[e] != 'screen':
        return [0.1, 0.9]
    elif r == 'UAV':
        return [0.1, 0.9]
    elif ape.state.data[r] == 4:
        return [0.1, 0.9]
    return res

ape.declare_prob(screen, GetProbability_screen)
def screen_Sim(r, l, outcome):
    if outcome == 0:
        res = SUCCESS
        ape.state.data[r] += 1
    elif outcome == 1:
        res = FAILURE
    return res

def sample(r, l):
    ape.state.load.AcquireLock(r)
    ape.state.loc.AcquireLock(r)
    ape.state.data.AcquireLock(r)
    e = ape.state.load[r]
    if e not in rv.TYPE:
        gui.Simulate("%s does not have any equipment\n" %r)
        res = FAILURE
    elif ape.state.loc[r] == l and rv.TYPE[e] == 'sample' and r != 'UAV' and ape.state.data[r] < 4:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('sample', start) == False):
            pass
        gui.Simulate("%s has sampled the location\n" %r)
        res = SUCCESS
        ape.state.data[r] += 1
    elif ape.state.loc[r] != l:
        gui.Simulate("%s is not in location %s\n" %(r, l))
        res = FAILURE
    elif rv.TYPE[e] != 'sample':
        gui.Simulate("%s is not the right equipment for sampling\n" %e)
        res = FAILURE
    elif r == 'UAV':
        gui.Simulate("UAV cannot do sampling\n")
        res = FAILURE
    elif ape.state.data[r] == 4:
        gui.Simulate("%s cannot store any more data\n" %r)
        res = FAILURE
    ape.state.load.ReleaseLock(r)
    ape.state.loc.ReleaseLock(r)
    ape.state.data.ReleaseLock(r)
    return res

def GetProbability_sample(r, l):
    e = ape.state.load[r]
    if e not in rv.TYPE:        
        return [0.1, 0.9]
    elif ape.state.loc[r] == l and rv.TYPE[e] == 'sample' and r != 'UAV' and ape.state.data[r] < 4:
        return [0.7, 0.3]
    elif ape.state.loc[r] != l:
        return [0.1, 0.9]
    elif rv.TYPE[e] != 'sample':
        return [0.1, 0.9]
    elif r == 'UAV':
        return [0.1, 0.9]
    elif ape.state.data[r] == 4:
        return [0.1, 0.9]
    return res

ape.declare_prob(sample, GetProbability_sample)
def sample_Sim(r, l, outcome):
    if outcome == 0:
        res = SUCCESS
        ape.state.data[r] += 1
    elif outcome == 1:
        res = FAILURE
    return res

def process(r, l):
    ape.state.load.AcquireLock(r)
    ape.state.loc.AcquireLock(r)
    ape.state.data.AcquireLock(r)
    e = ape.state.load[r]
    if e not in rv.TYPE:
        gui.Simulate("%s does not have any equipment\n" %r)
        res = FAILURE
    elif ape.state.loc[r] == l and rv.TYPE[e] == 'process' and r != 'UAV' and ape.state.data[r] < 4:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('process', start) == False):
            pass
        gui.Simulate("%s has processed the location\n" %r)
        res = SUCCESS
        ape.state.data[r] += 1
    elif ape.state.loc[r] != l:
        gui.Simulate("%s is not in location %s\n" %(r, l))
        res = FAILURE
    elif rv.TYPE[e] != 'process':
        gui.Simulate("%s is not the right equipment for process\n" %e)
        res = FAILURE
    elif r == 'UAV':
        gui.Simulate("UAV cannot do processing\n")
        res = FAILURE
    elif ape.state.data[r] == 4:
        gui.Simulate("%s cannot store any more data\n" %r)
        res = FAILURE
    ape.state.load.ReleaseLock(r)
    ape.state.loc.ReleaseLock(r)
    ape.state.data.ReleaseLock(r)
    return res

def GetProbability_process(r, l):
    e = ape.state.load[r]
    if e not in rv.TYPE:
        return [0.1, 0.9]
    elif ape.state.loc[r] == l and rv.TYPE[e] == 'process' and r != 'UAV' and ape.state.data[r] < 4:
        return [0.7, 0.3]
        ape.state.data[r] += 1
    elif ape.state.loc[r] != l:
        return [0.1, 0.9]
    elif rv.TYPE[e] != 'process':
        return [0.1, 0.9]
    elif r == 'UAV':
        return [0.1, 0.9]
    elif ape.state.data[r] == 4:
        return [0.1, 0.9]
    return res

ape.declare_prob(process, GetProbability_process)
def process_Sim(r, l, outcome):
    if outcome == 0:
        res = SUCCESS
        ape.state.data[r] += 1
    elif outcome == 1:
        res = FAILURE
    return res

def alienSpotted(l):
    gui.Simulate("An alien is spotted in location %s", l)
    return SUCCESS

def handleAlien(r, l):
    if ape.state.loc[r] == l:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('negotiate', start) == False):
            pass
        gui.Simulate("Robot %s is negotiating with alien.\n" %r)
        res = SUCCESS
    else:
        gui.Simulate("Robot %s is not in alien's location\n" %r)
        res = FAILURE
    return res

def GetProbability_handleAlien(r, l):
    if ape.state.loc[r] == l:
        return [0.5, 0.5]
    else:
        return [0.1, 0.9]

ape.declare_prob(handleAlien, GetProbability_handleAlien)
def handleAlien_Sim(r, l, outcome):
    if outcome == 0:
        res = SUCCESS
    else:
        res = FAILURE
    return res

def charge(r, c):
    ape.state.loc.AcquireLock(r)
    ape.state.pos.AcquireLock(c)
    if ape.state.loc[r] == ape.state.pos[c] or ape.state.pos[c] == r:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('charge', start) == False):
            pass
        ape.state.charge.AcquireLock(r)
        ape.state.charge[r] = 100
        gui.Simulate("%s is fully charged\n" %r)
        ape.state.charge.ReleaseLock(r)
        res = SUCCESS
    else:
        gui.Simulate("%s is not in the charger's location or it doesn't have the charger with it\n" %r)
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
        ape.state.charge[r] = 100
        res = SUCCESS
    else:
        res = FAILURE
    return res

def move(r, l1, l2):
    ape.state.loc.AcquireLock(r)
    ape.state.charge.AcquireLock(r)
    dist = EE_GETDISTANCE(l1, l2)
    if l1 == l2:
        gui.Simulate("%s is already at location %s\n" %(r, l2))
        res = SUCCESS
    elif ape.state.loc[r] == l1 and ape.state.charge[r] >= dist:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('move', start) == False):
            pass
        gui.Simulate("%s has moved from %s to %s\n" %(r, l1, l2))
        ape.state.loc[r] = l2
        ape.state.charge[r] = ape.state.charge[r] - dist
        res = SUCCESS
    elif ape.state.loc[r] != l1 and ape.state.charge[r] >= dist:
        gui.Simulate("%s is not in location %s\n" %(r, l1))
        res = FAILURE
    elif ape.state.loc[r] == l1 and ape.state.charge[r] < dist:
        gui.Simulate("%s does not have any charge to move :(\n" %r)
        res = FAILURE
    else:
        gui.Simulate("%s is not at location %s and it doesn't have enough charge!\n" %(r, l1))
        res = FAILURE
    ape.state.loc.ReleaseLock(r)
    ape.state.charge.ReleaseLock(r)
    return res

def GetProbability_move(r, l1, l2):
    dist = EE_GETDISTANCE(l1, l2)
    if l1 == l2:
        return [1, 0, 0]
    elif ape.state.loc[r] == l1 and ape.state.charge[r] >= dist:
        return [0.1, 0.7, 0.2]
    elif ape.state.loc[r] != l1 and ape.state.charge[r] >= dist:
        return [0.1, 0.1, 0.8]
    elif ape.state.loc[r] == l1 and ape.state.charge[r] < dist:
        return [0.1, 0.1, 0.8]
    else:
        return [0.1, 0.1, 0.8]

ape.declare_prob(move, GetProbability_move)
def move_Sim(r, l1, l2, outcome):
    dist = EE_GETDISTANCE(l1, l2)
    if outcome == 0:
        res = SUCCESS
    elif outcome == 1:
        ape.state.loc[r] = l2
        ape.state.charge[r] = ape.state.charge[r] - dist
        res = SUCCESS
    elif outcome == 2:
        res = FAILURE
    return res

def fly(r, l1, l2):

    ape.state.loc.AcquireLock(r)
    ape.state.charge.AcquireLock(r)

    dist = EE_GETDISTANCE(l1, l2)
    if r != 'UAV':
        gui.Simulate("%s cannot fly\n" %r)
        res = FAILURE
    elif l1 == l2:
        gui.Simulate("%s is already at location %s\n" %(r, l2))
        res = SUCCESS
    elif ape.state.loc[r] == l1 and ape.state.charge[r] >= dist:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('fly', start) == False):
            pass
        gui.Simulate("%s has flied from %s to %s\n" %(r, l1, l2))
        ape.state.loc[r] = l2
        ape.state.charge[r] = ape.state.charge[r] - dist
        res = SUCCESS
    elif ape.state.loc[r] != l1 and ape.state.charge[r] >= dist:
        gui.Simulate("%s is not in location %s\n" %(r, l1))
        res = FAILURE
    elif ape.state.loc[r] == l1 and ape.state.charge[r] < dist:
        gui.Simulate("%s does not have any charge to move :(\n" %r)
        res = FAILURE
    else:
        gui.Simulate("%s is not at location %s and it doesn't have enough charge!\n" %(r, l1))
        res = FAILURE
    ape.state.loc.ReleaseLock(r)
    ape.state.charge.ReleaseLock(r)
    return res

def GetProbability_fly(r, l1, l2):
    dist = EE_GETDISTANCE(l1, l2)
    if r != 'UAV':
        return [0.1, 0.1, 0.8]
    elif l1 == l2:
        return [0.9, 0.05, 0.05]
    elif ape.state.loc[r] == l1 and ape.state.charge[r] >= dist:
        return [0.1, 0.7, 0.2]
    elif ape.state.loc[r] != l1 and ape.state.charge[r] >= dist:
        return [0.0, 0.1, 0.9]
    elif ape.state.loc[r] == l1 and ape.state.charge[r] < dist:
        return [0.0, 0.1, 0.9]
    else:
        return [0.0, 0.1, 0.9]

ape.declare_prob(fly, GetProbability_fly)

def fly_Sim(r, l1, l2, outcome):
    dist = EE_GETDISTANCE(l1, l2)
    if outcome == 0:
        res = SUCCESS
    elif outcome == 1:
        ape.state.loc[r] = l2
        ape.state.charge[r] = ape.state.charge[r] - dist
        res = SUCCESS
    elif outcome == 2:
        res = FAILURE
    return res

def take(r, o):
    ape.state.load.AcquireLock(r)
    if ape.state.load[r] == NIL:
        ape.state.loc.AcquireLock(r)
        ape.state.pos.AcquireLock(o)
        if ape.state.loc[r] == ape.state.pos[o]:
            start = globalTimer.GetTime()
            while(globalTimer.IsCommandExecutionOver('take', start) == False):
                pass
            gui.Simulate("%s has picked up %s\n" %(r, o))
            ape.state.pos[o] = r
            ape.state.load[r] = o
            res = SUCCESS
        else:
            gui.Simulate("%s is not at %s's location\n" %(r, o))
            res = FAILURE
        ape.state.loc.ReleaseLock(r)
        ape.state.pos.ReleaseLock(o)
    else:
        gui.Simulate("%s is not free to take anything\n" %r)
        res = FAILURE
    ape.state.load.ReleaseLock(r)
    return res

def GetProbability_take(r, o):
    if ape.state.load[r] == NIL:
        if ape.state.loc[r] == ape.state.pos[o]:
            return [0.9, 0.1]
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
    ape.state.loc.AcquireLock(r)
    ape.state.pos.AcquireLock(o)
    if ape.state.pos[o] == r:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('put', start) == False):
            pass
        ape.state.pos[o] = ape.state.loc[r]
        ape.state.load[r] = NIL
        gui.Simulate("%s has put %s at location %s\n" %(r,o,ape.state.loc[r]))
        res = SUCCESS
    else:
        gui.Simulate("%s is not with %s\n" %(o,r))
        res = FAILURE
    ape.state.loc.ReleaseLock(r)
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

def deposit(r):
    ape.state.loc.AcquireLock(r)
    ape.state.data.AcquireLock(r)
    if ape.state.loc[r] == 'base':
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('deposit', start) == False):
            pass
        gui.Simulate("%s has deposited data in the base\n" %r)
        ape.state.data[r] = 0
        res = SUCCESS
    else:
        gui.Simulate("%s is not in base, so it cannot deposit data.\n" %r)
        res = FAILURE
    ape.state.loc.ReleaseLock(r)
    ape.state.data.ReleaseLock(r)
    return res

def GetProbability_deposit(r):
    if ape.state.loc[r] == 'base':
        return [0.8, 0.2]
    else:
        return [0.2, 0.8]

ape.declare_prob(deposit, GetProbability_deposit)
def deposit_Sim(r, outcome):
    if outcome == 0:
        ape.state.data[r] = 0
        res = SUCCESS
    else:
        res = FAILURE
    return res

def transferData(r1, r2):
    ape.state.loc.AcquireLock(r1)
    ape.state.loc.AcquireLock(r2)
    ape.state.data.AcquireLock(r1)
    ape.state.data.AcquireLock(r2)

    if ape.state.loc[r1] != ape.state.loc[r2]:
        gui.Simulate("%s and %s are not in same location.\n" %(r1, r2))
        res = FAILURE
    elif ape.state.data[r2] + ape.state.data[r1] <= 4:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('transferData', start) == False):
            pass
        gui.Simulate("%s transfered data to %s\n" %(r1, r2))
        ape.state.data[r2] += ape.state.data[r1]
        ape.state.data[r1] = 0
        res = SUCCESS
    elif ape.state.data[r2] < 4:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('transferData', start) == False):
            pass
        t = 4 - ape.state.data[r2]
        ape.state.data[r2] = 4
        ape.state.data[r1] -= t
        gui.Simulate("%s transfered data to %s\n" %(r1, r2))
        res = SUCCESS
    ape.state.loc.ReleaseLock(r1)
    ape.state.loc.ReleaseLock(r2)
    ape.state.data.ReleaseLock(r1)
    ape.state.data.ReleaseLock(r2)
    return res

def GetProbability_transferData(r1, r2):
    if ape.state.loc[r1] != ape.state.loc[r2]:
        return [0.8, 0.1, 0.1]
    elif ape.state.data[r2] + ape.state.data[r1] <= 4:
        return [0.1, 0.5, 0.4]
    elif ape.state.data[r2] < 4:
        return [0.1, 0.3, 0.6]

ape.declare_prob(transferData, GetProbability_transferData)
def transferData_Sim(r1, r2, outcome):
    if outcome == 2:
        res = FAILURE
    elif outcome == 0:
        ape.state.data[r2] += ape.state.data[r1]
        ape.state.data[r1] = 0
        res = SUCCESS
    elif outcome == 1:
        t = 4 - ape.state.data[r2]
        ape.state.data[r2] = 4
        ape.state.data[r1] -= t
        res = SUCCESS
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
    return SUCCESS

def GetEquipment_Method1(r, activity):
    if ape.state.load[r] != rv.EQUIPMENT[activity]:
        ape.do_task('moveTo', r, ape.state.pos[rv.EQUIPMENT[activity]])
        ape.do_command(take, r, rv.EQUIPMENT[activity])
    return SUCCESS

def GetEquipment_Method2(r, activity):
    if ape.state.load[r] != rv.EQUIPMENT[activity]:
        ape.do_task('moveTo', r, ape.state.pos[rv.EQUIPMENT[activity]])
        ape.state.load.AcquireLock(r)
        if ape.state.load[r] != NIL:
            x = ape.state.load[r]
            ape.state.load.ReleaseLock(r)
            ape.do_command(put, r, x)
        else:
            ape.state.load.ReleaseLock(r)
        ape.do_command(take, r, rv.EQUIPMENT[activity])
    return SUCCESS

def GetEquipment_Method3(r, activity):
    if ape.state.load[r] != rv.EQUIPMENT[activity]:
        loc = ape.state.pos[rv.EQUIPMENT[activity]]
        if loc not in rv.LOCATIONS:
            robo = loc
            ape.do_task('moveTo', r, ape.state.loc[robo])
            ape.state.load.AcquireLock(r)
            if ape.state.load[r] != NIL:
                x = ape.state.load[r]
                ape.state.load.ReleaseLock(r)
                ape.do_command(put, r, x)
            else:
                ape.state.load.ReleaseLock(r)
            ape.do_command(put, robo, rv.EQUIPMENT[activity])
            ape.do_command(take, r, rv.EQUIPMENT[activity])
        else:
            return FAILURE
    return SUCCESS

def MoveTo_MethodHelper(r, l):
    res = SUCCESS
    path = EE_GETPATH(ape.state.loc[r], l)
    if path == {}:
        gui.Simulate("%s is already at location %s \n" %(r, l))
    else:
        lTemp = ape.state.loc[r]
        if lTemp not in path:
            gui.Simulate("%s is out of its path to %s\n" %(r, l))
            res = FAILURE
        else:
            while(lTemp != l):
                lNext = path[lTemp]
                ape.do_command(move, r, lTemp, lNext)
                if lNext != ape.state.loc[r]:
                    gui.Simulate("%s is out of its path to %s\n" %(r, l))
                    res = FAILURE
                    break
                else:
                    lTemp = lNext
    return res

def MoveTo_Method1(r, l):
    if l not in rv.LOCATIONS:
        gui.Simulate("%s is trying to go to an invalid location\n" %r)
        res = FAILURE
    else:
        res = MoveTo_MethodHelper(r, l)
    return res

# def MoveTo_Method2(r, l):
#     if l not in rv.LOCATIONS:
#         gui.Simulate("%s is trying to go to an invalid location\n" %r)
#         res = FAILURE
#     else:
#         dist = EE_GETDISTANCE(ape.state.loc[r], l)
#         if ape.state.charge[r] >= dist:
#             res = MoveTo_MethodHelper(r, l)
#         else:
#             gui.Simulate("Insufficient charge! only %.2f%%. %s cannot move\n" %(ape.state.charge[r], r))
#             res = FAILURE
#     return res

def MoveTo_Method2(r, l):
    if l not in rv.LOCATIONS:
        gui.Simulate("%s is trying to go to an invalid location\n" %r)
        res = FAILURE
    else:
        dist = EE_GETDISTANCE(ape.state.loc[r], l)
        if ape.state.charge[r] >= dist:
            res = MoveTo_MethodHelper(r, l)
        else:
            ape.do_task('recharge', r)
            ape.do_task('moveTo', r, l)
            res = SUCCESS
    return res

def FlyTo_Method1(r, l):
    if r == 'UAV':
        ape.do_command(fly, r, ape.state.loc[r], l)
        res = SUCCESS
    else:
        gui.Simulate("%s is not a UAV. So, it cannot fly\n" %r)
        res = FAILURE
    return res

# def FlyTo_Method2(r, l):
#     dist = EE_GETDISTANCE(ape.state.loc[r], l)
#     if r == 'UAV':
#         if ape.state.charge[r] >= dist:
#             ape.do_command(fly, r, ape.state.loc[r], l)
#             res = SUCCESS
#         else:
#             gui.Simulate("Insufficient charge! only %.2f%%. %s cannot move\n" %(ape.state.charge[r], r))
#             res = FAILURE
#     else:
#         gui.Simulate("%s is not a UAV. So, it cannot fly\n" %r)
#         res = FAILURE
#     return res

def FlyTo_Method2(r, l):
    dist = EE_GETDISTANCE(ape.state.loc[r], l)
    if r == 'UAV':
        if ape.state.charge[r] >= dist:
            ape.do_command(fly, r, ape.state.loc[r], l)
            res = SUCCESS
        else:
            ape.do_task('recharge', r)
            ape.do_task('flyTo', r, l)
            res = SUCCESS
    else:
        gui.Simulate("%s is not a UAV. So, it cannot fly\n" %r)
        res = FAILURE
    return res

def DepositData_Method1(r):
    if ape.state.data[r] > 0:
        ape.do_task('moveTo', r, 'base')
        ape.do_command(deposit, r)
    else:
        gui.Simulate("%s has no data to deposit.\n" %r)
    return SUCCESS

def DepositData_Method2(r):
    if ape.state.data[r] > 0:
        if r != 'UAV':
            ape.do_task('flyTo', 'UAV', ape.state.loc[r])
            ape.do_command(transferData, r, 'UAV')
        ape.do_task('flyTo', 'UAV', 'base')
        ape.do_command(deposit, 'UAV')
    else:
        gui.Simulate("%s has no data to deposit.\n" %r)
    return SUCCESS

def Recharge_Method1(r):
    c = 'c1'
    if ape.state.pos[c] not in rv.LOCATIONS and ape.state.pos[c] != r:
        gui.Simulate("%s cannot find charger %s\n" %(r, c))
        res = FAILURE
    elif ape.state.loc[r] != ape.state.pos[c] and ape.state.pos[c] != r:
        dist = EE_GETDISTANCE(ape.state.loc[r], ape.state.pos[c])
        if ape.state.charge[r] >= dist:
            ape.do_task('moveTo', r, ape.state.pos[c])
            ape.do_command(charge, r, c)
            res = SUCCESS
        else:
            gui.Simulate("%s is stranded without any possibility of charging\n" %r)
            res = FAILURE
    else:
        ape.do_command(charge, r, c)
        res = SUCCESS
    return res

def Recharge_Method2(r):
    c = 'c1'
    if ape.state.pos[c] not in rv.LOCATIONS and ape.state.pos[c] != r:
        gui.Simulate("%s cannot find charger %s\n" %(r, c))
        res = FAILURE
    elif ape.state.loc[r] != ape.state.pos[c] and ape.state.pos[c] != r:
        dist = EE_GETDISTANCE(ape.state.loc[r], ape.state.pos[c])
        if ape.state.charge[r] >= dist:
            ape.do_task('moveTo', r, ape.state.pos[c])
            ape.do_command(charge, r, c)
            ape.do_command(take, r, c)
            res = SUCCESS
        else:
            gui.Simulate("%s is stranded without any possibility of charging\n" %r)
            res = FAILURE
    else:
        ape.do_command(charge, r, c)
        ape.do_command(take, r, c)
        res = SUCCESS
    return res

def DoActivities_Method1(r, actList):
    for act in actList:
        ape.do_task('explore', r, act[0], act[1])
        ape.do_task('depositData', r)
    return SUCCESS

def DoActivities_Method2(r, actList):
    for act in actList:
        ape.do_task('explore', r, act[0], act[1])
    ape.do_task('depositData', r)
    return SUCCESS

def DoActivities_Method3(r, actList):
    for act in actList:
        ape.do_task('explore', r, act[0], act[1])
        ape.do_task('depositData', r)
        ape.do_task('recharge', r)
    return SUCCESS

def DoActivities_Method4(r, actList):
    for act in actList:
        ape.do_task('explore', r, act[0], act[1])
        ape.do_task('recharge', r)
    ape.do_task('depositData', r)
    return SUCCESS

def HandleEmergency_Method1(r, l):
    ape.do_task('recharge', r)
    ape.do_task('moveTo', r, l)
    ape.do_command(handleAlien, r, l)
    return SUCCESS

def HandleEmergency_Method2(r, l):
    ape.do_task('moveTo', r, l)
    ape.do_command(handleAlien, r, l)
    return SUCCESS

rv = RV()
ape.declare_commands([survey, monitor, screen, sample, process, charge, move, put, take, fly, deposit, transferData, handleAlien],
                      [survey_Sim, monitor_Sim, screen_Sim, sample_Sim, process_Sim, charge_Sim, move_Sim, put_Sim, take_Sim, fly_Sim, deposit_Sim, transferData_Sim, handleAlien_Sim])

ape.declare_methods('explore', Explore_Method1)
ape.declare_methods('getEquipment', GetEquipment_Method1, GetEquipment_Method2, GetEquipment_Method3)
ape.declare_methods('moveTo', MoveTo_Method1)
ape.declare_methods('flyTo', FlyTo_Method1)
ape.declare_methods('recharge', Recharge_Method1, Recharge_Method2)
ape.declare_methods('depositData', DepositData_Method1, DepositData_Method2)
ape.declare_methods('doActivities', DoActivities_Method2, DoActivities_Method4, DoActivities_Method1, DoActivities_Method3)
ape.declare_methods('handleEmergency', HandleEmergency_Method2, HandleEmergency_Method1)


