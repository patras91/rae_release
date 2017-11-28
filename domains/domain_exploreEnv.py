__author__ = 'patras'

from domain_constants import *
import rae1
import gui
from timer import globalTimer

'''A UAV and several robots explore environment and collect data.
UAV can only survey whereas robots can survey, monitor, screen, sample and process.
UAV can fly whereas a robot can only move on the ground. The UAV and robots have limited
charge and needs to be charged frequently. They also have a capacity of the amount of data
they can carry with them. They can store data in the base location. UAV needs to return to
base location every night.'''

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
    rae1.state.load.AcquireLock(r)
    rae1.state.loc.AcquireLock(r)
    rae1.state.data.AcquireLock(r)
    e = rae1.state.load[r]
    if e not in rv.TYPE:
        gui.Simulate("%s does not have any equipment\n" %r)
        res = FAILURE
    elif rae1.state.loc[r] == l and rv.TYPE[e] == 'survey' and rae1.state.data[r] < 4:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('survey', start) == False):
			pass
        gui.Simulate("%s has surveyed the location %s\n" %(r, l))
        res = SUCCESS
        rae1.state.data[r] += 1
    elif rae1.state.loc[r] != l:
        gui.Simulate("%s is not in location %s\n" %(r, l))
        res = FAILURE
    elif rv.TYPE[e] != 'survey':
        gui.Simulate("%s is not the right equipment for survey\n" %e)
        res = FAILURE
    elif rae1.state.data[r] == 4:
        gui.Simulate("%s cannot store any more data\n" %r)
        res = FAILURE
    rae1.state.load.ReleaseLock(r)
    rae1.state.loc.ReleaseLock(r)
    rae1.state.data.ReleaseLock(r)
    return res

def survey_Sim(r, l):
    rae1.state.load.AcquireLock(r)
    rae1.state.loc.AcquireLock(r)
    rae1.state.data.AcquireLock(r)
    e = rae1.state.load[r]
    if e not in rv.TYPE:
        gui.Simulate("%s does not have any equipment\n" %r)
        res = FAILURE
    elif rae1.state.loc[r] == l and rv.TYPE[e] == 'survey' and rae1.state.data[r] < 4:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('survey', start) == False):
			pass
        gui.Simulate("%s has surveyed the location %s\n" %(r, l))
        res = SUCCESS
        rae1.state.data[r] += 1
    elif rae1.state.loc[r] != l:
        gui.Simulate("%s is not in location %s\n" %(r, l))
        res = FAILURE
    elif rv.TYPE[e] != 'survey':
        gui.Simulate("%s is not the right equipment for survey\n" %e)
        res = FAILURE
    elif rae1.state.data[r] == 4:
        gui.Simulate("%s cannot store any more data\n" %r)
        res = FAILURE
    rae1.state.load.ReleaseLock(r)
    rae1.state.loc.ReleaseLock(r)
    rae1.state.data.ReleaseLock(r)
    return res

def monitor(r, l):
    rae1.state.load.AcquireLock(r)
    rae1.state.loc.AcquireLock(r)
    rae1.state.data.AcquireLock(r)
    e = rae1.state.load[r]
    if e not in rv.TYPE:
        gui.Simulate("%s does not have any equipment\n" %r)
        res = FAILURE
    elif rae1.state.loc[r] == l and rv.TYPE[e] == 'monitor' and r != 'UAV' and rae1.state.data[r] < 4:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('monitor', start) == False):
			pass
        gui.Simulate("%s has monitored the location\n" %r)
        res = SUCCESS
        rae1.state.data[r] += 1
    elif rae1.state.loc[r] != l:
        gui.Simulate("%s is not in location %s\n" %(r, l))
        res = FAILURE
    elif rv.TYPE[e] != 'monitor':
        gui.Simulate("%s is not the right equipment for monitor\n" %e)
        res = FAILURE
    elif r == 'UAV':
        gui.Simulate("UAV cannot monitor\n")
        res = FAILURE
    elif rae1.state.data[r] == 4:
        gui.Simulate("%s cannot store any more data\n" %r)
        res = FAILURE
    rae1.state.load.ReleaseLock(r)
    rae1.state.loc.ReleaseLock(r)
    rae1.state.data.ReleaseLock(r)
    return res

