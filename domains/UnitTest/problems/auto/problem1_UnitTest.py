__author__ = 'patras'
from domains.UnitTest.domain_UnitTest import *
from shared.timer import DURATION

DURATION.TIME = {
    'a1': 2,
}

DURATION.COUNTER = {
    'a1': 2,
}

def SetInitialStateVariables(state, rv):
    pass

tasks = {
    3: [['testRAEretry']],
}
eventsEnv = {
}