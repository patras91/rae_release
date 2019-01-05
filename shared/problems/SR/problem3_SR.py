__author__ = 'patras'

from domain_searchAndRescue import *
from timer import DURATION
from state import state

def GetCostOfMove(r, l1, l2, dist):
    return dist

DURATION.COUNTER = {
    'giveSupportToPerson': 15,
    'clearLocation': 5,
    'inspectPerson': 20,
    'moveEuclidean': GetCostOfMove,
    'moveCurved': GetCostOfMove,
    'moveManhattan': GetCostOfMove,
    'fly': 15,
    'inspectLocation': 5,
 }

DURATION.COUNTER = {
    'giveSupportToPerson': 15,
    'clearLocation': 5,
    'inspectPerson': 20,
    'moveEuclidean': GetCostOfMove,
    'moveCurved': GetCostOfMove,
    'moveManhattan': GetCostOfMove,
    'fly': 15,
    'inspectLocation': 5,
 }


rv.WHEELEDROBOTS = {'w1'}
rv.LARGEROBOTS = {'r1'}
rv.OBSTACLES = {(2.5, 2.5), (2,1)}

def ResetState():
    state.loc = {'r1': (1,1), 'w1': (1,1)}
    state.robotType = {'r1': 'large', 'w1': 'wheeled'}

tasks = {
    1: [['moveTo', 'r1', (5,5)]]
}

eventsEnv = {
}