def monitor_Sim(r, l):
    rae1.state.load.AcquireLock(r)
    rae1.state.loc.AcquireLock(r)
    rae1.state.data.AcquireLock(r)
    e = rae1.state.load[r]
    if e not in rv.TYPE:
        gui.Simulate("%s does not have any equipment\n" %r)
        res = FAILURE
    elif rae1.state.loc[r] == l and rv.TYPE[e] == 'monitor' and r != 'UAV' and rae1.state.data[r] < 4:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('monitor', start) == False):
			pass
        gui.Simulate("%s has monitored the location\n" %r)
        res = SUCCESS
        rae1.state.data[r] += 1
    elif rae1.state.loc[r] != l:
        gui.Simulate("%s is not in location %s\n" %(r, l))
        res = FAILURE
    elif rv.TYPE[e] != 'monitor':
        gui.Simulate("%s is not the right equipment for monitor\n" %e)
        res = FAILURE
    elif r == 'UAV':
        gui.Simulate("UAV cannot monitor\n")
        res = FAILURE
    elif rae1.state.data[r] == 4:
        gui.Simulate("%s cannot store any more data\n" %r)
        res = FAILURE
    rae1.state.load.ReleaseLock(r)
    rae1.state.loc.ReleaseLock(r)
    rae1.state.data.ReleaseLock(r)
    return res

def screen(r, l):
    rae1.state.load.AcquireLock(r)
    rae1.state.loc.AcquireLock(r)
    rae1.state.data.AcquireLock(r)
    e = rae1.state.load[r]
    if e not in rv.TYPE:
        gui.Simulate("%s does not have any equipment\n" %r)
        res = FAILURE
    elif rae1.state.loc[r] == l and rv.TYPE[e] == 'screen' and r != 'UAV' and rae1.state.data[r] < 4:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('screen', start) == False):
			pass
        gui.Simulate("%s has screened the location\n" %r)
        res = SUCCESS
        rae1.state.data[r] += 1
    elif rae1.state.loc[r] != l:
        gui.Simulate("%s is not in location %s\n" %(r, l))
        res = FAILURE
    elif rv.TYPE[e] != 'screen':
        gui.Simulate("%s is not the right equipment for screening\n" %e)
        res = FAILURE
    elif r == 'UAV':
        gui.Simulate("UAV cannot do screening\n")
        res = FAILURE
    elif rae1.state.data[r] == 4:
        gui.Simulate("%s cannot store any more data\n" %r)
        res = FAILURE
    rae1.state.load.ReleaseLock(r)
    rae1.state.loc.ReleaseLock(r)
    rae1.state.data.ReleaseLock(r)
    return res

def screen_Sim(r, l):
    rae1.state.load.AcquireLock(r)
    rae1.state.loc.AcquireLock(r)
    rae1.state.data.AcquireLock(r)
    e = rae1.state.load[r]
    if e not in rv.TYPE:
        gui.Simulate("%s does not have any equipment\n" %r)
        res = FAILURE
    elif rae1.state.loc[r] == l and rv.TYPE[e] == 'screen' and r != 'UAV' and rae1.state.data[r] < 4:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('screen', start) == False):
			pass
        gui.Simulate("%s has screened the location\n" %r)
        res = SUCCESS
        rae1.state.data[r] += 1
    elif rae1.state.loc[r] != l:
        gui.Simulate("%s is not in location %s\n" %(r, l))
        res = FAILURE
    elif rv.TYPE[e] != 'screen':
        gui.Simulate("%s is not the right equipment for screening\n" %e)
        res = FAILURE
    elif r == 'UAV':
        gui.Simulate("UAV cannot do screening\n")
        res = FAILURE
    elif rae1.state.data[r] == 4:
        gui.Simulate("%s cannot store any more data\n" %r)
        res = FAILURE
    rae1.state.load.ReleaseLock(r)
    rae1.state.loc.ReleaseLock(r)
    rae1.state.data.ReleaseLock(r)
    return res

