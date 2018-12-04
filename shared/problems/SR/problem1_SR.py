__author__ = 'patras'

from domain_searchAndRescue import *
from timer import DURATION
from state import state

DURATION.TIME = {
    'put': 2, #for domain SR
    'take': 2,
    'perceive': 3,
    'charge': 5,
    'move': 10,
    'moveToEmergency': 10,
    'moveCharger': 5,
    'addressEmergency': 15,
    'wait': 5
 }

DURATION.COUNTER = {
    'put': 2, #for domain SR
    'take': 2,
    'perceive': 3,
    'charge': 5,
    'move': 10,
    'moveToEmergency': 10,
    'moveCharger': 5,
    'addressEmergency': 15,
    'wait': 5,
 }

rv.WHEELEDROBOTS = {'w1'}
rv.LARGEROBOTS = {'r1'}
rv.CHARGERS = {'c1'}

def ResetState():
    state.loc = {'r1': (1,1), 'w1': (1,1)}
    state.charge = {'w1':10, 'r1': 100}
    state.load = {'w1': NIL, 'r1': NIL}
    state.pos = {'c1': (1,1)} 
    state.busy = {'w1': False, 'r1': False}

tasks = {
    1: [['rescue', 'p1', (5,5)]]
}

eventsEnv = {
}