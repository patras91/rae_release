__author__ = 'patras'

''' Search and Rescue domain:
    There are some natural disasters happening in an area.
    Robots with the help of human experts do search and rescue operations in this area. 
'''

from domains.constants import *
from shared import gui
from shared.timer import globalTimer
from shared import GLOBALS # needed for heuristic (zero or domainSpecific), and for planning mode in environment
import numpy
import math

class RescueDomain():
    def __init__(self, state, rv, actor, env):
        # params:
        # state: the state the domain operates on
        # actor: needed for do_task and do_command
        # env: the environment the domain gathers/senses information from

        self.state = state
        self.actor = actor
        self.env = env
        self.rv = rv

        # self.actor.declare_commands([
        #     moveEuclidean,
        #     moveCurved,
        #     moveManhattan,
        #     fly,
        #     giveSupportToPerson,
        #     clearLocation,
        #     inspectLocation,
        #     inspectPerson,
        #     transfer,
        #     replenishSupplies,
        #     captureImage,
        #     changeAltitude,
        #     deadEnd,
        #     fail
        # ])

        self.actor.declare_task('moveTo', 'r', 'l')
        self.actor.declare_task('rescue', 'r', 'p')
        self.actor.declare_task('helpPerson', 'r', 'p')
        self.actor.declare_task('getSupplies', 'r')
        self.actor.declare_task('survey', 'r', 'l')
        self.actor.declare_task('getRobot')
        self.actor.declare_task('adjustAltitude', 'r')

        self.actor.declare_methods('moveTo',
                                   self.MoveTo_Method4,
                                   self.MoveTo_Method3,
                                   self.MoveTo_Method2,
                                   self.MoveTo_Method1,
                                   )

        self.actor.declare_methods('rescue',
                                   self.Rescue_Method1,
                                   self.Rescue_Method2,
                                   )

        self.actor.declare_methods('helpPerson',
                                   self.HelpPerson_Method2,
                                   self.HelpPerson_Method1,
                                   )

        self.actor.declare_methods('getSupplies',
                                   self.GetSupplies_Method2,
                                   self.GetSupplies_Method1,
                                   )

        self.actor.declare_methods('survey',
                                   self.Survey_Method1,
                                   self.Survey_Method2
                                   )

        self.actor.declare_methods('getRobot',
                                   self.GetRobot_Method1,
                                   self.GetRobot_Method2,
                                   )

        self.actor.declare_methods('adjustAltitude',
                                   self.AdjustAltitude_Method1,
                                   self.AdjustAltitude_Method2,
                                   )

        if GLOBALS.GetHeuristicName() == 'h1':
            self.actor.declare_heuristic('survey', self.Heuristic1)
        elif GLOBALS.GetHeuristicName() == 'h2':
            self.actor.declare_heuristic('survey', self.Heuristic2)

    def GetCommand(self, cmd_name):# save the commands by name
        return getattr(self, cmd_name)

    def fail(self):
        return FAILURE

    def deadEnd(self, p):
        self.state.status[p] = 'dead'
        self.state.realStatus[p] = 'dead'
        return FAILURE

    def moveEuclidean(self, r, l1, l2, dist):
        (x1, y1) = l1
        (x2, y2) = l2
        xlow = min(x1, x2)
        xhigh = max(x1, x2)
        ylow = min(y1, y2)
        yhigh = max(y1, y2)
        for o in self.rv.OBSTACLES:
            (ox, oy) = o
            if ox >= xlow and ox <= xhigh and oy >= ylow and oy <= yhigh:
                if ox == x1 or x2 == x1:
                    gui.Simulate("%s cannot move in Euclidean path because of obstacle\n" %r)
                    return FAILURE
                elif abs((oy - y1)/(ox - x1) - (y2 - y1)/(x2 - x1)) <= 0.0001:
                    gui.Simulate("%s cannot move in Euclidean path because of obstacle\n" %r)
                    return FAILURE

        self.state.loc.AcquireLock(r)
        if l1 == l2:
            gui.Simulate("Robot %s is already at location %s\n" %(r, l2))
            res = SUCCESS
        elif self.state.loc[r] == l1:
            start = globalTimer.GetTime()
            while(globalTimer.IsCommandExecutionOver('moveEuclidean', start, r, l1, l2, dist) == False):
               pass
            res = self.env.Sense('moveEuclidean')
            if res == SUCCESS:
                gui.Simulate("Robot %s has moved from %s to %s\n" %(r, str(l1), str(l2)))
                self.state.loc[r] = l2
            else:
                gui.Simulate("Robot %s failed to move due to some internal failure.\n" %r)
        else:
            gui.Simulate("Robot %s is not in location %d.\n" %(r, l1))
            res = FAILURE
        self.state.loc.ReleaseLock(r)
        return res

    def moveCurved(self, r, l1, l2, dist):
        (x1, y1) = l1
        (x2, y2) = l2
        centrex = (x1 + x2)/2
        centrey = (y1 + y2)/2
        for o in self.rv.OBSTACLES:
            (ox, oy) = o
            r2 = (x2 - centrex)*(x2 - centrex) + (y2 - centrey)*(y2 - centrey)
            ro = (ox - centrex)*(ox - centrex) + (oy - centrey)*(oy - centrey)
            if abs(r2 - ro) <= 0.0001:
                gui.Simulate("%s cannot move in curved path because of obstacle\n" %r)
                return FAILURE

        self.state.loc.AcquireLock(r)
        if l1 == l2:
            gui.Simulate("Robot %s is already at location %s\n" %(r, l2))
            res = SUCCESS
        elif self.state.loc[r] == l1:
            start = globalTimer.GetTime()
            while(globalTimer.IsCommandExecutionOver('moveCurved', start, r, l1, l2, dist) == False):
               pass
            res = self.env.Sense('moveCurved')
            if res == SUCCESS:
                gui.Simulate("Robot %s has moved from %s to %s\n" %(r, str(l1), str(l2)))
                self.state.loc[r] = l2
            else:
                gui.Simulate("Robot %s failed to move due to some internal failure.\n" %r)
        else:
            gui.Simulate("Robot %s is not in location %d.\n" %(r, l1))
            res = FAILURE
        self.state.loc.ReleaseLock(r)
        return res

    def moveManhattan(self, r, l1, l2, dist):
        (x1, y1) = l1
        (x2, y2) = l2
        xlow = min(x1, x2)
        xhigh = max(x1, x2)
        ylow = min(y1, y2)
        yhigh = max(y1, y2)
        for o in self.rv.OBSTACLES:
            (ox, oy) = o
            if abs(oy - y1) <= 0.0001 and ox >= xlow and ox <= xhigh:
                gui.Simulate("%s cannot move in Manhattan path because of obstacle\n" %r)
                return FAILURE

            if abs(ox - x2) <= 0.0001 and oy >= ylow and oy <= yhigh:
                gui.Simulate("%s cannot move in Manhattan path because of obstacle\n" %r)
                return FAILURE

        self.state.loc.AcquireLock(r)
        if l1 == l2:
            gui.Simulate("Robot %s is already at location %s\n" %(r, l2))
            res = SUCCESS
        elif self.state.loc[r] == l1:
            start = globalTimer.GetTime()
            while(globalTimer.IsCommandExecutionOver('moveManhattan', start, r, l1, l2, dist) == False):
               pass
            res = self.env.Sense('moveManhattan')
            if res == SUCCESS:
                gui.Simulate("Robot %s has moved from %s to %s\n" %(r, str(l1), str(l2)))
                self.state.loc[r] = l2
            else:
                gui.Simulate("Robot %s failed to move due to some internal failure.\n" %r)
        else:
            gui.Simulate("Robot %s is not in location %d.\n" %(r, l1))
            res = FAILURE
        self.state.loc.ReleaseLock(r)
        return res

    def fly(self, r, l1, l2):
        self.state.loc.AcquireLock(r)
        if l1 == l2:
            gui.Simulate("Robot %s is already at location %s\n" %(r, l2))
            res = SUCCESS
        elif self.state.loc[r] == l1:
            start = globalTimer.GetTime()
            while(globalTimer.IsCommandExecutionOver('fly', start) == False):
               pass
            res = self.env.Sense('fly')
            if res == SUCCESS:
                gui.Simulate("Robot %s has flied from %s to %s\n" %(r, str(l1), str(l2)))
                self.state.loc[r] = l2
            else:
                gui.Simulate("Robot %s failed to fly due to some internal failure.\n" %r)
        else:
            gui.Simulate("Robot %s is not in location %d.\n" %(r, l1))
            res = FAILURE
        self.state.loc.ReleaseLock(r)
        return res

    def inspectPerson(self, r, p):
        gui.Simulate("Robot %s is inspecting person %s \n" %(r, p))
        self.state.status[p] = self.state.realStatus[p]
        return SUCCESS

    def giveSupportToPerson(self, r, p):
        if self.state.status[p] != 'dead':
            gui.Simulate("Robot %s has saved person %s \n" %(r, p))
            self.state.status[p] = 'OK'
            self.state.realStatus[p] = 'OK'
            res = SUCCESS
        else:
            gui.Simulate("Person %s is already dead \n" %(p))
            res = FAILURE
        return res

    def inspectLocation(self, r, l):
        gui.Simulate("Robot %s is inspecting location %s \n" %(r, str(l)))
        self.state.status[l] = self.state.realStatus[l]
        return SUCCESS

    def clearLocation(self, r, l):
        gui.Simulate("Robot %s has cleared location %s \n" %(r, str(l)))
        self.state.status[l] = 'clear'
        self.state.realStatus[l] = 'clear'
        return SUCCESS

    def replenishSupplies(self, r):
        self.state.hasMedicine.AcquireLock(r)
        if self.state.loc[r] == (1,1):
            self.state.hasMedicine[r] = 5
            gui.Simulate("Robot %s has replenished supplies at the base.\n" %r)
            res = SUCCESS
        else:
            gui.Simulate("Robot %s is not at the base.\n" %r)
            res = FAILURE

        self.state.hasMedicine.ReleaseLock(r)
        return res

    def transfer(self, r1, r2):
        self.state.hasMedicine.AcquireLock(r1)
        self.state.hasMedicine.AcquireLock(r2)
        if self.state.loc[r1] == self.state.loc[r2]:
            if self.state.hasMedicine[r1] > 0:
                self.state.hasMedicine[r2] += 1
                self.state.hasMedicine[r1] -= 1
                gui.Simulate("Robot %s has transferred medicine to %s.\n" %(r1, r2))
                res = SUCCESS
            else:
                gui.Simulate("Robot %s does not have medicines.\n" %r1)
                res = FAILURE
        else:
            gui.Simulate("Robots %s and %s are in different locations.\n" %(r1, r2))
            res = FAILURE
        self.state.hasMedicine.ReleaseLock(r2)
        self.state.hasMedicine.ReleaseLock(r1)
        return res

    def captureImage(self, r, camera, l):
        img = self.env.Sense('captureImage', r, camera, l)

        self.state.currentImage.AcquireLock(r)
        self.state.currentImage[r] = img
        gui.Simulate("UAV %s has captured image in location %s using %s\n" %(r, l, camera))
        self.state.currentImage.ReleaseLock(r)
        return SUCCESS

    def changeAltitude(self, r, newAltitude):
        self.state.altitude.AcquireLock(r)
        if self.state.altitude[r] != newAltitude:
            res = self.env.Sense('changeAltitude')
            if res == SUCCESS:
                self.state.altitude[r] = newAltitude
                gui.Simulate("UAV %s has changed altitude to %s\n" %(r, newAltitude))
            else:
                gui.Simulate("UAV %s was not able to change altitude to %s\n" %(r, newAltitude))
        else:
            res = SUCCESS
            gui.Simulate("UAV %s is already in %s altitude.\n" %(r, newAltitude))
        self.state.altitude.ReleaseLock(r)
        return res

    def SR_GETDISTANCE_Euclidean(self, l0, l1):
        (x0, y0) = l0
        (x1, y1) = l1
        return math.sqrt((x1 - x0)*(x1 - x0) + (y1 - y0)*(y1-y0))

    def MoveTo_Method1(self, r, l): # takes the straight path
        x = self.state.loc[r]
        if x == l:
            gui.Simulate("Robot %s is already in location %s\n." %(r, l))
        elif self.state.robotType[r] == 'wheeled':
            dist = self.SR_GETDISTANCE_Euclidean(x, l)
            gui.Simulate("Euclidean distance = %d " %dist)
            self.actor.do_command(self.moveEuclidean, r, x, l, dist)
        else:
            self.actor.do_command(self.fail)

    def SR_GETDISTANCE_Manhattan(self, l0, l1):
        (x1, y1) = l0
        (x2, y2) = l1
        return abs(x2 - x1) + abs(y2 - y1)

    def MoveTo_Method2(self, r, l): # takes a Manhattan path
        x = self.state.loc[r]
        if x == l:
            gui.Simulate("Robot %s is already in location %s\n." %(r, l))
        elif self.state.robotType[r] == 'wheeled':
            dist = self.SR_GETDISTANCE_Manhattan(x, l)
            gui.Simulate("Manhattan distance = %d " %dist)
            self.actor.do_command(self.moveManhattan, r, x, l, dist)
        else:
            self.actor.do_command(self.fail)

    def SR_GETDISTANCE_Curved(self, l0, l1):
        diameter = self.SR_GETDISTANCE_Euclidean(l0, l1)
        return math.pi * diameter / 2

    def MoveTo_Method3(self, r, l): # takes a curved path
        x = self.state.loc[r]
        if x == l:
            gui.Simulate("Robot %s is already in location %s\n." %(r, l))
        elif self.state.robotType[r] == 'wheeled':
            dist = self.SR_GETDISTANCE_Curved(x, l)
            gui.Simulate("Curved distance = %d " %dist)
            self.actor.do_command(self.moveCurved, r, x, l, dist)
        else:
            self.actor.do_command(self.fail)

    def MoveTo_Method4(self, r, l):
        x = self.state.loc[r]
        if x == l:
            gui.Simulate("Robot %s is already in location %s\n." %(r, l))
        elif self.state.robotType[r] == 'uav':
            self.actor.do_command(self.fly, r, x, l)
        else:
            self.actor.do_command(self.fail)

    def Rescue_Method1(self, r, p):
        if self.state.robotType[r] != 'uav':
            if self.state.hasMedicine[r] == 0:
                self.actor.do_task('getSupplies', r)
            self.actor.do_task('helpPerson', r, p)
        else:
            self.actor.do_command(self.fail)

    def Rescue_Method2(self, r, p):
        if self.state.robotType[r] == 'uav':
            self.actor.do_task('getRobot')
        r2 = self.state.newRobot[1]
        if r2 != None:
            if self.state.hasMedicine[r2] == 0:
                self.actor.do_task('getSupplies', r2)
            self.actor.do_task('helpPerson', r2, p)
            self.state.status[r2] = 'free'
        else:
            gui.Simulate("No robot is free to help person %s\n" %p)
            self.actor.do_command(self.fail)

    def HelpPerson_Method1(self, r, p):
        # help an injured person
        self.actor.do_task('moveTo', r, self.state.loc[p])
        self.actor.do_command(self.inspectPerson, r, p)
        if self.state.status[p] == 'injured':
            self.actor.do_command(self.giveSupportToPerson, r, p)
        else:
            self.actor.do_command(self.fail)

    def HelpPerson_Method2(self, r, p):
        # help a person trapped inside some debri but not injured
        self.actor.do_task('moveTo', r, self.state.loc[p])
        self.actor.do_command(self.inspectLocation, r, self.state.loc[r])
        if self.state.status[self.state.loc[r]] == 'hasDebri':
            self.actor.do_command(self.clearLocation, r, self.state.loc[r])
        else:
            self.CheckReal(self.state.loc[p])
            self.actor.do_command(self.fail)

    def GetSupplies_Method1(self, r):
        # get supplies from nearby robots
        r2 = None
        nearestDist = float("inf")
        for r1 in self.rv.WHEELEDROBOTS:
            if self.state.hasMedicine[r1] > 0:
                dist = self.SR_GETDISTANCE_Euclidean(self.state.loc[r], self.state.loc[r1])
                if dist < nearestDist:
                    nearestDist = dist
                    r2 = r1
        if r2 != None:
            self.actor.do_task('moveTo', r, self.state.loc[r2])
            self.actor.do_command(self.transfer, r2, r)

        else:
            self.actor.do_command(self.fail)

    def GetSupplies_Method2(self, r):
        # get supplies from the base
        self.actor.do_task('moveTo', r, (1,1))
        self.actor.do_command(self.replenishSupplies, r)

    def CheckReal(self, l):
        p = self.state.realPerson[l]
        if p != None:
            if self.state.realStatus[p] == 'injured' or self.state.realStatus[p] == 'dead' or self.state.realStatus[l] == 'hasDebri':
                gui.Simulate("Person in location %s failed to be saved.\n" %str(l))
                self.actor.do_command(self.deadEnd, p)
                self.actor.do_command(self.fail)

    def Survey_Method1(self, r, l):
        if self.state.robotType[r] != 'uav':
            self.actor.do_command(self.fail)

        self.actor.do_task('adjustAltitude', r)

        self.actor.do_command(self.captureImage, r, 'frontCamera', l)

        img = self.state.currentImage[r]
        position = img['loc']
        person = img['person']

        if person != None:
            self.actor.do_task('rescue', r, person)

        self.CheckReal(l)

    def Survey_Method2(self, r, l):
        if self.state.robotType[r] != 'uav':
            self.actor.do_command(self.fail)

        self.actor.do_task('adjustAltitude', r)

        self.actor.do_command(self.captureImage, r, 'bottomCamera', l)

        img = self.state.currentImage[r]
        position = img['loc']
        person = img['person']

        if person != None:
            self.actor.do_task('rescue', r, person)

        self.CheckReal(l)

    def GetRobot_Method1(self, ):
        dist = float("inf")
        robot = None
        for r in self.rv.WHEELEDROBOTS:
            if self.state.status[r] == 'free':
                if self.SR_GETDISTANCE_Euclidean(self.state.loc[r], (1,1)) < dist:
                    robot = r
                    dist = self.SR_GETDISTANCE_Euclidean(self.state.loc[r], (1,1))
        if robot == None:
            self.actor.do_command(self.fail)
        else:
            self.state.status[robot] = 'busy'
            self.state.newRobot[1] = robot   # Check if this can cause any regression with assignment self.statements

    def GetRobot_Method2(self, ):
        self.state.newRobot[1] = self.rv.WHEELEDROBOTS[0]
        self.state.status[self.rv.WHEELEDROBOTS[0]] = 'busy'

    def AdjustAltitude_Method1(self, r):
        if self.state.altitude[r] == 'high':
            self.actor.do_command(self.changeAltitude, r, 'low')

    def AdjustAltitude_Method2(self, r):
        if self.state.altitude[r] == 'low':
            self.actor.do_command(self.changeAltitude, r, 'high')

    def Heuristic2(self, args):
        r = args[0]
        lfinal = args[1]

        if lfinal == self.state.loc[r]:
            return float("inf")
        else:
            return 1/self.SR_GETDISTANCE_Euclidean(self.state.loc[r], lfinal)

    def Heuristic1(self, args):
        return float("inf")