def sample(r, l):
    rae1.state.load.AcquireLock(r)
    rae1.state.loc.AcquireLock(r)
    rae1.state.data.AcquireLock(r)
    e = rae1.state.load[r]
    if e not in rv.TYPE:
        gui.Simulate("%s does not have any equipment\n" %r)
        res = FAILURE
    elif rae1.state.loc[r] == l and rv.TYPE[e] == 'sample' and r != 'UAV' and rae1.state.data[r] < 4:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('sample', start) == False):
			pass
        gui.Simulate("%s has sampled the location\n" %r)
        res = SUCCESS
        rae1.state.data[r] += 1
    elif rae1.state.loc[r] != l:
        gui.Simulate("%s is not in location %s\n" %(r, l))
        res = FAILURE
    elif rv.TYPE[e] != 'sample':
        gui.Simulate("%s is not the right equipment for sampling\n" %e)
        res = FAILURE
    elif r == 'UAV':
        gui.Simulate("UAV cannot do sampling\n")
        res = FAILURE
    elif rae1.state.data[r] == 4:
        gui.Simulate("%s cannot store any more data\n" %r)
        res = FAILURE
    rae1.state.load.ReleaseLock(r)
    rae1.state.loc.ReleaseLock(r)
    rae1.state.data.ReleaseLock(r)
    return res

def sample_Sim(r, l):
    rae1.state.load.AcquireLock(r)
    rae1.state.loc.AcquireLock(r)
    rae1.state.data.AcquireLock(r)
    e = rae1.state.load[r]
    if e not in rv.TYPE:
        gui.Simulate("%s does not have any equipment\n" %r)
        res = FAILURE
    elif rae1.state.loc[r] == l and rv.TYPE[e] == 'sample' and r != 'UAV' and rae1.state.data[r] < 4:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('sample', start) == False):
			pass
        gui.Simulate("%s has sampled the location\n" %r)
        res = SUCCESS
        rae1.state.data[r] += 1
    elif rae1.state.loc[r] != l:
        gui.Simulate("%s is not in location %s\n" %(r, l))
        res = FAILURE
    elif rv.TYPE[e] != 'sample':
        gui.Simulate("%s is not the right equipment for sampling\n" %e)
        res = FAILURE
    elif r == 'UAV':
        gui.Simulate("UAV cannot do sampling\n")
        res = FAILURE
    elif rae1.state.data[r] == 4:
        gui.Simulate("%s cannot store any more data\n" %r)
        res = FAILURE
    rae1.state.load.ReleaseLock(r)
    rae1.state.loc.ReleaseLock(r)
    rae1.state.data.ReleaseLock(r)
    return res

def process(r, l):
    rae1.state.load.AcquireLock(r)
    rae1.state.loc.AcquireLock(r)
    rae1.state.data.AcquireLock(r)
    e = rae1.state.load[r]
    if e not in rv.TYPE:
        gui.Simulate("%s does not have any equipment\n" %r)
        res = FAILURE
    elif rae1.state.loc[r] == l and rv.TYPE[e] == 'process' and r != 'UAV' and rae1.state.data[r] < 4:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('process', start) == False):
			pass
        gui.Simulate("%s has processed the location\n" %r)
        res = SUCCESS
        rae1.state.data[r] += 1
    elif rae1.state.loc[r] != l:
        gui.Simulate("%s is not in location %s\n" %(r, l))
        res = FAILURE
    elif rv.TYPE[e] != 'process':
        gui.Simulate("%s is not the right equipment for process\n" %e)
        res = FAILURE
    elif r == 'UAV':
        gui.Simulate("UAV cannot do processing\n")
        res = FAILURE
    elif rae1.state.data[r] == 4:
        gui.Simulate("%s cannot store any more data\n" %r)
        res = FAILURE
    rae1.state.load.ReleaseLock(r)
    rae1.state.loc.ReleaseLock(r)
    rae1.state.data.ReleaseLock(r)
    return res

def process_Sim(r, l):
    rae1.state.load.AcquireLock(r)
    rae1.state.loc.AcquireLock(r)
    rae1.state.data.AcquireLock(r)
    e = rae1.state.load[r]
    if e not in rv.TYPE:
        gui.Simulate("%s does not have any equipment\n" %r)
        res = FAILURE
    elif rae1.state.loc[r] == l and rv.TYPE[e] == 'process' and r != 'UAV' and rae1.state.data[r] < 4:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('process', start) == False):
			pass
        gui.Simulate("%s has processed the location\n" %r)
        res = SUCCESS
        rae1.state.data[r] += 1
    elif rae1.state.loc[r] != l:
        gui.Simulate("%s is not in location %s\n" %(r, l))
        res = FAILURE
    elif rv.TYPE[e] != 'process':
        gui.Simulate("%s is not the right equipment for process\n" %e)
        res = FAILURE
    elif r == 'UAV':
        gui.Simulate("UAV cannot do processing\n")
        res = FAILURE
    elif rae1.state.data[r] == 4:
        gui.Simulate("%s cannot store any more data\n" %r)
        res = FAILURE
    rae1.state.load.ReleaseLock(r)
    rae1.state.loc.ReleaseLock(r)
    rae1.state.data.ReleaseLock(r)
    return res

