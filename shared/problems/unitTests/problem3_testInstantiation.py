__author__ = 'patras'
from domain_testInstantiation import *
from timer import DURATION
from state import state

DURATION.COUNTER = {
    't1_c1': 5,
    't1_c2': 2,
}

rv.LOCATIONS = [
 1, 2, 3, 4]

rv.ROBOTS = [
 'r1', 'r2', 'r3']

def ResetState():
    state.loc = {'r1': 1, 'o1': 1}


tasks = {1: [['t3']]}

eventsEnv = {}