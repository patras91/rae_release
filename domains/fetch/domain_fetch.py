__author__ = 'patras'

'''A robot is searching for an object in the environment consisting of a few locations. 
The robot knows the map. It is a rigid state variable.
The robot moves from one location to another using Djikstra's shortest path.
It has a battery that needs to be recharged after some moves.
A move consumes 1/4 of the battery capacity.'''

from domains.constants import *
from shared import gui
from shared.timer import globalTimer
from shared import GLOBALS # needed for heuristic (zero or domainSpecific), and for planning mode in environment
import numpy

class FetchDomain():
    def __init__(self, state, rv, actor, env):
        # params:
        # state: the state the domain operates on
        # actor: needed for do_task and do_command
        # env: the environment the domain gathers/senses information from

        self.state = state
        self.actor = actor
        self.env = env
        self.rv = rv
        #actor.declare_commands([self.put, self.take, self.perceive, self.charge, self.move, self.moveToEmergency, self.addressEmergency, self.wait, self.fail])

        actor.declare_task('search', 'r', 'o')
        actor.declare_task('fetch', 'r', 'o')
        actor.declare_task('recharge', 'r', 'c')
        actor.declare_task('moveTo', 'r', 'l')
        actor.declare_task('emergency', 'r', 'l', 'i')
        actor.declare_task('nonEmergencyMove', 'r', 'l1', 'l2', 'dist')

        actor.declare_methods('search', self.Search_Method1, self.Search_Method2)
        actor.declare_methods('fetch', self.Fetch_Method1, self.Fetch_Method2)
        actor.declare_methods('recharge', self.Recharge_Method1, self.Recharge_Method2, self.Recharge_Method3)
        actor.declare_methods('moveTo', self.MoveTo_Method1)
        actor.declare_methods('emergency', self.Emergency_Method1)
        actor.declare_methods('nonEmergencyMove', self.NonEmergencyMove_Method1)

        if GLOBALS.GetHeuristicName() == 'zero':
            actor.declare_heuristic('search', self.Heuristic1)
            actor.declare_heuristic('fetch', self.Heuristic1)
        elif GLOBALS.GetHeuristicName() == 'domainSpecific':
            actor.declare_heuristic('search', self.Heuristic2)
            actor.declare_heuristic('fetch', self.Heuristic2)

    def GetCommand(self, cmd_name):# save the commands by name
        return getattr(self, cmd_name)

    # Using Dijsktra's self.actororithm
    def GETDISTANCE(self, l0, l1):
        visitedDistances = {l0: 0}
        locs = list(self.rv.LOCATIONS)

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

            for l in self.rv.EDGES[min_loc]:
                dist = current_dist + 1
                if l not in visitedDistances or dist < visitedDistances[l]:
                    visitedDistances[l] = dist

        return visitedDistances[l1]

    def fail(self,):
        return FAILURE

    def take(self, r, o):
        self.state.load.AcquireLock(r)
        if self.state.load[r] == NIL:
            self.state.pos.AcquireLock(o)
            if self.state.loc[r] == self.state.pos[o]:
                start = globalTimer.GetTime()
                while(globalTimer.IsCommandExecutionOver('take', start) == False):
                    pass
                res = self.env.Sense('take')
                if res == SUCCESS:
                    gui.Simulate("Robot %s has picked up object %s\n" %(r, o))
                    self.state.pos[o] = r
                    self.state.load[r] = o
                else:
                    gui.Simulate("Non-deterministic event has made the take command fail\n")
            else:
                gui.Simulate("Robot %s is not at object %s's location\n" %(r, o))
                res = FAILURE
            self.state.pos.ReleaseLock(o)
        else:
            gui.Simulate("Robot %s is not free to take anything\n" %r)
            res = FAILURE
        self.state.load.ReleaseLock(r)
        return res

    def put(self, r, o):
        self.state.pos.AcquireLock(o)
        if self.state.pos[o] == r:
            start = globalTimer.GetTime()
            self.state.loc.AcquireLock(r)
            self.state.load.AcquireLock(r)
            while(globalTimer.IsCommandExecutionOver('put', start) == False):
                pass
            res = self.env.Sense('put')
            if res == SUCCESS:    
                gui.Simulate("Robot %s has put object %s at location %d\n" %(r,o,self.state.loc[r]))
                self.state.pos[o] = self.state.loc[r]
                self.state.load[r] = NIL
            else:
                gui.Simulate("Robot %s has failed to put %s because of some internal error")
            self.state.loc.ReleaseLock(r)
            self.state.load.ReleaseLock(r)
        else:
            gui.Simulate("Object %s is not with robot %s\n" %(o,r))
            res = FAILURE
        self.state.pos.ReleaseLock(o)
        return res

    def charge(self, r, c):
        self.state.loc.AcquireLock(r)
        self.state.pos.AcquireLock(c)
        if self.state.loc[r] == self.state.pos[c] or self.state.pos[c] == r:
            self.state.charge.AcquireLock(r)
            start = globalTimer.GetTime()
            while(globalTimer.IsCommandExecutionOver('charge', start) == False):
                pass
            res = self.env.Sense('charge')
            if res == SUCCESS:
                self.state.charge[r] = 4
                gui.Simulate("Robot %s is fully charged\n" %r)
            else:
                gui.Simulate("Charging of robot %s failed due to some internal error.\n" %r)
            self.state.charge.ReleaseLock(r)
        else:
            gui.Simulate("Robot %s is not in the charger's location or it doesn't have the charger with it\n" %r)
            res = FAILURE
        self.state.loc.ReleaseLock(r)
        self.state.pos.ReleaseLock(c)
        return res

    def moveToEmergency(self, r, l1, l2, dist):
        self.state.loc.AcquireLock(r)
        self.state.charge.AcquireLock(r)
        if l1 == l2:
            gui.Simulate("Robot %s is already at location %s\n" %(r, l2))
            res = SUCCESS
        elif self.state.loc[r] == l1 and self.state.charge[r] >= dist:
            start = globalTimer.GetTime()
            while(globalTimer.IsCommandExecutionOver('move', start) == False):
               pass
            res = self.env.Sense('moveToEmergency')
            if res == SUCCESS:
                gui.Simulate("Robot %s has moved from %d to %d\n" %(r, l1, l2))
                self.state.loc[r] = l2
                self.state.charge[r] = self.state.charge[r] - dist
            else:
                gui.Simulate("Moving failed due to some internal error\n")
        elif self.state.loc[r] != l1 and self.state.charge[r] >= dist:
            gui.Simulate("Robot %s is not in location %d\n" %(r, l1))
            res = FAILURE
        elif self.state.loc[r] == l1 and self.state.charge[r] < dist:
            gui.Simulate("Robot %s does not have enough charge to move :(\n" %r)
            self.state.charge[r] = 0 # should we do this?
            res = FAILURE
        else:
            gui.Simulate("Robot %s is not at location %s and it doesn't have enough charge!\n" %(r, l1))
            res = FAILURE
        self.state.loc.ReleaseLock(r)
        self.state.charge.ReleaseLock(r)
        if res == FAILURE:
            self.state.emergencyHandling.AcquireLock(r)
            self.state.emergencyHandling[r] = False
            self.state.emergencyHandling.ReleaseLock(r)
        return res

    def perceive(self, l):
        self.state.view.AcquireLock(l)
        if self.state.view[l] == False:
            start = globalTimer.GetTime()
            while(globalTimer.IsCommandExecutionOver('perceive', start) == False):
                pass
            self.env.Sense('perceive')
            for c in self.state.containers[l]:
                self.state.pos.AcquireLock(c)
                self.state.pos[c] = l
                self.state.pos.ReleaseLock(c)
            self.state.view[l] = True
            gui.Simulate("Perceived location %d\n" %l)
        else:
            gui.Simulate("Already perceived\n")
        self.state.view.ReleaseLock(l)
        return SUCCESS

    def move(self, r, l1, l2, dist):
        self.state.emergencyHandling.AcquireLock(r)
        if self.state.emergencyHandling[r] == False:
            self.state.loc.AcquireLock(r)
            self.state.charge.AcquireLock(r)
            if l1 == l2:
                gui.Simulate("Robot %s is already at location %s\n" %(r, l2))
                res = SUCCESS
            elif self.state.loc[r] == l1 and (self.state.charge[r] >= dist or self.state.load[r] == 'c1'):
                start = globalTimer.GetTime()
                while(globalTimer.IsCommandExecutionOver('move', start) == False):
                   pass
                res = self.env.Sense('move')
                if res == SUCCESS:
                    gui.Simulate("Robot %s has moved from %d to %d\n" %(r, l1, l2))
                    self.state.loc[r] = l2
                    if self.state.load[r] != 'c1':
                        self.state.charge[r] = self.state.charge[r] - dist
                else:
                    gui.Simulate("Robot %s failed to move due to some internal failure\n" %r)
            elif self.state.loc[r] != l1 and self.state.charge[r] >= dist:
                gui.Simulate("Robot %s is not in location %d\n" %(r, l1))
                res = FAILURE
            elif self.state.loc[r] == l1 and self.state.charge[r] < dist:
                gui.Simulate("Robot %s does not have enough charge to move :(\n" %r)
                self.state.charge[r] = 0 # should we do this?
                res = FAILURE
            else:
                gui.Simulate("Robot %s is not at location %s and it doesn't have enough charge!\n" %(r, l1))
                res = FAILURE
            self.state.loc.ReleaseLock(r)
            self.state.charge.ReleaseLock(r)
        else:
            gui.Simulate("Robot is addressing emergency so it cannot move.\n")
            res = FAILURE
        self.state.emergencyHandling.ReleaseLock(r)
        return res

    def addressEmergency(self, r, l, i):
        self.state.loc.AcquireLock(r)
        self.state.emergencyHandling.AcquireLock(r)
        if self.state.loc[r] == l:
            start = globalTimer.GetTime()
            while(globalTimer.IsCommandExecutionOver('addressEmergency', start) == False):
                pass
            res = self.env.Sense('addressEmergency')
            if res == SUCCESS:
                gui.Simulate("Robot %s has addressed emergency %d\n" %(r, i))
            else:
                gui.Simulate("Robot %s has failed to address emergency due to some internal error \n" %r)
        else:
            gui.Simulate("Robot %s has failed to address emergency %d\n" %(r, i))
            res = FAILURE
        self.state.emergencyHandling[r] = False
        self.state.loc.ReleaseLock(r)
        self.state.emergencyHandling.ReleaseLock(r)
        return res

    def wait(self, r):
        while(self.state.emergencyHandling[r] == True):
            start = globalTimer.GetTime()
            while(globalTimer.IsCommandExecutionOver('wait', start) == False):
                pass
            #gui.Simulate("Robot %s is waiting for emergency to be over\n" %r)
            self.env.Sense('wait')
        return SUCCESS

    def Recharge_Method3(self, r, c):
        """ Robot r charges and carries the charger with it """
        if self.state.loc[r] != self.state.pos[c] and self.state.pos[c] != r:
            if self.state.pos[c] in self.rv.LOCATIONS:
                self.actor.do_task('moveTo', r, self.state.pos[c])
            else:
                robot = self.state.pos[c]
                self.actor.do_command(self.put, robot, c)
                self.actor.do_task('moveTo', r, self.state.pos[c])
        self.actor.do_command(self.charge, r, c)
        self.actor.do_command(self.take, r, c)

    def Recharge_Method2(self, r, c):
        """ Robot r charges and does not carry the charger with it """
        if self.state.loc[r] != self.state.pos[c] and self.state.pos[c] != r:
            if self.state.pos[c] in self.rv.LOCATIONS:
                self.actor.do_task('moveTo', r, self.state.pos[c])
            else:
                robot = self.state.pos[c]
                self.actor.do_command(self.put, robot, c)
                self.actor.do_task('moveTo', r, self.state.pos[c])
        self.actor.do_command(self.charge, r, c)

    def Recharge_Method1(self, r, c):
        """ When the charger is with another robot and that robot takes the charger back """ 
        robot = NIL
        if self.state.loc[r] != self.state.pos[c] and self.state.pos[c] != r:
            if self.state.pos[c] in self.rv.LOCATIONS:
                self.actor.do_task('moveTo', r, self.state.pos[c])
            else:
                robot = self.state.pos[c]
                self.actor.do_command(self.put, robot, c)
                self.actor.do_task('moveTo', r, self.state.pos[c])
        self.actor.do_command(self.charge, r, c)
        if robot != NIL:
            self.actor.do_command(self.take, robot, c)

    def Search_Method1(self, r, o):
        if self.state.pos[o] == UNK:
            toBePerceived = NIL
            for l in self.rv.LOCATIONS:
                if self.state.view[l] == False:
                    toBePerceived = l
                    break

            if toBePerceived != NIL:
                self.actor.do_task('moveTo', r, toBePerceived)
                self.actor.do_command(self.perceive, toBePerceived)
                if self.state.pos[o] == toBePerceived:
                    if self.state.load[r] != NIL:
                        self.actor.do_command(self.put, r, self.state.load[r])
                    self.actor.do_command(self.take, r, o)
                else:
                    self.actor.do_task('search', r, o)
            else:
                gui.Simulate("Failed to search %s" %o)
                self.actor.do_command(self.fail)
        else:
            gui.Simulate("Position of %s is already known\n" %o)

    def Search_Method2(self, r, o):
        if self.state.pos[o] == UNK:
            toBePerceived = NIL
            for l in self.rv.LOCATIONS:
                if self.state.view[l] == False:
                    toBePerceived = l
                    break

            if toBePerceived != NIL:
                self.actor.do_task('recharge', r, 'c1') # is this allowed?
                self.actor.do_task('moveTo', r, toBePerceived)
                self.actor.do_command(self.perceive, toBePerceived)
                if self.state.pos[o] == toBePerceived:
                    if self.state.load[r] != NIL:
                        self.actor.do_command(self.put, r, self.state.load[r])
                    self.actor.do_command(self.take, r, o)
                else:
                    self.actor.do_task('search', r, o)
            else:
                gui.Simulate("Failed to search %s" %o)
                self.actor.do_command(self.fail)
        else:
            gui.Simulate("Position of %s is already known\n" %o)

    def Fetch_Method1(self, r, o):
        pos_o = self.state.pos[o]
        if pos_o == UNK:
            self.actor.do_task('search', r, o)
        else:
            if self.state.loc[r] != pos_o:
                self.actor.do_task('moveTo', r, pos_o)
            if self.state.load[r] != NIL:
                self.actor.do_command(self.put, r, self.state.load[r])
            self.actor.do_command(self.take, r, o)

    def Fetch_Method2(self, r, o):
        pos_o = self.state.pos[o]
        if pos_o == UNK:
            self.actor.do_task('search', r, o)
        else:
            if self.state.loc[r] != pos_o:
                self.actor.do_task('recharge', r, 'c1')
                self.actor.do_task('moveTo', r, pos_o)
            if self.state.load[r] != NIL:
                self.actor.do_command(self.put, r, self.state.load[r])
            self.actor.do_command(self.take, r, o)

    def Emergency_Method1(self, r, l, i):
        if self.state.emergencyHandling[r] == False:
            self.state.emergencyHandling[r] = True
            load_r = self.state.load[r]
            if load_r != NIL:
                self.actor.do_command(self.put, r, load_r)
            l1 = self.state.loc[r]
            dist = self.GETDISTANCE(l1, l)
            self.actor.do_command(self.moveToEmergency, r, l1, l, dist)
            self.actor.do_command(self.addressEmergency, r, l, i)
        else:
            gui.Simulate("%r is already busy handling another emergency\n" %r)
            self.actor.do_command(self.fail)

    def NonEmergencyMove_Method1(self, r, l1, l2, dist):
        if self.state.emergencyHandling[r] == False:
            self.actor.do_command(self.move, r, l1, l2, dist)
        else:
            self.actor.do_command(self.wait, r)
            self.actor.do_command(self.move, r, l1, l2, dist)

    def MoveTo_Method1(self, r, l):
        x = self.state.loc[r]
        dist = self.GETDISTANCE(x, l)
        if self.state.charge[r] >= dist or self.state.load[r] == 'c1':
            self.actor.do_task('nonEmergencyMove', r, x, l, dist)
        else:
            self.state.charge[r] = 0
            gui.Simulate("Robot %s does not have enough charge to move from %d to %d\n" %(r, x, l))
            self.actor.do_command(self.fail)

    def Heuristic1(self, args):
        return float("inf")

    def Heuristic2(self, args):
        robot = args[0]
        return 5 * self.state.charge[robot]

    # TODO
    #def goalMethod1(self):
    #   pass