def charge(r, c):
    rae1.state.loc.AcquireLock(r)
    rae1.state.pos.AcquireLock(c)
    if rae1.state.loc[r] == rae1.state.pos[c] or rae1.state.pos[c] == r:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('charge', start) == False):
			pass
        rae1.state.charge.AcquireLock(r)
        rae1.state.charge[r] = 75
        gui.Simulate("%s is fully charged\n" %r)
        rae1.state.charge.ReleaseLock(r)
        res = SUCCESS
    else:
        gui.Simulate("%s is not in the charger's location or it doesn't have the charger with it\n" %r)
        res = FAILURE
    rae1.state.loc.ReleaseLock(r)
    rae1.state.pos.ReleaseLock(c)
    return res

def charge_Sim(r, c):
    rae1.state.loc.AcquireLock(r)
    rae1.state.pos.AcquireLock(c)
    if rae1.state.loc[r] == rae1.state.pos[c] or rae1.state.pos[c] == r:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('charge', start) == False):
			pass
        rae1.state.charge.AcquireLock(r)
        rae1.state.charge[r] = 75
        gui.Simulate("%s is fully charged\n" %r)
        rae1.state.charge.ReleaseLock(r)
        res = SUCCESS
    else:
        gui.Simulate("%s is not in the charger's location or it doesn't have the charger with it\n" %r)
        res = FAILURE
    rae1.state.loc.ReleaseLock(r)
    rae1.state.pos.ReleaseLock(c)
    return res

def move(r, l1, l2):
    rae1.state.loc.AcquireLock(r)
    rae1.state.charge.AcquireLock(r)
    dist = EE_GETDISTANCE(l1, l2)
    if l1 == l2:
        gui.Simulate("%s is already at location %s\n" %(r, l2))
        res = SUCCESS
    elif rae1.state.loc[r] == l1 and rae1.state.charge[r] >= dist:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('move', start) == False):
			pass
        gui.Simulate("%s has moved from %s to %s\n" %(r, l1, l2))
        rae1.state.loc[r] = l2
        rae1.state.charge[r] = rae1.state.charge[r] - dist
        res = SUCCESS
    elif rae1.state.loc[r] != l1 and rae1.state.charge[r] >= dist:
        gui.Simulate("%s is not in location %s\n" %(r, l1))
        res = FAILURE
    elif rae1.state.loc[r] == l1 and rae1.state.charge[r] < dist:
        gui.Simulate("%s does not have any charge to move :(\n" %r)
        res = FAILURE
    else:
        gui.Simulate("%s is not at location %s and it doesn't have enough charge!\n" %(r, l1))
        res = FAILURE
    rae1.state.loc.ReleaseLock(r)
    rae1.state.charge.ReleaseLock(r)
    return res

def move_Sim(r, l1, l2):
    rae1.state.loc.AcquireLock(r)
    rae1.state.charge.AcquireLock(r)
    print("crossed")
    dist = EE_GETDISTANCE(l1, l2)
    if l1 == l2:
        gui.Simulate("%s is already at location %s\n" %(r, l2))
        res = SUCCESS
    elif rae1.state.loc[r] == l1 and rae1.state.charge[r] >= dist:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('move', start) == False):
			pass
        gui.Simulate("%s has moved from %s to %s\n" %(r, l1, l2))
        rae1.state.loc[r] = l2
        rae1.state.charge[r] = rae1.state.charge[r] - dist
        res = SUCCESS
    elif rae1.state.loc[r] != l1 and rae1.state.charge[r] >= dist:
        gui.Simulate("%s is not in location %s\n" %(r, l1))
        res = FAILURE
    elif rae1.state.loc[r] == l1 and rae1.state.charge[r] < dist:
        gui.Simulate("%s does not have any charge to move :(\n" %r)
        res = FAILURE
    else:
        gui.Simulate("%s is not at location %s and it doesn't have enough charge!\n" %(r, l1))
        res = FAILURE
    rae1.state.loc.ReleaseLock(r)
    rae1.state.charge.ReleaseLock(r)
    return res

