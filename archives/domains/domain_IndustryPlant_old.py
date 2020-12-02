__author__ = 'patras'

from ape import state, do_task, do_command, declare_commands, declare_methods, declare_prob
from gui import Simulate
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
            dist = current_dist + 1
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
            dist = current_dist + 1
            if l not in visitedDistances or dist < visitedDistances[l]:
                visitedDistances[l] = dist
                path[l] = min_loc
    l = l1
    path2 = {}
    while l != l0:
        path2[path[l]] = l
        l = path[l]

    return path2

def damage(*machines):
    for m in machines:
        state.cond.AcquireLock(m)
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('damage', start) == False):
            pass
        Simulate("Machine %s is damaged\n" %m)
        state.cond[m] = NOTOK
        state.cond.ReleaseLock(m)
    return SUCCESS

def repairc(m):
    state.cond.AcquireLock(m)
    start = globalTimer.GetTime()
    while(globalTimer.IsCommandExecutionOver('repair', start) == False):
        pass
    Simulate("Machine %s is repaired\n" %m)
    state.cond[m] = OK
    state.cond.ReleaseLock(m)
    return SUCCESS

def GetProbability_repairc(m):
    return [1]

declare_prob(repairc, GetProbability_repairc)
def repairc_Sim(m, outcome):
    state.cond[m] = OK
    return SUCCESS

def GetNewName():
    GetNewName.current += 1
    return 'TMPOBJECT' + GetNewName.current.__str__()

GetNewName.current = 0

def paint(m, o, colour, name):
    state.pos.AcquireLock(o)
    if state.pos[o] == rv.MACHINE_LOCATION[m]:
        if state.cond[m] == OK:
            state.status.AcquireLock(m)
            #Simulate("%s is colouring %s with colour %s and naming it %s\n" %(m, o, colour, name))
            start = globalTimer.GetTime()
            while(globalTimer.IsCommandExecutionOver('paint', start) == False):
                pass
            state.pos[name] = rv.MACHINE_LOCATION[m]
            state.status[m] = 'free'
            res = SUCCESS
            state.status.ReleaseLock(m)
        else:
            Simulate("%s is damaged\n" %m)
            res = FAILURE

    else:
        #Simulate("%s is not in painting machine %s's location\n" %(o, m))
        Simulate("object not in machine location", o, m, rv)
        res = FAILURE
    state.pos.ReleaseLock(o)
    return res

def GetProbability_paint(m, o, colour, name):
    if state.pos[o] == rv.MACHINE_LOCATION[m]:
        if state.cond[m] == OK:
            return [0.8, 0.2]
        else:
            return [0.2, 0.8]
    else:
        return [0.2, 0.8]

declare_prob(paint, GetProbability_paint)
def paint_Sim(m, o, colour, name, outcome):
    if outcome == 0:
        state.pos[name] = rv.MACHINE_LOCATION[m]
        state.status[m] = 'free'
        res = SUCCESS
    else:
        res = FAILURE
    return res

def wrap(m, o, name):
    state.pos.AcquireLock(o)
    if state.pos[o] == rv.MACHINE_LOCATION[m]:
        if state.cond[m] == OK:
            state.status.AcquireLock(m)
            Simulate("%s is wrapping %s and naming it %s\n" %(m, o, name))
            start = globalTimer.GetTime()
            while(globalTimer.IsCommandExecutionOver('wrap', start) == False):
                pass
            state.pos[name] = rv.MACHINE_LOCATION[m]
            state.status[m] = 'free'
            res = SUCCESS
            state.status.ReleaseLock(m)
        else:
           Simulate("%s is damaged\n" %m)
           res = FAILURE
    else:
        Simulate("%s is not in wrapping machine's location\n" %o)
        res = FAILURE
    state.pos.ReleaseLock(o)
    return res

def GetProbability_wrap(m, o, name):
    if state.pos[o] == rv.MACHINE_LOCATION[m]:
        if state.cond[m] == OK:
            return [0.8, 0.2]
        else:
           return [0.2, 0.8]
    else:
        return [0.2, 0.8]

