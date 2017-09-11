__author__ = 'patras'

import rae1
import gui
from domain_constants import *
from timer import globalTimer

# Using Dijsktra's algorithm
def IP_GETDISTANCE(l0, l1):
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

# Using Dijsktra's algorithm
def IP_GETPATH(l0, l1):
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

def GetNewName():
    GetNewName.current += 1
    return 'TMPOBJECT' + GetNewName.current.__str__()

GetNewName.current = 0

def paint(o, colour, name):
    rae1.state.pos.AcquireLock(o)
    if rae1.state.pos[o] == rv.MACHINE_LOCATION['paint']:
        rae1.state.status.AcquireLock('paint')
        gui.Simulate("Colouring %s with colour %s and naming it %s\n" %(o, colour, name))
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('paint', start) == False):
		    pass
        rae1.state.pos[name] = rv.MACHINE_LOCATION['paint']
        rae1.state.status.ReleaseLock('paint')
        res = SUCCESS
    else:
        gui.Simulate("%s is not in painting machine's location\n" %o)
        res = FAILURE
    rae1.state.pos.ReleaseLock(o)
    return res

def assemble(p1, p2, name):
    rae1.state.pos.AcquireLock(p1)
    rae1.state.pos.AcquireLock(p2)

    if rae1.state.pos[p1] == rv.MACHINE_LOCATION['assemble'] and rae1.state.pos[p2] == rv.MACHINE_LOCATION['assemble']:
        rae1.state.status.AcquireLock('assemble')
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('assemble', start) == False):
		    pass
        gui.Simulate("Assembled parts %s and %s and naming it %s\n" %(p1, p2, name))
        rae1.state.pos[name] = rv.MACHINE_LOCATION['assemble']
        rae1.state.status.ReleaseLock('assemble')
        res = SUCCESS
    else:
        gui.Simulate("Part %s or %s is not in painting machine's location\n" %(p1, p2))
        res = FAILURE
    rae1.state.pos.ReleaseLock(p1)
    rae1.state.pos.ReleaseLock(p2)
    return res

def pack(o1, o2, name):
    rae1.state.pos.AcquireLock(o1)
    rae1.state.pos.AcquireLock(o2)
    if rae1.state.pos[o1] == rv.MACHINE_LOCATION['pack'] and rae1.state.pos[o2] == rv.MACHINE_LOCATION['pack']:
        rae1.state.status.AcquireLock('pack')
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('pack', start) == False):
		    pass
        gui.Simulate("Packed objects %s and %s and naming it %s\n" %(o1, o2, name))
        rae1.state.pos[name] = rv.MACHINE_LOCATION['pack']
        rae1.state.status.ReleaseLock('pack')
        res = SUCCESS
    else:
        gui.Simulate("Part %s or %s is not in packing machine's location\n" %(o1, o2))
        res = FAILURE
    rae1.state.pos.ReleaseLock(o1)
    rae1.state.pos.ReleaseLock(o2)
    return res

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

def move(r, loc1, loc2):
    rae1.state.loc.AcquireLock(r)
    if rae1.state.loc[r] == loc1:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('move', start) == False):
		    pass
        rae1.state.loc[r] = loc2
        gui.Simulate("%s has moved from %s to %s\n" %(r, loc1, loc2))
        res = SUCCESS
    else:
        gui.Simulate("%s is not in location %s\n" %(r, loc1))
        res = FAILURE
    rae1.state.loc.ReleaseLock(r)
    return res

def Delegate(args, o_name):
    taskName = args[0]
    param1 = args[1]
    param2 = args[2]
    if len(param1) == 1:
        param1 = param1[0]
    if len(param2) == 1:
        param2 = param2[0]
    rae1.do_task(taskName, param1, param2, o_name)

def Paint_Method1(o, colour, name):
    if isinstance(o, list):
        o_name = GetNewName()
        Delegate(o, o_name)
    else:
        o_name = o

    if o_name not in rae1.state.pos or rae1.state.pos[o_name] != rv.MACHINE_LOCATION['paint']:
        rae1.do_task('deliver', o_name, rv.MACHINE_LOCATION['paint'])
    rae1.do_command(paint, o_name, colour, name)
    return SUCCESS

