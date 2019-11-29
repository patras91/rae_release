__author__ = 'patras'
from domain_testInstantiation import *
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

rv.LOCATIONS = [
 1, 2, 3, 4]

rv.ROBOTS = [
 'r1', 'r2', 'r3']

def ResetState():
    state.v = {0: 1}

tasks = {
1: [['tbackup']]
}

eventsEnv = {}