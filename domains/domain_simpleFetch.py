__author__ = 'patras'
import rae1
from domain_constants import *
import gui
from timer import globalTimer

'''A simple example where a robot has to fetch an object in a harbor and handle emergencies. From Ch 3'''

def moveTo(r, l):
    rae1.state.emergencyHandling.AcquireLock(r)
    if rae1.state.emergencyHandling[r] == False:
        rae1.state.loc.AcquireLock(r)
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('moveTo', start) == False):
            pass
        gui.Simulate("Robot %s has gone to location %d\n" %(r,l))
        rae1.state.loc[r] = l
        rae1.state.loc.ReleaseLock(r)
        res = SUCCESS
    else:
        gui.Simulate("Cannot move robot %s because it is handling emergency\n" %r)
        res = FAILURE
    rae1.state.emergencyHandling.ReleaseLock(r)
    return res

def moveTo_Sim(r, l):
    rae1.state.emergencyHandling.AcquireLock(r)
    if rae1.state.emergencyHandling[r] == False:
        rae1.state.loc.AcquireLock(r)
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('moveTo', start) == False):
            pass
        gui.Simulate("Robot %s has gone to location %d\n" %(r,l))
        rae1.state.loc[r] = l
        rae1.state.loc.ReleaseLock(r)
        res = SUCCESS
    else:
        gui.Simulate("Cannot move robot %s because it is handling emergency\n" %r)
        res = FAILURE
    rae1.state.emergencyHandling.ReleaseLock(r)
    return res

def moveToEmergency(r, l):
    rae1.state.loc.AcquireLock(r)
    start = globalTimer.GetTime()
    while(globalTimer.IsCommandExecutionOver('moveToEmergency', start) == False):
        pass
    gui.Simulate("Robot %s has gone to location %d to handle emergency\n" %(r,l))
    rae1.state.loc[r] = l
    rae1.state.loc.ReleaseLock(r)
    return SUCCESS

def moveToEmergency_Sim(r, l):
    rae1.state.loc.AcquireLock(r)
    start = globalTimer.GetTime()
    while(globalTimer.IsCommandExecutionOver('moveToEmergency', start) == False):
        pass
    gui.Simulate("Robot %s has gone to location %d to handle emergency\n" %(r,l))
    rae1.state.loc[r] = l
    rae1.state.loc.ReleaseLock(r)
    return SUCCESS

def take(r, o, l):
    rae1.state.pos.AcquireLock(o)
    if rae1.state.pos[o] == l:
        rae1.state.load.AcquireLock(r)
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('take', start) == False):
            pass
        rae1.state.pos[o] = r
        rae1.state.load[r] = o
        rae1.state.load.ReleaseLock(r)
        gui.Simulate("Robot %s has taken object %s at location %d\n" %(r,o,l))
        res = SUCCESS
    else:
        gui.Simulate("Object %s is not at location %d\n" %(o,l))
        res = FAILURE
    rae1.state.pos.ReleaseLock(o)
    return res

def take_Sim(r, o, l):
    rae1.state.pos.AcquireLock(o)
    if rae1.state.pos[o] == l:
        rae1.state.load.AcquireLock(r)
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('take', start) == False):
            pass
        rae1.state.pos[o] = r
        rae1.state.load[r] = o
        rae1.state.load.ReleaseLock(r)
        gui.Simulate("Robot %s has taken object %s at location %d\n" %(r,o,l))
        res = SUCCESS
    else:
        gui.Simulate("Object %s is not at location %d\n" %(o,l))
        res = FAILURE
    rae1.state.pos.ReleaseLock(o)
    return res

def put(r, o, l):
    rae1.state.pos.AcquireLock(o)
    if rae1.state.pos[o] == r:
        rae1.state.load.AcquireLock(r)
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('put', start) == False):
            pass
        rae1.state.pos[o] = l
        rae1.state.load[r] = NIL
        rae1.state.load.ReleaseLock(r)
        gui.Simulate("Robot %s has put object %s at location %d\n" %(r,o,l))
        res = SUCCESS
    else:
        gui.Simulate("Object %s is not with robot %s\n" %(o,r))
        res = FAILURE
    rae1.state.pos.ReleaseLock(o)
    return res

def put_Sim(r, o, l):
    rae1.state.pos.AcquireLock(o)
    if rae1.state.pos[o] == r:
        rae1.state.load.AcquireLock(r)
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('put', start) == False):
            pass
        rae1.state.pos[o] = l
        rae1.state.load[r] = NIL
        rae1.state.load.ReleaseLock(r)
        gui.Simulate("Robot %s has put object %s at location %d\n" %(r,o,l))
        res = SUCCESS
    else:
        gui.Simulate("Object %s is not with robot %s\n" %(o,r))
        res = FAILURE
    rae1.state.pos.ReleaseLock(o)
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

def Search_Method1(r, o):
    if rae1.state.pos[o] == UNK:
        for l in rv.LOCATIONS:
            if rae1.state.view[l] == False:
                rae1.do_task('nonEmergencyMove', r, l)
                rae1.do_command(perceive, l)
                if rae1.state.pos[o] == l:
                    rae1.do_command(take, r, o, l)
                    break
        res = SUCCESS
    else:
        gui.Simulate("Failed to search %s" %o)
        res = FAILURE
    return res

def Fetch_Method1(r, o):
    pos_o = rae1.state.pos[o]
    if pos_o == UNK:
        rae1.do_task('search', r, o)
    elif rae1.state.loc[r] == pos_o:
        rae1.do_command(take, r, o, pos_o)
    else:
        rae1.do_task('nonEmergencyMove', r, pos_o)
        rae1.do_command(take, r, o, pos_o)
    return SUCCESS

def Emergency_Method1(r, l, i):
    if rae1.state.emergencyHandling[r] == False:
        rae1.state.emergencyHandling[r] = True
        load_r = rae1.state.load[r]
        if load_r != NIL:
            rae1.do_command(put, r, load_r, rae1.state.loc[r])
        rae1.do_command(moveToEmergency, r, l)
        rae1.do_command(addressEmergency, r, l, i)
        res = SUCCESS
    else:
        gui.Simulate("%r is already busy handling another emergency\n" %r)
        res = FAILURE
    return res

def NonEmergencyMove_Method1(r, l):
    if rae1.state.emergencyHandling[r] == False:
        rae1.do_command(moveTo, r, l)
        res = SUCCESS
    else:
        gui.Simulate("Move failed, trying to do a non emergency move for a robot handling emergency\n")
        res = FAILURE
    return res

def NonEmergencyMove_Method2(r, l):
    if rae1.state.emergencyHandling[r] == False:
        rae1.do_command(moveTo, r, l)
    else:
        rae1.do_command(wait, r)
        rae1.do_command(moveTo, r, l)
    return SUCCESS

rv = RV()
rae1.declare_commands([moveTo, take, perceive, addressEmergency, moveToEmergency, wait],
                      [moveTo_Sim, take_Sim, perceive_Sim, addressEmergency_Sim, moveToEmergency_Sim, wait_Sim])

rae1.declare_methods('search', Search_Method1)
rae1.declare_methods('fetch', Fetch_Method1)
rae1.declare_methods('emergency', Emergency_Method1)
rae1.declare_methods('nonEmergencyMove', NonEmergencyMove_Method1, NonEmergencyMove_Method2)
