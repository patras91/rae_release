__author__ = 'patras'
import ape
from domain_constants import *
import gui
from timer import globalTimer

'''A simple example where a robot has to fetch an object in a harbor and handle emergencies. From Ch 3'''

def moveTo(r, l):
    ape.state.emergencyHandling.AcquireLock(r)
    if ape.state.emergencyHandling[r] == False:
        ape.state.loc.AcquireLock(r)
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('moveTo', start) == False):
            pass
        gui.Simulate("Robot %s has gone to location %d\n" %(r,l))
        ape.state.loc[r] = l
        ape.state.loc.ReleaseLock(r)
        res = SUCCESS
    else:
        gui.Simulate("Cannot move robot %s because it is handling emergency\n" %r)
        res = FAILURE
    ape.state.emergencyHandling.ReleaseLock(r)
    return res

def moveTo_Sim(r, l):
    ape.state.emergencyHandling.AcquireLock(r)
    if ape.state.emergencyHandling[r] == False:
        ape.state.loc.AcquireLock(r)
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('moveTo', start) == False):
            pass
        gui.Simulate("Robot %s has gone to location %d\n" %(r,l))
        ape.state.loc[r] = l
        ape.state.loc.ReleaseLock(r)
        res = SUCCESS
    else:
        gui.Simulate("Cannot move robot %s because it is handling emergency\n" %r)
        res = FAILURE
    ape.state.emergencyHandling.ReleaseLock(r)
    return res

def moveToEmergency(r, l):
    ape.state.loc.AcquireLock(r)
    start = globalTimer.GetTime()
    while(globalTimer.IsCommandExecutionOver('moveToEmergency', start) == False):
        pass
    gui.Simulate("Robot %s has gone to location %d to handle emergency\n" %(r,l))
    ape.state.loc[r] = l
    ape.state.loc.ReleaseLock(r)
    return SUCCESS

def moveToEmergency_Sim(r, l):
    ape.state.loc.AcquireLock(r)
    start = globalTimer.GetTime()
    while(globalTimer.IsCommandExecutionOver('moveToEmergency', start) == False):
        pass
    gui.Simulate("Robot %s has gone to location %d to handle emergency\n" %(r,l))
    ape.state.loc[r] = l
    ape.state.loc.ReleaseLock(r)
    return SUCCESS

def take(r, o, l):
    ape.state.pos.AcquireLock(o)
    if ape.state.pos[o] == l:
        ape.state.load.AcquireLock(r)
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('take', start) == False):
            pass
        ape.state.pos[o] = r
        ape.state.load[r] = o
        ape.state.load.ReleaseLock(r)
        gui.Simulate("Robot %s has taken object %s at location %d\n" %(r,o,l))
        res = SUCCESS
    else:
        gui.Simulate("Object %s is not at location %d\n" %(o,l))
        res = FAILURE
    ape.state.pos.ReleaseLock(o)
    return res

def take_Sim(r, o, l):
    ape.state.pos.AcquireLock(o)
    if ape.state.pos[o] == l:
        ape.state.load.AcquireLock(r)
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('take', start) == False):
            pass
        ape.state.pos[o] = r
        ape.state.load[r] = o
        ape.state.load.ReleaseLock(r)
        gui.Simulate("Robot %s has taken object %s at location %d\n" %(r,o,l))
        res = SUCCESS
    else:
        gui.Simulate("Object %s is not at location %d\n" %(o,l))
        res = FAILURE
    ape.state.pos.ReleaseLock(o)
    return res

def put(r, o, l):
    ape.state.pos.AcquireLock(o)
    if ape.state.pos[o] == r:
        ape.state.load.AcquireLock(r)
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('put', start) == False):
            pass
        ape.state.pos[o] = l
        ape.state.load[r] = NIL
        ape.state.load.ReleaseLock(r)
        gui.Simulate("Robot %s has put object %s at location %d\n" %(r,o,l))
        res = SUCCESS
    else:
        gui.Simulate("Object %s is not with robot %s\n" %(o,r))
        res = FAILURE
    ape.state.pos.ReleaseLock(o)
    return res

def put_Sim(r, o, l):
    ape.state.pos.AcquireLock(o)
    if ape.state.pos[o] == r:
        ape.state.load.AcquireLock(r)
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('put', start) == False):
            pass
        ape.state.pos[o] = l
        ape.state.load[r] = NIL
        ape.state.load.ReleaseLock(r)
        gui.Simulate("Robot %s has put object %s at location %d\n" %(r,o,l))
        res = SUCCESS
    else:
        gui.Simulate("Object %s is not with robot %s\n" %(o,r))
        res = FAILURE
    ape.state.pos.ReleaseLock(o)
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
    return SUCCESS

def perceive_Sim(l):
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
    return SUCCESS

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

def addressEmergency_Sim(r, l, i):
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

def wait(r):
    while(ape.state.emergencyHandling[r] == True):
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
    ape.state.emergencyHandling.AcquireLock(r)
    ape.state.emergencyHandling[r] = False
    ape.state.emergencyHandling.ReleaseLock(r)

    return SUCCESS

def Search_Method1(r, o):
    if ape.state.pos[o] == UNK:
        for l in rv.LOCATIONS:
            if ape.state.view[l] == False:
                ape.do_task('nonEmergencyMove', r, l)
                ape.do_command(perceive, l)
                if ape.state.pos[o] == l:
                    ape.do_command(take, r, o, l)
                    break
        res = SUCCESS
    else:
        gui.Simulate("Failed to search %s" %o)
        res = FAILURE
    return res

def Fetch_Method1(r, o):
    pos_o = ape.state.pos[o]
    if pos_o == UNK:
        ape.do_task('search', r, o)
    elif ape.state.loc[r] == pos_o:
        ape.do_command(take, r, o, pos_o)
    else:
        ape.do_task('nonEmergencyMove', r, pos_o)
        ape.do_command(take, r, o, pos_o)
    return SUCCESS

def Emergency_Method1(r, l, i):
    if ape.state.emergencyHandling[r] == False:
        ape.state.emergencyHandling[r] = True
        load_r = ape.state.load[r]
        if load_r != NIL:
            ape.do_command(put, r, load_r, ape.state.loc[r])
        ape.do_command(moveToEmergency, r, l)
        ape.do_command(addressEmergency, r, l, i)
        res = SUCCESS
    else:
        gui.Simulate("%r is already busy handling another emergency\n" %r)
        res = FAILURE
    return res

def NonEmergencyMove_Method1(r, l):
    if ape.state.emergencyHandling[r] == False:
        ape.do_command(moveTo, r, l)
        res = SUCCESS
    else:
        gui.Simulate("Move failed, trying to do a non emergency move for a robot handling emergency\n")
        res = FAILURE
    return res

def NonEmergencyMove_Method2(r, l):
    if ape.state.emergencyHandling[r] == False:
        ape.do_command(moveTo, r, l)
    else:
        ape.do_command(wait, r)
        ape.do_command(moveTo, r, l)
    return SUCCESS

rv = RV()
ape.declare_commands([moveTo, take, perceive, addressEmergency, moveToEmergency, wait],
                      [moveTo_Sim, take_Sim, perceive_Sim, addressEmergency_Sim, moveToEmergency_Sim, wait_Sim])

ape.declare_methods('search', Search_Method1)
ape.declare_methods('fetch', Fetch_Method1)
ape.declare_methods('emergency', Emergency_Method1)
ape.declare_methods('nonEmergencyMove', NonEmergencyMove_Method1, NonEmergencyMove_Method2)
