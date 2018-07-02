__author__ = 'patras'

from domain_test import *
from timer import DURATION
from state import state

DURATION.TIME = {
    'c1': 1,
    'c2': 2,
    'c3': 3
 }

DURATION.COUNTER = {
    'c1': 1,
    'c2': 2,
    'c3': 3
}

def ResetState():
    state.value = {'a': 0}

tasks = {
    1: ['t1'],
}

eventsEnv = {}