declare_prob(wrap, GetProbability_wrap)
def wrap_Sim(m, o, name, outcome):
    if outcome == 0:
        state.pos[name] = rv.MACHINE_LOCATION[m]
        state.status[m] = 'free'
        res = SUCCESS
    else:
       res = FAILURE
    return res

def assemble(m, p1, p2, name):
    state.pos.AcquireLock(p1)
    state.pos.AcquireLock(p2)

    if state.pos[p1] == rv.MACHINE_LOCATION[m] and state.pos[p2] == rv.MACHINE_LOCATION[m]:
        if state.cond[m] == OK:
            state.status.AcquireLock(m)
            start = globalTimer.GetTime()
            while(globalTimer.IsCommandExecutionOver('assemble', start) == False):
                pass
            Simulate("Assembled parts %s and %s and naming it %s\n" %(p1, p2, name))
            state.pos[name] = rv.MACHINE_LOCATION[m]
            state.status[m] = 'free'
            res = SUCCESS
            state.status.ReleaseLock(m)
        else:
           Simulate("%s is damaged\n" %m)
           res = FAILURE
    else:
        Simulate("Part %s or %s is not in painting machine's location\n" %(p1, p2))
        res = FAILURE
    state.pos.ReleaseLock(p1)
    state.pos.ReleaseLock(p2)
    return res

def GetProbability_assemble(m, p1, p2, name):
    if state.pos[p1] == rv.MACHINE_LOCATION[m] and state.pos[p2] == rv.MACHINE_LOCATION[m]:
        if state.cond[m] == OK:
            return [0.8, 0.2]
        else:
            return [0.2, 0.8]
    else:
        return [0.2, 0.8]

declare_prob(assemble, GetProbability_assemble)
def assemble_Sim(m, p1, p2, name, outcome):
    if outcome == 0:
        state.pos[name] = rv.MACHINE_LOCATION[m]
        state.status[m] = 'free'
        res = SUCCESS
    else:
       res = FAILURE
    return res

def pack(m, o1, o2, name):
    state.pos.AcquireLock(o1)
    state.pos.AcquireLock(o2)
    if state.pos[o1] == rv.MACHINE_LOCATION[m] and state.pos[o2] == rv.MACHINE_LOCATION[m]:
        if state.cond[m] == OK:
            state.status.AcquireLock(m)
            start = globalTimer.GetTime()
            while(globalTimer.IsCommandExecutionOver('pack', start) == False):
                pass
            Simulate("Packed objects %s and %s and naming it %s\n" %(o1, o2, name))
            state.pos[name] = rv.MACHINE_LOCATION[m]
            state.status.ReleaseLock(m)
            res = SUCCESS
        else:
           Simulate("%s is damaged\n" %m)
           res = FAILURE
    else:
        Simulate("Part %s or %s is not in packing machine's location\n" %(o1, o2))
        res = FAILURE
    state.pos.ReleaseLock(o1)
    state.pos.ReleaseLock(o2)
    return res

def GetProbability_pack(m, o1, o2, name):
    if state.pos[o1] == rv.MACHINE_LOCATION[m] and state.pos[o2] == rv.MACHINE_LOCATION[m]:
        if state.cond[m] == OK:
            return [0.8, 0.2]
        else:
            return [0.2, 0.8]
    else:
        return [0.2, 0.8]

declare_prob(pack, GetProbability_pack)
def pack_Sim(m, o1, o2, name, outcome):
    if outcome == 0:
        state.pos[name] = rv.MACHINE_LOCATION[m]
        res = SUCCESS
    else:
       res = FAILURE
    return res

def take(r, o, l):
    state.pos.AcquireLock(o)
    if state.pos[o] == l:
        state.load.AcquireLock(r)
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('take', start) == False):
            pass
        state.pos[o] = r
        state.load[r] = o
        state.load.ReleaseLock(r)
        Simulate("Robot %s has taken object %s at location %d\n" %(r,o,l))
        res = SUCCESS
    else:
        Simulate("Object %s is not at location %d\n" %(o,l))
        res = FAILURE
    state.pos.ReleaseLock(o)
    return res