def fly(r, l1, l2):

    rae1.state.loc.AcquireLock(r)
    rae1.state.charge.AcquireLock(r)

    dist = EE_GETDISTANCE(l1, l2)
    if r != 'UAV':
        gui.Simulate("%s cannot fly\n" %r)
        res = FAILURE
    elif l1 == l2:
        gui.Simulate("%s is already at location %s\n" %(r, l2))
        res = SUCCESS
    elif rae1.state.loc[r] == l1 and rae1.state.charge[r] >= dist:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('fly', start) == False):
			pass
        gui.Simulate("%s has flied from %s to %s\n" %(r, l1, l2))
        rae1.state.loc[r] = l2
        rae1.state.charge[r] = rae1.state.charge[r] - dist
        res = SUCCESS
    elif rae1.state.loc[r] != l1 and rae1.state.charge[r] >= dist:
        gui.Simulate("%s is not in location %s\n" %(r, l1))
        res = FAILURE
    elif rae1.state.loc[r] == l1 and rae1.state.charge[r] < dist:
        gui.Simulate("%s does not have any charge to move :(\n" %r)
        res = FAILURE
    else:
        gui.Simulate("%s is not at location %s and it doesn't have enough charge!\n" %(r, l1))
        res = FAILURE
    rae1.state.loc.ReleaseLock(r)
    rae1.state.charge.ReleaseLock(r)
    return res

def fly_Sim(r, l1, l2):
    print("here")
    rae1.state.loc.AcquireLock(r)
    rae1.state.charge.AcquireLock(r)
    print("crossed")
    dist = EE_GETDISTANCE(l1, l2)
    if r != 'UAV':
        gui.Simulate("%s cannot fly\n" %r)
        res = FAILURE
    elif l1 == l2:
        gui.Simulate("%s is already at location %s\n" %(r, l2))
        res = SUCCESS
    elif rae1.state.loc[r] == l1 and rae1.state.charge[r] >= dist:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('fly', start) == False):
			pass
        gui.Simulate("%s has flied from %s to %s\n" %(r, l1, l2))
        rae1.state.loc[r] = l2
        rae1.state.charge[r] = rae1.state.charge[r] - dist
        res = SUCCESS
    elif rae1.state.loc[r] != l1 and rae1.state.charge[r] >= dist:
        gui.Simulate("%s is not in location %s\n" %(r, l1))
        res = FAILURE
    elif rae1.state.loc[r] == l1 and rae1.state.charge[r] < dist:
        gui.Simulate("%s does not have any charge to move :(\n" %r)
        res = FAILURE
    else:
        gui.Simulate("%s is not at location %s and it doesn't have enough charge!\n" %(r, l1))
        res = FAILURE
    rae1.state.loc.ReleaseLock(r)
    rae1.state.charge.ReleaseLock(r)
    return res

def take(r, o):
    rae1.state.load.AcquireLock(r)
    if rae1.state.load[r] == NIL:
        rae1.state.loc.AcquireLock(r)
        rae1.state.pos.AcquireLock(o)
        if rae1.state.loc[r] == rae1.state.pos[o]:
            start = globalTimer.GetTime()
            while(globalTimer.IsCommandExecutionOver('take', start) == False):
                pass
            gui.Simulate("%s has picked up %s\n" %(r, o))
            rae1.state.pos[o] = r
            rae1.state.load[r] = o
            res = SUCCESS
        else:
            gui.Simulate("%s is not at %s's location\n" %(r, o))
            res = FAILURE
        rae1.state.loc.ReleaseLock(r)
        rae1.state.pos.ReleaseLock(o)
    else:
        gui.Simulate("%s is not free to take anything\n" %r)
        res = FAILURE
    rae1.state.load.ReleaseLock(r)
    return res

