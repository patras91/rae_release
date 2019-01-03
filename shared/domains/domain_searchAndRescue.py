__author__ = 'patras'

''' Search and Rescue domain:
    There are some natural disasters happening in an area.
    Robots with the help of human experts do search and rescue operations in this area. 
'''

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
import math
import globals

def fail():
    return FAILURE

def moveEuclidean(r, l1, l2, dist):
    (x1, y1) = l1
    (x2, y2) = l2
    xlow = min(x1, x2)
    xhigh = max(x1, x2)
    ylow = min(y1, y2)
    yhigh = max(y1, y2)
    for o in rv.OBSTACLES:    
        (ox, oy) = o
        if ox >= xlow and ox <= xhigh and oy >= ylow and oy <= yhigh:
            if abs((oy - y1)/(ox - x1) - (y2 - y1)/(x2 - x1)) <= 0.0001:
                gui.Simulate("%s cannot move in euclidean path because of obstacle\n" %r)
                return FAILURE

    state.loc.AcquireLock(r)
    if l1 == l2:
        gui.Simulate("Robot %s is already at location %s\n" %(r, l2))
        res = SUCCESS
    elif state.loc[r] == l1:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('move', start) == False):
           pass
        res = Sense('moveEuclidean')
        if res == SUCCESS:
            gui.Simulate("Robot %s has moved from %s to %s\n" %(r, str(l1), str(l2)))
            state.loc[r] = l2
        else:
            gui.Simulate("Robot %s failed to move due to some internal failure.\n" %r)
    else:
        gui.Simulate("Robot %s is not in location %d.\n" %(r, l1))
        res = FAILURE
    state.loc.ReleaseLock(r)
    return res

def moveCurved(r, l1, l2, dist):
    (x1, y1) = l1
    (x2, y2) = l2
    centrex = (x1 + x2)/2
    centrey = (y1 + y2)/2
    for o in rv.OBSTACLES:
        (ox, oy) = o
        r2 = (x2 - centrex)*(x2 - centrex) + (y2 - centrey)*(y2 - centrey)
        ro = (ox - centrex)*(ox - centrex) + (oy - centrey)*(oy - centrey)  
        if abs(r2 - ro) <= 0.0001:
            gui.Simulate("%s cannot move in curved path because of obstacle\n" %r)
            return FAILURE
    
    state.loc.AcquireLock(r)
    if l1 == l2:
        gui.Simulate("Robot %s is already at location %s\n" %(r, l2))
        res = SUCCESS
    elif state.loc[r] == l1:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('move', start) == False):
           pass
        res = Sense('moveCurved')
        if res == SUCCESS:
            gui.Simulate("Robot %s has moved from %s to %s\n" %(r, str(l1), str(l2)))
            state.loc[r] = l2
        else:
            gui.Simulate("Robot %s failed to move due to some internal failure.\n" %r)
    else:
        gui.Simulate("Robot %s is not in location %d.\n" %(r, l1))
        res = FAILURE
    state.loc.ReleaseLock(r)
    return res

def moveManhattan(r, l1, l2, dist):
    (x1, y1) = l1
    (x2, y2) = l2
    xlow = min(x1, x2)
    xhigh = max(x1, x2)
    ylow = min(y1, y2)
    yhigh = max(y1, y2)
    for o in rv.OBSTACLES:
        (ox, oy) = o
        if abs(oy - y1) <= 0.0001 and ox >= xlow and ox <= xhigh:
            gui.Simulate("%s cannot move in Manhattan path because of obstacle\n" %r)
            return FAILURE

        if abs(ox - x2) <= 0.0001 and oy >= ylow and oy <= yhigh:
            gui.Simulate("%s cannot move in Manhattan path because of obstacle\n" %r)
            return FAILURE

    state.loc.AcquireLock(r)
    if l1 == l2:
        gui.Simulate("Robot %s is already at location %s\n" %(r, l2))
        res = SUCCESS
    elif state.loc[r] == l1:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('move', start) == False):
           pass
        res = Sense('moveManhattan')
        if res == SUCCESS:
            gui.Simulate("Robot %s has moved from %s to %s\n" %(r, str(l1), str(l2)))
            state.loc[r] = l2
        else:
            gui.Simulate("Robot %s failed to move due to some internal failure.\n" %r)
    else:
        gui.Simulate("Robot %s is not in location %d.\n" %(r, l1))
        res = FAILURE
    state.loc.ReleaseLock(r)
    return res

