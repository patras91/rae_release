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

def moveToEmergency(r, l):
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

def wait(r):
    start = globalTimer.GetTime()
    while(globalTimer.IsCommandExecutionOver('wait', start) == False):
	    pass
    gui.Simulate("Robot %s is waiting for emergency to be over\n" %r)
    return SUCCESS

def Search_Method1(r, o, stackid):
    if rae1.state.pos[o] == UNK:
        for l in LOCATIONS:
            if rae1.state.view[l] == False:
                rae1.do_task('nonEmergencyMove', r, l, stackid)
                rae1.do_command(perceive, l, stackid)
                if rae1.state.pos[o] == l:
                    rae1.do_command(take, r, o, l, stackid)
                    break
        res = SUCCESS
    else:
        gui.Simulate("Failed to search %s" %o)
        res = FAILURE
    return res

def Fetch_Method1(r, o, stackid):
    pos_o = rae1.state.pos[o]
    if pos_o == UNK:
        rae1.do_task('search', r, o, stackid)
    elif rae1.state.loc[r] == pos_o:
        rae1.do_command(take, r, o, pos_o, stackid)
    else:
        rae1.do_task('nonEmergencyMove', r, pos_o, stackid)
        rae1.do_command(take, r, o, pos_o, stackid)
    return SUCCESS

def Emergency_Method1(r, l, i, stackid):
    if rae1.state.emergencyHandling[r] == False:
        rae1.state.emergencyHandling[r] = True
        load_r = rae1.state.load[r]
        if load_r != NIL:
            rae1.do_command(put, r, load_r, rae1.state.loc[r], stackid)
        rae1.do_command(moveToEmergency, r, l, stackid)
        rae1.do_command(addressEmergency, r, l, i, stackid)
        res = SUCCESS
    else:
        gui.Simulate("%r is already busy handling another emergency\n" %r)
        res = FAILURE
    return res

def NonEmergencyMove_Method1(r, l, stackid):
    if rae1.state.emergencyHandling[r] == False:
        rae1.do_command(moveTo, r, l, stackid)
        res = SUCCESS
    else:
        gui.Simulate("Move failed, trying to do a non emergency move for a robot handling emergency\n")
        res = FAILURE
    return res

def NonEmergencyMove_Method2(r, l, stackid):
    if rae1.state.emergencyHandling[r] == False:
        rae1.do_command(moveTo, r, l, stackid)
    else:
        while(rae1.state.emergencyHandling[r] == True):
            rae1.do_command(wait, r, stackid)
        rae1.do_command(moveTo, r, l, stackid)
    return SUCCESS

def simpleFetch_init():

    rae1.declare_commands(moveTo, take, perceive, addressEmergency, moveToEmergency, wait)
    print('\n')
    rae1.print_commands()

    rae1.declare_methods('search', Search_Method1)
    rae1.declare_methods('fetch', Fetch_Method1)
    rae1.declare_methods('emergency', Emergency_Method1)
    rae1.declare_methods('nonEmergencyMove', NonEmergencyMove_Method1, NonEmergencyMove_Method2)
    print('\n')
    rae1.print_methods()

    print('\n*********************************************************')
    print("* Call rae1 on simple fetch domain.")
    print("* For a different amout of printout, try verbosity(0), verbosity(1), or verbosity(2).")
    print('*********************************************************\n')

    rae1.state.loc = {'r1' : 1}
    rae1.state.pos = {'o1' : UNK, 'o2': UNK}
    rae1.state.load = {'r1' : NIL}
    rae1.state.view = {}
    rae1.state.containers = {1:[], 2:['o2'], 3:[], 4:[], 5:[], 6:['o1']}

    for l in LOCATIONS:
        rae1.state.view[l] = False
    rae1.state.emergencyHandling = {'r1' : False}