class RescueEnv():
    def __init__(self, state, rv):
        self.commandProb = {
            'giveSupportToPerson': [0.9, 0.1],
            'clearLocation': [0.8, 0.2],
            'inspectPerson': [0.8, 0.2],
            'moveEuclidean': [0.95, 0.05],
            'moveCurved': [0.95, 0.05],
            'moveManhattan': [0.95, 0.05],
            'fly': [0.9, 0.1],
            'inspectLocation': [0.98, 0.02],
            'changeAltitude': [0.8, 0.2]
        }
        self.state = state
        self.rv = rv

    def Sense(self, cmd, *cmdArgs):
        if cmd == 'perceive':
            if GLOBALS.GetPlanningMode():
                return self.SenseObjects()
            else:
                return SUCCESS
        elif cmd == 'wait':
            if GLOBALS.GetPlanningMode():
                for r in self.rv.ROBOTS:
                    self.state.emergencyHandling[r] = False
        elif cmd == 'captureImage':
            return self.SenseImage(*cmdArgs)
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
            if not self.state.view[loc]:
                total += 1

        for o in self.rv.OBJECTS:
            prob = {}
            if self.state.pos[o] == UNK:
                for l in self.state.view:
                    if not self.state.view[l]:
                        prob[l] = 1/total
                p = list(prob.values())
                locs = list(prob.keys())
                locIndex = numpy.random.choice(len(p), 50, p=p)
                self.state.containers[locs[locIndex[0]]].append(o)

    def SenseImage(self, r, camera, l):
        img = {'loc': None, 'person': None}
        visibility = False
        if self.state.weather[l] == 'rainy':
            if camera == 'bottomCamera' and self.state.altitude[r] == 'low':
                visibility = True
        elif self.state.weather[l] == 'foggy':
            if camera == 'frontCamera' and self.state.altitude[r] == 'low':
                visibility = True
        elif self.state.weather[l] == 'dustStorm':
            if self.state.altitude[r] == 'low':
                visibility = True
        elif self.state.weather[l] == 'clear':
            visibility = True
        else:
            print("Invalid weather conditions. Please check problem file.\n")

        if visibility == True:
            img['loc'] = l
            img['person'] = self.state.realPerson[l]

        return img