def Assemble_Method1(part1, part2, name):
    if isinstance(part1, list):
        o_name1 = GetNewName()
        Delegate(part1, o_name1)
    else:
        o_name1 = part1

    if isinstance(part2, list):
        o_name2 = GetNewName()
        Delegate(part2, o_name2)
    else:
        o_name2 = part2

    if o_name1 not in rae1.state.pos or rae1.state.pos[o_name1] != rv.MACHINE_LOCATION['assemble']:
        rae1.do_task('deliver', o_name1, rv.MACHINE_LOCATION['assemble'])
    if o_name2 not in rae1.state.pos or rae1.state.pos[o_name2] != rv.MACHINE_LOCATION['assemble']:
        rae1.do_task('deliver', o_name2, rv.MACHINE_LOCATION['assemble'])
    rae1.do_command(assemble, o_name1, o_name2, name)
    return SUCCESS

def Pack_Method1(o1, o2, name):
    if isinstance(o1, list):
        o_name1 = GetNewName()
        Delegate(o1, o_name1)
    else:
        o_name1 = o1

    if isinstance(o2, list):
        o_name2 = GetNewName()
        Delegate(o2, o_name2)
    else:
        o_name2 = o2
    if o_name1 not in rae1.state.pos or rae1.state.pos[o_name1] != rv.MACHINE_LOCATION['pack']:
        rae1.do_task('deliver', o_name1, rv.MACHINE_LOCATION['pack'])
    if o_name2 not in rae1.state.pos or rae1.state.pos[o_name2] != rv.MACHINE_LOCATION['pack']:
        rae1.do_task('deliver', o_name2, rv.MACHINE_LOCATION['pack'])
    rae1.do_command(pack, o_name1, o_name2, name)
    return SUCCESS

def Order_Method1(taskArgs):
    taskName = taskArgs[0]
    taskArg1 = taskArgs[1]
    taskArg2 = taskArgs[2]
    name = GetNewName()
    rae1.do_task(taskName, taskArg1, taskArg2, name)
    rae1.do_task('deliver', name, rv.MACHINE_LOCATION['output'])
    return SUCCESS

def Deliver_Method1(o, l):
    if o not in rae1.state.pos:
        rae1.state.pos[o] = 1
    loc_o = rae1.state.pos[o]
    deliveryRobot = NIL
    while(deliveryRobot == NIL):
        for r in rv.ROBOTS:
            rae1.state.status.AcquireLock(r)
            if rae1.state.status[r] == 'free':
                deliveryRobot = r
                rae1.state.status[r] = 'busy'
                rae1.state.status.ReleaseLock(r)
                break
            rae1.state.status.ReleaseLock(r)
    if rae1.state.loc[deliveryRobot] != loc_o:
        rae1.do_command(move, deliveryRobot, rae1.state.loc[deliveryRobot], loc_o)
    rae1.do_command(take, deliveryRobot, o, loc_o)
    if rae1.state.loc[deliveryRobot] != l:
        rae1.do_command(move, deliveryRobot, rae1.state.loc[deliveryRobot], l)
    rae1.do_command(put, deliveryRobot, o, l)

    rae1.state.status.AcquireLock(deliveryRobot)
    rae1.state.status[deliveryRobot] = 'free'
    rae1.state.status.ReleaseLock(deliveryRobot)
    return SUCCESS

rv = RV()
rae1.declare_commands(paint, assemble, pack, take, put)
print('\n')
rae1.print_commands()

rae1.declare_methods('paint', Paint_Method1)
rae1.declare_methods('assemble', Assemble_Method1)
rae1.declare_methods('pack', Pack_Method1)
rae1.declare_methods('deliver', Deliver_Method1)
rae1.declare_methods('order', Order_Method1)

print('\n')
rae1.print_methods()

print('\n*********************************************************')
print("* Call rae1 on industry plant domain.")
print("* For a different amout of printout,  try verbosity(0), verbosity(1), or verbosity(2).")
print("* For a different mode, try SetMode(\'Clock\') or SetMode(\'Counter\').")
print('*********************************************************\n')