def take_Sim(r, o):
    rae1.state.load.AcquireLock(r)
    if rae1.state.load[r] == NIL:
        rae1.state.loc.AcquireLock(r)
        rae1.state.pos.AcquireLock(o)
        if rae1.state.loc[r] == rae1.state.pos[o]:
            start = globalTimer.GetTime()
            while(globalTimer.IsCommandExecutionOver('take', start) == False):
                pass
            gui.Simulate("%s has picked up %s\n" %(r, o))
            rae1.state.pos[o] = r
            rae1.state.load[r] = o
            res = SUCCESS
        else:
            gui.Simulate("%s is not at %s's location\n" %(r, o))
            res = FAILURE
        rae1.state.loc.ReleaseLock(r)
        rae1.state.pos.ReleaseLock(o)
    else:
        gui.Simulate("%s is not free to take anything\n" %r)
        res = FAILURE
    rae1.state.load.ReleaseLock(r)
    return res

def put(r, o):
    rae1.state.loc.AcquireLock(r)
    rae1.state.pos.AcquireLock(o)
    if rae1.state.pos[o] == r:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('put', start) == False):
			pass
        rae1.state.pos[o] = rae1.state.loc[r]
        rae1.state.load[r] = NIL
        gui.Simulate("%s has put %s at location %s\n" %(r,o,rae1.state.loc[r]))
        res = SUCCESS
    else:
        gui.Simulate("%s is not with %s\n" %(o,r))
        res = FAILURE
    rae1.state.loc.ReleaseLock(r)
    rae1.state.pos.ReleaseLock(o)
    return res

def put_Sim(r, o):
    rae1.state.loc.AcquireLock(r)
    rae1.state.pos.AcquireLock(o)
    if rae1.state.pos[o] == r:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('put', start) == False):
			pass
        rae1.state.pos[o] = rae1.state.loc[r]
        rae1.state.load[r] = NIL
        gui.Simulate("%s has put %s at location %s\n" %(r,o,rae1.state.loc[r]))
        res = SUCCESS
    else:
        gui.Simulate("%s is not with %s\n" %(o,r))
        res = FAILURE
    rae1.state.loc.ReleaseLock(r)
    rae1.state.pos.ReleaseLock(o)
    return res

def deposit(r):
    rae1.state.loc.AcquireLock(r)
    rae1.state.data.AcquireLock(r)
    if rae1.state.loc[r] == 'base':
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('deposit', start) == False):
			pass
        gui.Simulate("%s has deposited data in the base\n" %r)
        rae1.state.data[r] = 0
        res = SUCCESS
    else:
        gui.Simulate("%s is not in base, so it cannot deposit data.\n" %r)
        res = FAILURE
    rae1.state.loc.ReleaseLock(r)
    rae1.state.data.ReleaseLock(r)
    return res

def deposit_Sim(r):
    rae1.state.loc.AcquireLock(r)
    rae1.state.data.AcquireLock(r)
    if rae1.state.loc[r] == 'base':
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('deposit', start) == False):
			pass
        gui.Simulate("%s has deposited data in the base\n" %r)
        rae1.state.data[r] = 0
        res = SUCCESS
    else:
        gui.Simulate("%s is not in base, so it cannot deposit data.\n" %r)
        res = FAILURE
    rae1.state.loc.ReleaseLock(r)
    rae1.state.data.ReleaseLock(r)
    return res

def transferData(r1, r2):
    rae1.state.loc.AcquireLock(r1)
    rae1.state.loc.AcquireLock(r2)
    rae1.state.data.AcquireLock(r1)
    rae1.state.data.AcquireLock(r2)

    if rae1.state.loc[r1] != rae1.state.loc[r2]:
        gui.Simulate("%s and %s are not in same location.\n" %(r1, r2))
        res = FAILURE
    elif rae1.state.data[r2] + rae1.state.data[r1] <= 4:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('transferData', start) == False):
			pass
        gui.Simulate("%s transfered data to %s\n" %(r1, r2))
        rae1.state.data[r2] += rae1.state.data[r1]
        rae1.state.data[r1] = 0
        res = SUCCESS
    elif rae1.state.data[r2] < 4:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('transferData', start) == False):
			pass
        t = 4 - rae1.state.data[r2]
        rae1.state.data[r2] = 4
        rae1.state.data[r1] -= t
        gui.Simulate("%s transfered data to %s\n" %(r1, r2))
        res = SUCCESS
    rae1.state.loc.ReleaseLock(r1)
    rae1.state.loc.ReleaseLock(r2)
    rae1.state.data.ReleaseLock(r1)
    rae1.state.data.ReleaseLock(r2)
    return res

