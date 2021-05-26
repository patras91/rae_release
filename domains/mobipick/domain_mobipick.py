__author__ = 'patras'

'''Mobipick is moving in an indoor environment. 
The robot knows the map and waypoints.'''

from domains.constants import *
from shared import gui
from shared.timer import globalTimer, DURATION
from shared import GLOBALS # needed for heuristic (zero or domainSpecific), and for planning mode in environment
import numpy

DURATION.TIME = {
    'move': 5,
}

DURATION.COUNTER = {
    'move': 5,
}

class MobipickDomain():
    def __init__(self, state, rv, actor, env):
        # params:
        # state: the state the domain operates on
        # actor: needed for using actor.do_task and actor.do_command
        # env: the environment the domain gathers/senses information from

        self.state = state
        self.actor = actor
        self.env = env
        self.rv = rv
        actor.declare_commands([self.move, self.fail])

        actor.declare_task('nonEmergencyMove', 'r', 'l1', 'l2', 'dist')

        actor.declare_methods('nonEmergencyMove', self.NonEmergencyMove_Method1)

        if GLOBALS.GetHeuristicName() == 'zero':
            actor.declare_heuristic('nonEmergencyMove', self.Heuristic1)
        elif GLOBALS.GetHeuristicName() == 'domainSpecific':
            actor.declare_heuristic('nonEmergencyMove', self.Heuristic2)

    def fail(self,):
        return FAILURE

    def move(self, r, l1, l2, dist):
        self.state.loc.AcquireLock(r)
        if l1 == l2:
            gui.Simulate("Robot %s is already at location %s\n" %(r, l2))
            res = SUCCESS
        elif self.state.loc[r] == l1:
            start = globalTimer.GetTime()
            while not globalTimer.IsCommandExecutionOver('move', start):
                pass
            res = self.env.Sense('move')
            if res == SUCCESS:
                gui.Simulate("Robot %s has moved from %d to %d\n" %(r, l1, l2))
                self.state.loc[r] = l2
            else:
                gui.Simulate("Robot %s failed to move due to some internal failure\n" %r)
        else:
            gui.Simulate("Robot %s is not in location %d\n" %(r, l1))
            res = FAILURE
        self.state.loc.ReleaseLock(r)
        return res

    def NonEmergencyMove_Method1(self, r, l1, l2, dist):
        self.actor.do_command(self.move, r, l1, l2, dist)

    def Heuristic1(self, args):
        return float("inf")

    def Heuristic2(self, args):
        return 1


class MobipickEnv():
    def __init__(self, state, rv):
        self.commandProb = {
            'move': [0.95, 0.05],
        }
        self.state = state
        self.rv = rv

    def Sense(self, cmd):
        p = self.commandProb[cmd]
        outcome = numpy.random.choice(len(p), 50, p=p)
        res = outcome[0]
        if res == 0:
            return SUCCESS
        else:
            return FAILURE