def fly(r, l1, l2):
    state.loc.AcquireLock(r)
    if l1 == l2:
        gui.Simulate("Robot %s is already at location %s\n" %(r, l2))
        res = SUCCESS
    elif state.loc[r] == l1:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('fly', start) == False):
           pass
        res = Sense('fly')
        if res == SUCCESS:
            gui.Simulate("Robot %s has flied from %s to %s\n" %(r, str(l1), str(l2)))
            state.loc[r] = l2
        else:
            gui.Simulate("Robot %s failed to fly due to some internal failure.\n" %r)
    else:
        gui.Simulate("Robot %s is not in location %d.\n" %(r, l1))
        res = FAILURE
    state.loc.ReleaseLock(r)
    return res

def inspectPerson(r, p):
    gui.Simulate("Robot %s is inspecting person %s \n" %(r, p))
    state.status[p] = state.realStatus[p]
    return SUCCESS

def giveSupportToPerson(r, p):
    gui.Simulate("Robot %s is giving support to person %s \n" %(r, p))
    return SUCCESS

def inspectLocation(r, l):
    gui.Simulate("Robot %s is inspecting location %s \n" %(r, str(l)))
    state.status[l] = state.realStatus[l]
    return SUCCESS

def clearLocation(r, l):
    gui.Simulate("Robot %s has cleared location %s \n" %(r, str(l)))
    return SUCCESS

def SR_GETDISTANCE_Euclidean(l0, l1):
    (x0, y0) = l0
    (x1, y1) = l1
    return math.sqrt((x1 - x0)*(x1 - x0) + (y1 - y0)*(y1-y0))

def MoveTo_Method1(r, l): # takes the straight path
    x = state.loc[r]
    if state.robotType[r] == 'wheeled':
        dist = SR_GETDISTANCE_Euclidean(x, l)
        gui.Simulate("Euclidean distance = %d " %dist)
        ape.do_command(moveEuclidean, r, x, l, dist)
    else:
        ape.do_command(fail)

def SR_GETDISTANCE_Manhattan(l0, l1):
    (x1, y1) = l0
    (x2, y2) = l1
    return abs(x2 - x1) + abs(y2 - y1)

def MoveTo_Method2(r, l): # takes a Manhattan path
    x = state.loc[r]
    if state.robotType[r] == 'wheeled':
        dist = SR_GETDISTANCE_Manhattan(x, l)
        gui.Simulate("Manhattan distance = %d " %dist)
        ape.do_command(moveManhattan, r, x, l, dist) 
    else:
        ape.do_command(fail)

def SR_GETDISTANCE_Curved(l0, l1):
    diameter = SR_GETDISTANCE_Euclidean(l0, l1)
    return math.pi * diameter / 2

def MoveTo_Method3(r, l): # takes a curved path
    x = state.loc[r]
    if state.robotType[r] == 'wheeled':
        dist = SR_GETDISTANCE_Curved(x, l)
        gui.Simulate("Curved distance = %d " %dist)
        ape.do_command(moveCurved, r, x, l, dist) 
    else:
        ape.do_command(fail)

def MoveTo_Method4(r, l):
    x = state.loc[r]
    if state.robotType[r] == 'uav':
        ape.do_command(fly, r, x, l)
    else:
        ape.do_command(fail)

def Rescue_Method1(r, p):
    ape.do_task('moveTo', r, state.loc[p])
    ape.do_task('helpPerson', r, p)

def HelpPerson_Method1(r, p):
    ape.do_command(inspectPerson, r, p)
    if state.status[p] == 'injured':
        ape.do_command(giveSupportToPerson, r, p)
    else:
        ape.do_command(fail)

def HelpPerson_Method2(r, p):
    ape.do_command(inspectLocation, r, state.loc[r])
    if state.status[state.loc[r]] == 'hasDebri':
        ape.do_command(clearLocation, r, state.loc[r]) 
    else:
        ape.do_command(fail)

rv = RV()
ape.declare_commands([
    moveEuclidean,
    moveCurved,
    moveManhattan,
    fly,
    giveSupportToPerson,
    clearLocation,
    inspectLocation,
    inspectPerson,
    fail
    ])

ape.declare_methods('moveTo', 
    MoveTo_Method4,
    MoveTo_Method3, 
    MoveTo_Method2, 
    MoveTo_Method1,
    )

ape.declare_methods('rescue',
    Rescue_Method1,
    )

ape.declare_methods('helpPerson',
    HelpPerson_Method1, 
    HelpPerson_Method2
    )

from env_searchAndRescue import *