def transferData_Sim(r1, r2):
    rae1.state.loc.AcquireLock(r1)
    rae1.state.loc.AcquireLock(r2)
    rae1.state.data.AcquireLock(r1)
    rae1.state.data.AcquireLock(r2)

    if rae1.state.loc[r1] != rae1.state.loc[r2]:
        gui.Simulate("%s and %s are not in same location.\n" %(r1, r2))
        res = FAILURE
    elif rae1.state.data[r2] + rae1.state.data[r1] <= 4:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('transferData', start) == False):
			pass
        gui.Simulate("%s transfered data to %s\n" %(r1, r2))
        rae1.state.data[r2] += rae1.state.data[r1]
        rae1.state.data[r1] = 0
        res = SUCCESS
    elif rae1.state.data[r2] < 4:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('transferData', start) == False):
			pass
        t = 4 - rae1.state.data[r2]
        rae1.state.data[r2] = 4
        rae1.state.data[r1] -= t
        gui.Simulate("%s transfered data to %s\n" %(r1, r2))
        res = SUCCESS
    rae1.state.loc.ReleaseLock(r1)
    rae1.state.loc.ReleaseLock(r2)
    rae1.state.data.ReleaseLock(r1)
    rae1.state.data.ReleaseLock(r2)
    return res

def Explore_Method2(r, activity, l):
    rae1.do_task('getEquipment', r, activity)
    rae1.do_task('moveTo', r, l)
    if activity == 'survey':
        rae1.do_command(survey, r, l)
    elif activity == 'monitor':
        rae1.do_command(monitor, r, l)
    elif activity == 'screen':
        rae1.do_command(screen, r, l)
    elif activity == 'sample':
        rae1.do_command(sample, r, l)
    elif activity == 'process':
        rae1.do_command(process, r, l)
    rae1.do_task('depositData', r)
    return SUCCESS

def Explore_Method1(r, activity, l):
    rae1.do_task('getEquipment', r, activity)
    rae1.do_task('moveTo', r, l)
    if activity == 'survey':
        rae1.do_command(survey, r, l)
    elif activity == 'monitor':
        rae1.do_command(monitor, r, l)
    elif activity == 'screen':
        rae1.do_command(screen, r, l)
    elif activity == 'sample':
        rae1.do_command(sample, r, l)
    elif activity == 'process':
        rae1.do_command(process, r, l)
    return SUCCESS

def GetEquipment_Method1(r, activity):
    if rae1.state.load[r] != rv.EQUIPMENT[activity]:
        rae1.do_task('moveTo', r, rae1.state.pos[rv.EQUIPMENT[activity]])
        rae1.do_command(take, r, rv.EQUIPMENT[activity])
    return SUCCESS

def GetEquipment_Method2(r, activity):
    if rae1.state.load[r] != rv.EQUIPMENT[activity]:
        rae1.do_task('moveTo', r, rae1.state.pos[rv.EQUIPMENT[activity]])
        rae1.state.load.AcquireLock(r)
        if rae1.state.load[r] != NIL:
            x = rae1.state.load[r]
            rae1.state.load.ReleaseLock(r)
            rae1.do_command(put, r, x)
        else:
            rae1.state.load.ReleaseLock(r)
        rae1.do_command(take, r, rv.EQUIPMENT[activity])
    return SUCCESS

def MoveTo_MethodHelper(r, l):
    res = SUCCESS
    path = EE_GETPATH(rae1.state.loc[r], l)
    if path == {}:
        gui.Simulate("%s is already at location %s \n" %(r, l))
    else:
        lTemp = rae1.state.loc[r]
        if lTemp not in path:
            gui.Simulate("%s is out of its path to %s\n" %(r, l))
            res = FAILURE
        else:
            while(lTemp != l):
                lNext = path[lTemp]
                rae1.do_command(move, r, lTemp, lNext)
                if lNext != rae1.state.loc[r]:
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

def MoveTo_Method2(r, l):
    if l not in rv.LOCATIONS:
        gui.Simulate("%s is trying to go to an invalid location\n" %r)
        res = FAILURE
    else:
        dist = EE_GETDISTANCE(rae1.state.loc[r], l)
        if rae1.state.charge[r] >= dist:
            res = MoveTo_MethodHelper(r, l)
        else:
            gui.Simulate("Insufficient charge! only %.2f%%. %s cannot move\n" %(rae1.state.charge[r] * 100 / 75, r))
            res = FAILURE
    return res