def GetProbability_take(r, o, l):
    state.pos.AcquireLock(o)
    if state.pos[o] == l:
        return [0.8, 0.2]
    else:
        return [0.2, 0.8]

declare_prob(take, GetProbability_take)
def take_Sim(r, o, l, outcome):
    if outcome == 0:
        state.pos[o] = r
        state.load[r] = o
        res = SUCCESS
    else:
        res = FAILURE
    return res

def put(r, o, l):
    state.pos.AcquireLock(o)
    if state.pos[o] == r:
        state.load.AcquireLock(r)
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('put', start) == False):
            pass
        state.pos[o] = l
        state.load[r] = NIL
        state.load.ReleaseLock(r)
        Simulate("Robot %s has put object %s at location %d\n" %(r,o,l))
        res = SUCCESS
    else:
        Simulate("Object %s is not with robot %s\n" %(o,r))
        res = FAILURE
    state.pos.ReleaseLock(o)
    return res

def GetProbability_put(r, o, l):
    if state.pos[o] == r:
        return [0.8, 0.2]
    else:
        return [0.2, 0.8]

declare_prob(put, GetProbability_put)
def put_Sim(r, o, l, outcome):
    if outcome == 0:
        state.pos[o] = l
        state.load[r] = NIL
        res = SUCCESS
    else:
        res = FAILURE
    return res

def move(r, loc1, loc2):
    state.loc.AcquireLock(r)
    if state.loc[r] == loc1:
        start = globalTimer.GetTime()
        while(globalTimer.IsCommandExecutionOver('move', start) == False):
            pass
        state.loc[r] = loc2
        #Simulate("%s has moved from %s to %s\n" %(r, loc1, loc2))
        Simulate('move', r, loc1, loc2)
        res = SUCCESS
    else:
        #Simulate("%s is not in location %s\n" %(r, loc1))
        Simulate("not in location", r, loc1)
        res = FAILURE
    state.loc.ReleaseLock(r)
    return res

def GetProbability_move(r, loc1, loc2):
    if state.loc[r] == loc1:
        return [0.9, 0.1]
    else:
        return [0.1, 0.9]

declare_prob(move, GetProbability_move)
def move_Sim(r, loc1, loc2, outcome):
    if outcome == 0:
        state.loc[r] = loc2
        res = SUCCESS
    else:
        res = FAILURE
    return res

def Delegate(o, o_name):
    taskName = o[0]
    taskArgs = o[1:]
    do_task(taskName, o_name, *taskArgs)

def GetMachine(job, loc):
    free = [m for m in rv.MACHINES[job] if state.status[m] == 'free']
    dist = [IP_GETDISTANCE(loc, rv.MACHINE_LOCATION[m]) for m in free]
    if free == []:
        return NIL
    else:
        return free[dist.index(min(dist))]

def GetLocation(o):
    if o not in state.pos:
        state.pos[o] = rv.BUFFERS['input']
    return state.pos[o]

def Paint_Method1(name, *args):
    o = args[0]
    colour = args[1]
    if isinstance(o, list):
        o_name = GetNewName()
        Delegate(o, o_name)
    else:
        o_name = o

    m = GetMachine('paint', GetLocation(o_name))
    if m != NIL:
        if state.cond[m] == OK:
            if GetLocation(o_name) != rv.MACHINE_LOCATION[m]:
                do_task('deliver', o_name, rv.MACHINE_LOCATION[m])
            do_command(paint, m, o_name, colour, name)
            res = SUCCESS
        else:
            Simulate("Machine %s for painting is damaged " %m)
            res = FAILURE
    else:
        Simulate("There are no machines free to paint.\n")
        res = FAILURE
    return res

def Paint_Method2(name, *args):
    o = args[0]
    colour = args[1]
    if isinstance(o, list):
        o_name = GetNewName()
        Delegate(o, o_name)
    else:
        o_name = o

    m = GetMachine('paint', GetLocation(o_name))
    if m != NIL:
        if state.cond[m] == NOTOK:
            do_task('repair', m)
        if GetLocation(o_name) != rv.MACHINE_LOCATION[m]:
            do_task('deliver', o_name, rv.MACHINE_LOCATION[m])
        do_command(paint, m, o_name, colour, name)
        res = SUCCESS
    else:
        Simulate("There are no machines free to paint.\n")
        res = FAILURE
    return res

