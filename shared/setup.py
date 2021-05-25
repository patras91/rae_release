__author__="patras"
from shared.state import State, RV
from actors.RAE.RAE import rae
from domains.fetch.domain_fetch import FetchDomain, FetchEnv
from domains.AIRS.domain_AIRS import AIRSDomain, AIRSEnv
from domains.UnitTest.domain_UnitTest import UnitTestDomain, UnitTestEnv

class Setup():
    def __init__(self, domain, problem, actor, useLearningStrategy, planner, plannerParams, v, startState=None):
        self.state = State()
        self.rv = RV()
        self.actor = rae(
            domain, 
            problem, 
            useLearningStrategy,
            planner, plannerParams, 
            v, 
            self.state, self.rv, self.RestoreState, self.GetDomainState)
        if domain == "fetch":
            self.env = FetchEnv(self.state, self.rv)
            self.domain = FetchDomain(self.state, self.rv, self.actor, self.env)
        elif domain == "AIRS_dev" or domain == "AIRS":
            self.env = AIRSEnv(self.state, self.rv)
            self.domain = AIRSDomain(self.state, self.rv, self.actor, self.env)
        elif domain == "UnitTest":
            self.env = UnitTestEnv(self.state, self.rv)
            self.domain = UnitTestDomain(self.state, self.rv, self.actor, self.env)
        if startState:
            self.actor.RestoreState(startState)
        self.declare_goals()

    def declare_goals(self):
        pass
        # TODO
        # for g in [...]:
        #   goalState = ...
        #   goalMethod = ...   
        #   self.actor.declare_goal_method(method, goalState)


    def RestoreState(self, s2):
        self.state.restore(s2)

    def GetDomainState(self):
        return self.state