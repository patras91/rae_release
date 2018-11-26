__author__ = 'patras'

from domain_springDoor import *
from timer import DURATION
from state import state

#
#   _______________________________________
#  |      |      |        |       |   r2  |
#  |      |      |    r1  |    o1 |       |
#  |   5  d1  2  |    3   |   4   d2  6   |
#  |      |      |        |       |       |
#  |______|______|___d3___|_______|_______|
#                |        |
#                |   1    |  
#                |     o2 | 
#                |________| 

DURATION.TIME = {
    'unlatch1': 5, #for domain SD
    'unlatch2': 5, #for domain SD
    'holdDoor': 2,
    'passDoor': 3,
    'releaseDoor': 2,
    'closeDoors': 3,
    'move': 10,
    'take': 2,
    'put': 2,
 }

DURATION.COUNTER = {
    'unlatch1': 5, #for domain SD
    'unlatch2': 5, #for domain SD
    'holdDoor': 2,
    'passDoor': 3,
    'releaseDoor': 2,
    'closeDoors': 3,
    'move': 10,
    'take': 2,
    'put': 2,
 }


rv.LOCATIONS = [1, 2, 3, 4, 5, 6]
rv.EDGES = {
    1: [3],
    2: [3, 5],
    3: [1, 2, 4],
    4: [6, 3],
    5: [2],
    6: [4]
}
rv.DOORLOCATIONS = {(4, 6): 'd2', (2, 5): 'd1', (1, 3): 'd3'}
rv.ROBOTS = ['r1', 'r2']
rv.DOORS = ['d1', 'd2', 'd3']
rv.DOORTYPES = { 'd1': 'spring', 'd2': 'spring', 'd3': 'spring'}

def ResetState():
    state.load = {'r1': NIL, 'r2': NIL}
    state.doorStatus = {'d1': 'closed', 'd2': 'closed', 'd3': 'closed'}
    state.loc = {'r1': 3, 'r2': 6}
    state.pos = {'o1': 4, 'o2': 1}
    state.done = {0: False}
    state.doorType = {'d1': UNK, 'd2': UNK, 'd3': UNK}

tasks = {
    5: [['fetch', 'r1', 'o1', 5]],
}

eventsEnv = {
   # 5: [closeDoors, []]
}