def Assemble_Method2(name, *args):
    part1 = args[0]
    part2 = args[1]
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

    m = GetMachine('assemble', GetLocation(o_name1))
    if m != NIL:
        if state.cond[m] == NOTOK:
            do_task('repair', m)
        if GetLocation(o_name1) != rv.MACHINE_LOCATION[m]:
            do_task('deliver', o_name1, rv.MACHINE_LOCATION[m])
        if GetLocation(o_name2) != rv.MACHINE_LOCATION[m]:
            do_task('deliver', o_name2, rv.MACHINE_LOCATION[m])
        do_command(assemble, m, o_name1, o_name2, name)
        res = SUCCESS
    else:
        Simulate("There are no machines free to assemble.\n")
        res = FAILURE
    return res

def Assemble_Method1(name, *args):
    part1 = args[0]
    part2 = args[1]
    if isinstance(part1, list):
        o_name1 = GetNewName()
        Delegate(part1, o_name1)
    else:
        o_name1 = part1

    m = GetMachine('assemble', GetLocation(o_name1))
    if m != NIL:
        if state.cond[m] == NOTOK:
            do_task('repair', m)
        if GetLocation(o_name1) != rv.MACHINE_LOCATION[m]:
            do_task('deliver', o_name1, rv.MACHINE_LOCATION[m])
    else:
        Simulate("There are no machines free to assemble.\n")
        return FAILURE

    if isinstance(part2, list):
        o_name2 = GetNewName()
        Delegate(part2, o_name2)
    else:
        o_name2 = part2

    if GetLocation(o_name2) != rv.MACHINE_LOCATION[m]:
        do_task('deliver', o_name2, rv.MACHINE_LOCATION[m])

    do_command(assemble, m, o_name1, o_name2, name)

    return SUCCESS

def Pack_Method2(name, *args):
    o1 = args[0]
    o2 = args[1]
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

    m = GetMachine('pack', GetLocation(o_name1))
    if m != NIL:
        if state.cond[m] == NOTOK:
            do_task('repair', m)
        if GetLocation(o_name1) != rv.MACHINE_LOCATION[m]:
            do_task('deliver', o_name1, rv.MACHINE_LOCATION[m])
        if GetLocation(o_name2) != rv.MACHINE_LOCATION[m]:
            do_task('deliver', o_name2, rv.MACHINE_LOCATION[m])
        do_command(pack, m, o_name1, o_name2, name)
        res = SUCCESS
    else:
        Simulate("There are no machines free to pack.\n")
        res = FAILURE
    return res

def Pack_Method1(name, *args):
    o1 = args[0]
    o2 = args[1]
    if isinstance(o1, list):
        o_name1 = GetNewName()
        Delegate(o1, o_name1)
    else:
        o_name1 = o1

    m = GetMachine('pack', GetLocation(o_name1))
    if m != NIL:
        if state.cond[m] == NOTOK:
            do_task('repair', m)
    else:
        Simulate("There are no machines free to pack.\n")
        return FAILURE

    if GetLocation(o_name1) != rv.MACHINE_LOCATION[m]:
        do_task('deliver', o_name1, rv.MACHINE_LOCATION[m])

    if isinstance(o2, list):
        o_name2 = GetNewName()
        Delegate(o2, o_name2)
    else:
        o_name2 = o2

    if GetLocation(o_name2) != rv.MACHINE_LOCATION[m]:
        do_task('deliver', o_name2, rv.MACHINE_LOCATION[m])
    do_command(pack, m, o_name1, o_name2, name)

    return SUCCESS

def Wrap_Method1(name, o):
    if isinstance(o, list):
        o_name = GetNewName()
        Delegate(o, o_name)
    else:
        o_name = o

    m = GetMachine('wrap', GetLocation(o_name))
    if m != NIL:
        if GetLocation(o_name) != rv.MACHINE_LOCATION[m]:
            do_task('deliver', o_name, rv.MACHINE_LOCATION[m])
        do_command(wrap, m, o_name, name)
        res = SUCCESS
    else:
        Simulate("There are no machines free to wrap.\n")
        res = FAILURE
    return res

