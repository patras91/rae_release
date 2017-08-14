__author__ = 'patras'

import rae1
import gui
from domain_constants import *
from timer import globalTimer

def paint(o, colour, name):
    rae1.state.pos.AcquireLock(o)
    if rae1.state.pos[o] == IP_MACHINE_LOCATION['paint']:
        rae1.state.status.AcquireLock('paint')
        gui.Simulate("Colouring %s with colour %s and naming it %s\n" %(o, colour, name))
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('paint', start) == False):
		    pass
        rae1.state.pos[name] = IP_MACHINE_LOCATION['paint']
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

    if rae1.state.pos[p1] == IP_MACHINE_LOCATION['assemble'] and rae1.state.pos[p2] == IP_MACHINE_LOCATION['assemble']:
        rae1.state.status.AcquireLock('assemble')
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('assemble', start) == False):
		    pass
        gui.Simulate("Assembled parts %s and %s and naming it %s\n" %(p1, p2, name))
        rae1.state.pos[name] = IP_MACHINE_LOCATION['assemble']
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
    if rae1.state.pos[o1] == IP_MACHINE_LOCATION['pack'] and rae1.state.pos[o2] == IP_MACHINE_LOCATION['pack']:
        rae1.state.status.AcquireLock('pack')
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('pack', start) == False):
		    pass
        gui.Simulate("Packed objects %s and %s and naming it %s\n" %(o1, o2, name))
        rae1.state.pos[name] = IP_MACHINE_LOCATION['pack']
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

def Delegate(args, o_name, stackid):
    taskName = args[0]
    param1 = args[1]
    param2 = args[2]
    if len(param1) == 1:
        param1 = param1[0]
    if len(param2) == 1:
        param2 = param2[0]
    rae1.do_task(taskName, param1, param2, o_name, stackid)

def Paint_Method1(o, colour, name, stackid):
    if isinstance(o, list):
        o_name = GetNewName()
        Delegate(o, o_name, stackid)
    else:
        o_name = o

    if o_name not in rae1.state.pos or rae1.state.pos[o_name] != IP_MACHINE_LOCATION['paint']:
        rae1.do_task('deliver', o_name, IP_MACHINE_LOCATION['paint'], stackid)
    rae1.do_command(paint, o_name, colour, name, stackid)
    return SUCCESS

def Assemble_Method1(part1, part2, name, stackid):
    if isinstance(part1, list):
        o_name1 = GetNewName()
        Delegate(part1, o_name1, stackid)
    else:
        o_name1 = part1

    if isinstance(part2, list):
        o_name2 = GetNewName()
        Delegate(part2, o_name2, stackid)
    else:
        o_name2 = part2

    if o_name1 not in rae1.state.pos or rae1.state.pos[o_name1] != IP_MACHINE_LOCATION['assemble']:
        rae1.do_task('deliver', o_name1, IP_MACHINE_LOCATION['assemble'], stackid)
    if o_name2 not in rae1.state.pos or rae1.state.pos[o_name2] != IP_MACHINE_LOCATION['assemble']:
        rae1.do_task('deliver', o_name2, IP_MACHINE_LOCATION['assemble'], stackid)
    rae1.do_command(assemble, o_name1, o_name2, name, stackid)
    return SUCCESS

def Pack_Method1(o1, o2, name, stackid):
    if isinstance(o1, list):
        o_name1 = GetNewName()
        Delegate(o1, o_name1, stackid)
    else:
        o_name1 = o1

    if isinstance(o2, list):
        o_name2 = GetNewName()
        Delegate(o2, o_name2, stackid)
    else:
        o_name2 = o2
    if o_name1 not in rae1.state.pos or rae1.state.pos[o_name1] != IP_MACHINE_LOCATION['pack']:
        rae1.do_task('deliver', o_name1, IP_MACHINE_LOCATION['pack'], stackid)
    if o_name2 not in rae1.state.pos or rae1.state.pos[o_name2] != IP_MACHINE_LOCATION['pack']:
        rae1.do_task('deliver', o_name2, IP_MACHINE_LOCATION['pack'], stackid)
    rae1.do_command(pack, o_name1, o_name2, name, stackid)
    return SUCCESS

def Order_Method1(taskArgs, stackid):
    taskName = taskArgs[0]
    taskArg1 = taskArgs[1]
    taskArg2 = taskArgs[2]
    name = GetNewName()
    rae1.do_task(taskName, taskArg1, taskArg2, name, stackid)
    rae1.do_task('deliver', name, IP_MACHINE_LOCATION['output'], stackid)
    return SUCCESS

def Deliver_Method1(o, l, stackid):
    if o not in rae1.state.pos:
        rae1.state.pos[o] = 1
    loc_o = rae1.state.pos[o]
    deliveryRobot = NIL
    while(deliveryRobot == NIL):
        for r in IP_ROBOTS:
            rae1.state.status.AcquireLock(r)
            if rae1.state.status[r] == 'free':
                deliveryRobot = r
                rae1.state.status[r] = 'busy'
                rae1.state.status.ReleaseLock(r)
                break
            rae1.state.status.ReleaseLock(r)
    rae1.do_command(move, deliveryRobot, rae1.state.loc[deliveryRobot], loc_o, stackid)
    rae1.do_command(take, deliveryRobot, o, loc_o, stackid)
    rae1.do_command(move, deliveryRobot, rae1.state.loc[deliveryRobot], l, stackid)
    rae1.do_command(put, deliveryRobot, o, l, stackid)

    rae1.state.status.AcquireLock(deliveryRobot)
    rae1.state.status[deliveryRobot] = 'free'
    rae1.state.status.ReleaseLock(deliveryRobot)
    return SUCCESS

def industryPlant_init():
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

    rae1.state.load = {'r1': NIL, 'r2': NIL}
    rae1.state.loc = {'r1': 2, 'r2': 4}
    rae1.state.status = {'r1': 'free', 'r2': 'free', 'paint': 'free', 'assemble': 'free', 'pack': 'free'}
    rae1.state.pos = {'a': IP_MACHINE_LOCATION['input'], 'b': IP_MACHINE_LOCATION['input'], 'c': IP_MACHINE_LOCATION['input'], 'o1': IP_MACHINE_LOCATION['input']}