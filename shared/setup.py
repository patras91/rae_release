__author__="patras"
from state import State, RV
from RAE import rae
from domain_fetch import FetchDomain, FetchEnv
from domain_AIRS import AIRSDomain, AIRSEnv

class Setup():
    def __init__(self, domain, problem, actor, planner, plannerParams, v, startState=None):
        self.state = State()
        self.rv = RV()
        self.actor = rae(domain, 
            problem, 
            planner, plannerParams, 
            v, 
            self.state, self.rv, self.RestoreState, self.GetDomainState)
        if domain == "fetch":
            self.env = FetchEnv(self.state, self.rv)
            self.domain = FetchDomain(self.state, self.rv, self.actor, self.env)
        elif domain == "AIRS_dev" or domain == "AIRS":
            self.env = AIRSEnv(self.state, self.rv)
            self.domain = AIRSDomain(self.state, self.rv, self.actor, self.env)

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