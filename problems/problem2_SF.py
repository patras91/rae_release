__author__ = 'patras'

from domain_simpleFetch import *
from timer import DURATION
from rae1 import state

DURATION.TIME = {
    'moveTo': 10, # for domain SF
    'addressEmergency': 15,
    'moveToEmergency': 5,
    'wait': 5,
    'perceive': 3,
    'take': 2,
 }

DURATION.COUNTER = {
    'moveTo': 10, # for domain SF
    'addressEmergency': 15,
    'moveToEmergency': 5,
    'wait': 5,
    'perceive': 3,
    'take': 2,
 }

rv.LOCATIONS = [1, 2, 3, 4, 5, 6]

state.loc = {'r1' : 1}
state.pos = {'o1' : UNK, 'o2': UNK}
state.load = {'r1' : NIL}
state.view = {}
state.containers = {1:[], 2:['o2'], 3:[], 4:[], 5:[], 6:['o1']}
for l in rv.LOCATIONS:
    state.view[l] = False
state.emergencyHandling = {'r1' : True}

tasks = {
    1: ['fetch', 'r1', 'o1']
}

eventsEnv = {}