def Wrap_Method2(name, o):
    if isinstance(o, list):
        o_name = GetNewName()
        Delegate(o, o_name)
    else:
        o_name = o

    m = GetMachine('wrap', GetLocation(o_name))
    if m != NIL:
        do_task('repair', m)
        if GetLocation(o_name) != rv.MACHINE_LOCATION[m]:
            do_task('deliver', o_name, rv.MACHINE_LOCATION[m])
        do_command(wrap, m, o_name, name)
        res = SUCCESS
    else:
        Simulate("There are no machines free to wrap.\n")
        res = FAILURE
    return res

def Order_Method1(taskArgs):
    taskName = taskArgs[0]
    args = taskArgs[1:]
    name = GetNewName()
    do_task(taskName, name, *args)
    do_task('deliver', name, rv.BUFFERS['output'])
    return SUCCESS

def GetRobot(loc):
    free = [r for r in rv.ROBOTS if state.status[r] == 'free']
    dist = [IP_GETDISTANCE(loc, state.loc[r]) for r in free]
    if dist != []:
        r = free[dist.index(min(dist))]
        deliveryRobot = r
        state.status[r] = 'busy'
    else:
        deliveryRobot = NIL
    return deliveryRobot

def Deliver_Method1(o, l):
    loc_o = GetLocation(o)
    deliveryRobot = GetRobot(loc_o)
    if deliveryRobot != NIL:
        if state.loc[deliveryRobot] != loc_o:
            do_task('moveTo', deliveryRobot, state.loc[deliveryRobot], loc_o)
        do_command(take, deliveryRobot, o, loc_o)
        if state.loc[deliveryRobot] != l:
            do_task('moveTo', deliveryRobot, state.loc[deliveryRobot], l)
        do_command(put, deliveryRobot, o, l)
        state.status[deliveryRobot] = 'free'
        res = SUCCESS
    else:
        Simulate("No robot free to deliver %s to location %s\n" %(o, l))
        res = FAILURE
    return res

def Repair_Method1(m):
    repairBot = GetRobot(rv.MACHINE_LOCATION[m])
    if repairBot != NIL:
        if state.loc[repairBot] != rv.MACHINE_LOCATION[m]:
            do_task('moveTo', repairBot, state.loc[repairBot], rv.MACHINE_LOCATION[m])
        do_command(repairc, m)
        state.status[repairBot] = 'free'
        res = SUCCESS
    else:
        Simulate("No robot is free to repair %s\n" %m)
        res = FAILURE
    return res

def MoveTo_Method1(r, l1, l2):
    res = SUCCESS
    path = IP_GETPATH(l1, l2)
    if path == {}:
        Simulate("%s is already at location %s \n" %(r, l2))
    else:
        lTemp = state.loc[r]
        if lTemp not in path:
            Simulate("%s is out of its path to %s\n" %(r, l2))
            res = FAILURE
        else:
            while(lTemp != l2):
                lNext = path[lTemp]
                do_command(move, r, lTemp, lNext)
                if lNext != state.loc[r]:
                    Simulate("%s is out of its path to %s\n" %(r, l2))
                    res = FAILURE
                    break
                else:
                    lTemp = lNext
    return res

rv = RV()
declare_commands([paint, assemble, pack, take, put, move, wrap, repairc],
                 [paint_Sim, assemble_Sim, pack_Sim, take_Sim, put_Sim, move_Sim, wrap_Sim, repairc_Sim])

declare_methods('paint', Paint_Method1, Paint_Method2)
declare_methods('assemble', Assemble_Method1, Assemble_Method2)
declare_methods('pack', Pack_Method1, Pack_Method2)
declare_methods('wrap', Wrap_Method1, Wrap_Method2)
declare_methods('deliver', Deliver_Method1)
declare_methods('order', Order_Method1)
declare_methods('repair', Repair_Method1)
declare_methods('moveTo', MoveTo_Method1)