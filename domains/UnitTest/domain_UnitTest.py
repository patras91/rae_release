__author__ = 'patras'

'''Set of all Unit Tests'''

from domains.constants import *
from shared import gui
from shared.timer import globalTimer
from shared import GLOBALS # needed for heuristic (zero or domainSpecific), and for planning mode in environment
import numpy

class UnitTestDomain():
    def __init__(self, state, rv, actor, env):
        # params:
        # state: the state the domain operates on
        # the state object containing only rigid variables
        # actor: needed for do_task and do_command
        # env: the environment the domain gathers/senses information from

        self.state = state
        self.actor = actor
        self.env = env
        self.rv = rv
        actor.declare_commands([self.a1, self.fail])

        actor.declare_task('testRAEretry')
        actor.declare_task('testRAEretry_a')
        actor.declare_task('testRAEretry_b')

        actor.declare_methods('testRAEretry', self.RAEretry_Method1, self.RAEretry_Method2)
        actor.declare_methods('testRAEretry_a', self.RAEretry_a_Method1, self.RAEretry_a_Method2)
        actor.declare_methods('testRAEretry_b', self.RAEretry_b_Method1)

    def a1(self):
        return SUCCESS

    def fail(self):
        return FAILURE

    def RAEretry_Method1(self, ):
        self.actor.do_task('testRAEretry_a')
        self.actor.do_task('testRAEretry_b')

    def RAEretry_Method2(self, ):
        self.actor.do_command(self.a1)

    def RAEretry_a_Method1(self, ):
        self.actor.do_command(self.a1)

    def RAEretry_a_Method2(self, ):
        self.actor.do_command(self.a1)

    def RAEretry_b_Method1(self, ):
        self.actor.do_command(self.fail)

class UnitTestEnv():
    def __init__(self, state, rv):
        self.commandProb = {
        }
        self.state = state
        self.rv = rv

    def Sense(self, cmd):
        pass
