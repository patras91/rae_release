__author__ = 'patras'
from domain_testSSU import *
from timer import DURATION
from state import state

DURATION.COUNTER = {
    'u1': 5,
    'u2': 2,
    'u3': 8,
    'u4': 40,
    'u5': 10,
    'u6': 10,
    'u7': 12,
}

def ResetState():
    state.v = {0: 1}

tasks = {
1: [['tbackup']]
}

eventsEnv = {}