class FetchEnv():
    def __init__(self, state, rv):
        self.commandProb = {
            'take': [0.9, 0.1],
            'put': [0.99, 0.01],
            'charge': [0.90, 0.10],
            'moveToEmergency': [0.99, 0.01],
            'move': [0.95, 0.05],
            'addressEmergency': [0.98, 0.02],
        }
        self.state = state
        self.rv = rv

    def Sense(self, cmd):
        if cmd == 'perceive':
            if GLOBALS.GetPlanningMode() == True:
                return self.SenseObjects()
            else:
                return SUCCESS
        elif cmd == 'wait':
            if GLOBALS.GetPlanningMode() == True:
                for r in self.rv.ROBOTS:
                    self.state.emergencyHandling[r] = False
        else:
            p = self.commandProb[cmd]
            outcome = numpy.random.choice(len(p), 50, p=p)
            res = outcome[0]
            if res == 0:
                return SUCCESS
            else:
                return FAILURE

    def SenseObjects(self):
        total = 0
        for loc in self.state.containers:
            self.state.containers[loc] = []
            if self.state.view[loc] == False:
                total += 1

        for o in self.rv.OBJECTS:
            prob = {}
            if self.state.pos[o] == UNK:
                for l in self.state.view:
                    if self.state.view[l] == False:
                        prob[l] = 1/total
                p = list(prob.values())
                locs = list(prob.keys())
                locIndex = numpy.random.choice(len(p), 50, p=p)
                self.state.containers[locs[locIndex[0]]].append(o)