__author__ = 'patras'
import rae1
from domain_constants import *

'''A simple example where a robot has to fetch an object in a harbor and handle emergencies. From Ch 3'''

def moveTo(r, l, state):
    print("Robot %s has gone to location %d\n" %(r,l))
    state.loc[r] = l
    return SUCCESS

def take(r, o, l, state):
    if state.pos[o] == l:
        state.pos[o] = r
        state.load[r] = o
        print("Robot %s has taken object %s at location %d\n" %(r,o,l))
        res = SUCCESS
    else:
        print("Object %s is not at location %d\n" %(o,l))
        res = FAILURE
    return res

def put(r, o, l, state):
    if state.pos[o] == r:
        state.pos[o] = l
        state.load[r] = NIL
        print("Robot %s has put object %s at location %d\n" %(r,o,l))
        res = SUCCESS
    else:
        print("Object %s is not with robot %s\n" %(o,r))
        res = FAILURE
    return res

def perceive(l, state):
    if state.view[l] == False:
        for c in state.containers[l]:
            state.pos[c] = l
        state.view[l] = True
        print("Perceived location %d" %l)
    else:
        print("Already perceived\n")
    return SUCCESS

def addressEmergency(r, l, i, state):
    if state.loc[r] == l:
        print("Robot %s has addressed emergency %d" %(r, i))
        res = SUCCESS
    else:
        print("Robot %s has failed to address emergency %d" %(r, i))
        res = FAILURE
    return res

def Search_Method1(r, o, state, ipcArgs, stackid):
    if state.pos[o] == UNK:
        for l in LOCATIONS:
            if state.view[l] == False:
                rae1.do_command(moveTo, r, l, state, ipcArgs, stackid)
                rae1.do_command(perceive, l, state, ipcArgs, stackid)
                if state.pos[o] == l:
                    rae1.do_command(take, r, o, l, state, ipcArgs, stackid)
                    break
        res = SUCCESS
    else:
        print("Failed to search %s" %o)
        res = FAILURE
    return res

def Fetch_Method1(r, o, state, ipcArgs, stackid):
    if state.pos[o] == UNK:
        rae1.do_task('search', r, o, state, ipcArgs, stackid)
    elif state.loc[r] == state.pos[o]:
        rae1.do_command(take, r, o, state.pos[o], state, ipcArgs, stackid)
    else:
        rae1.do_command(moveTo, r, state.pos[o], state, ipcArgs, stackid)
        rae1.do_command(take, r, o, state.pos[o], state, ipcArgs, stackid)
    return SUCCESS

def Emergency_Method1(r, l, i, state, ipcArgs, stackid):
    if state.emergencyHandling[r] == False:
        state.emergencyHandling[r] = True
        if state.load[r] != NIL:
            rae1.do_command(put, r, state.load[r], state.loc[r], state, ipcArgs, stackid)
            rae1.do_command(moveTo, r, l, state, ipcArgs, stackid)
            rae1.do_command(addressEmergency, r, l, i, state, ipcArgs, stackid)
            res = SUCCESS
    else:
        print("%r is already busy handling another emergency\n" %r)
        res = FAILURE
    return res

def simpleFetch_run_1(ipcArgs, stackid):
    state = rae1.State()
    state.loc = {'r1' : 1}
    state.pos = {'o1' : UNK}
    state.load = {'r1' : NIL}
    state.view = {}
    state.containers = {1:[], 2:[], 3:[], 4:[], 5:['o1'], 6:[]}

    for l in LOCATIONS:
        state.view[l] = False
    state.emergencyHandling = {'r1' : False}

    rae1.do_task('fetch', 'r1', 'o1', state, ipcArgs, stackid)
    rae1.do_task('emergency', 'r1', 2, 1, state, ipcArgs, stackid)
    rae1.do_task('fetch', 'r1', 'o1', state, ipcArgs, stackid)

def simpleFetch_init():

	rae1.declare_commands(moveTo, take, perceive, addressEmergency)
	print('\n')
	rae1.print_commands()

	rae1.declare_methods('search', Search_Method1)
	rae1.declare_methods('fetch', Fetch_Method1)
	rae1.declare_methods('emergency', Emergency_Method1)
	print('\n')
	rae1.print_methods()

	print('\n*********************************************************')
	print("* Call rae1 on simple fetch using verbosity level 1.")
	print("* For a different amout of printout, try 0 or 2 instead.")
	print('*********************************************************\n')

	rae1.verbosity(1)