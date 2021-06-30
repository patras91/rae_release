__author__="patras"
from shared.state import State, RV
from actors.RAE.RAE import rae

class Setup():
    def __init__(self, domain, problem, actor, useLearningStrategy, planner, plannerParams, v, startState=None):
        if startState:
            self.state = startState
        else:
            self.state = State()
        self.rv = RV()
        assert(domain in [
                'fetch',
                'nav',
               'explore',
               'rescue',
               'deliver',
               'testInstantiation',
               'testSSU',
               'testMethodswithCosts',
               "AIRS", "AIRS_dev",
               'UnitTest',
               'Mobipick'])

        self.actor = rae(
            domain, 
            problem, 
            useLearningStrategy,
            planner, plannerParams, 
            v, 
            self.state, self.rv, self.RestoreState, self.GetDomainState)
        if domain == "fetch":
            from domains.fetch.domain_fetch import FetchDomain, FetchEnv
            self.env = FetchEnv(self.state, self.rv)
            self.domain = FetchDomain(self.state, self.rv, self.actor, self.env)
        elif domain == "AIRS_dev" or domain == "AIRS":
            from domains.AIRS.domain_AIRS import AIRSDomain, AIRSEnv
            self.env = AIRSEnv(self.state, self.rv)
            self.domain = AIRSDomain(self.state, self.rv, self.actor, self.env)
        elif domain == "Mobipick":
            from domains.mobipick.domain_mobipick import MobipickEnv, MobipickDomain
            self.env = MobipickEnv(self.state, self.rv)
            self.domain = MobipickDomain(self.state, self.rv, self.actor, self.env)
        elif domain == "UnitTest":
            from domains.UnitTest.domain_UnitTest import UnitTestDomain, UnitTestEnv
            self.env = UnitTestEnv(self.state, self.rv)
            self.domain = UnitTestDomain(self.state, self.rv, self.actor, self.env)
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