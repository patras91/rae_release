__author__ = 'patras'
from domain_testInstantiation import *
from timer import DURATION
from state import state, rv

rv.LOCATIONS = [
 1, 2, 3, 4]

rv.ROBOTS = [
 'r1', 'r2', 'r3']

def ResetState():
    state.loc = {'r1': 1, 'o1': 1}


tasks = {1: [['t', 'o1']]}

eventsEnv = {}