def MoveTo_Method3(r, l):
    if l not in rv.LOCATIONS:
        gui.Simulate("%s is trying to go to an invalid location\n" %r)
        res = FAILURE
    else:
        dist = EE_GETDISTANCE(rae1.state.loc[r], l)
        if rae1.state.charge[r] >= dist:
            res = MoveTo_MethodHelper(r, l)
        else:
            rae1.do_task('recharge', r)
            rae1.do_task('moveTo', r, l)
            res = SUCCESS
    return res

def FlyTo_Method1(r, l):
    if r == 'UAV':
        rae1.do_command(fly, r, rae1.state.loc[r], l)
        res = SUCCESS
    else:
        gui.Simulate("%s is not a UAV. So, it cannot fly\n" %r)
        res = FAILURE
    return res

def FlyTo_Method2(r, l):
    dist = EE_GETDISTANCE(rae1.state.loc[r], l)
    if r == 'UAV':
        if rae1.state.charge[r] >= dist:
            rae1.do_command(fly, r, rae1.state.loc[r], l)
            res = SUCCESS
        else:
            gui.Simulate("Insufficient charge! only %.2f%%. %s cannot move\n" %(rae1.state.charge[r] * 100 / 75, r))
            res = FAILURE
    else:
        gui.Simulate("%s is not a UAV. So, it cannot fly\n" %r)
        res = FAILURE
    return res

def FlyTo_Method3(r, l):
    dist = EE_GETDISTANCE(rae1.state.loc[r], l)
    if r == 'UAV':
        if rae1.state.charge[r] >= dist:
            rae1.do_command(fly, r, rae1.state.loc[r], l)
            res = SUCCESS
        else:
            rae1.do_task('recharge', r)
            rae1.do_task('flyTo', r, l)
            res = SUCCESS
    else:
        gui.Simulate("%s is not a UAV. So, it cannot fly\n" %r)
        res = FAILURE
    return res

def DepositData_Method1(r):
    if rae1.state.data[r] > 0:
        rae1.do_task('moveTo', r, 'base')
        rae1.do_command(deposit, r)
    else:
        gui.Simulate("%s has no data to deposit.\n" %r)
    return SUCCESS

def DepositData_Method2(r):
    if rae1.state.data[r] > 0:
        if r != 'UAV':
            rae1.do_task('flyTo', 'UAV', rae1.state.loc[r])
            rae1.do_command(transferData, r, 'UAV')
        rae1.do_task('flyTo', 'UAV', 'base')
        rae1.do_command(deposit, 'UAV')
    else:
        gui.Simulate("%s has no data to deposit.\n" %r)
    return SUCCESS

def Recharge_Method1(r):
    c = 'c1'
    if rae1.state.pos[c] not in rv.LOCATIONS and rae1.state.pos[c] != r:
        gui.Simulate("%s cannot find charger %s\n" %(r, c))
        res = FAILURE
    elif rae1.state.loc[r] != rae1.state.pos[c] and rae1.state.pos[c] != r:
        rae1.do_task('moveTo', r, rae1.state.pos[c])
        rae1.do_command(charge, r, c)
        res = SUCCESS
    else:
        rae1.do_command(charge, r, c)
        res = SUCCESS
    return res

def Recharge_Method2(r):
    c = 'c1'
    if rae1.state.pos[c] not in rv.LOCATIONS and rae1.state.pos[c] != r:
        gui.Simulate("%s cannot find charger %s\n" %(r, c))
        res = FAILURE
    elif rae1.state.loc[r] != rae1.state.pos[c] and rae1.state.pos[c] != r:
        rae1.do_task('moveTo', r, rae1.state.pos[c])
        rae1.do_command(charge, r, c)
        rae1.do_command(take, r, c)
        res = SUCCESS
    else:
        rae1.do_command(charge, r, c)
        rae1.do_command(take, r, c)
        res = SUCCESS
    return res

rv = RV()
rae1.declare_commands([survey, monitor, screen, sample, process, charge, move, put, take, fly, deposit, transferData],
                      [survey_Sim, monitor_Sim, screen_Sim, sample_Sim, process_Sim, charge_Sim, move_Sim, put_Sim, take_Sim, fly_Sim, deposit_Sim, transferData_Sim])
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

