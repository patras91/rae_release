__author__ = 'patras'

from domain_IndustryPlant import *
from timer import DURATION
from rae1 import state

#------------------------|
# input|     |     |pck1 |
#   1  |  2  |  3  |  4  |
#______|___r1|_____|_____|
#      |p1   |     |     |
#      |  5  |  6  |  7  |
#      |___r2|_____|___w1|______
#      |     |     |     |output
#      |  8  |  9  |  10 |  11
#      |___a1|r4_p2|___r3|______

def square(init, edge):
    (x, y) = init
    l = [[(x, y), (x + edge, y)], [(x, y), (x, y + edge)],
        [(x + edge, y), (x + edge, y + edge)], [(x, y + edge), (x + edge, y + edge)]]
    return l

rv.MAP = {
    1: square((0, 20), 10),
    2: square((10, 20), 10),
    3: square((20, 20), 10),
    4: square((30, 20), 10),
    5: square((10, 10), 10),
    6: square((20, 10), 10),
    7: square((30, 10), 10),
    8: square((10, 0), 10),
    9: square((20, 0), 10),
    10: square((30, 0), 10),
    11: square((40, 0), 10),
}

DURATION.TIME = {
    'paint': 5, # for domain IP
    'assemble': 5,
    'pack': 5,
    'move': 10,
    'take': 2,
    'put': 2,
    'wrap': 3,
    'damage': 1,
    'repair': 5
 }

DURATION.COUNTER = {
    'paint': 5, # for domain IP
    'assemble': 5,
    'pack': 5,
    'move': 10,
    'take': 2,
    'put': 2,
    'wrap': 3,
    'damage': 1,
    'repair': 5
 }


rv.MACHINE_LOCATION = {'p1': 5, 'pck1': 4, 'a1': 8, 'p2': 9, 'w1': 7}
rv.MACHINES = {'paint': ['p1', 'p2'], 'pack': ['pck1'], 'assemble': ['a1'], 'wrap': ['w1']}
rv.BUFFERS = {'input': 1, 'output': 11}
rv.LOCATIONS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
rv.EDGES = {1: [2], 2: [1, 3, 5], 3: [2, 4, 6], 4: [3, 7], 5: [2, 6, 8], 6: [3, 5, 7, 9], 7: [4, 6, 10], 8: [5, 9], 9: [6, 8, 10], 10: [7, 9, 11], 11: [10]}
rv.ROBOTS = ['r1', 'r2', 'r3', 'r4']

def ResetState():
    state.load = {'r1': NIL, 'r2': NIL, 'r3': NIL, 'r4': NIL}
    state.loc = {'r1': 2, 'r2': 5, 'r3': 10, 'r4': 9}
    state.status = {'r1': 'free', 'r2': 'free', 'r3': 'free', 'r4': 'free', 'p1': 'free', 'a1': 'free', 'pck1': 'free', 'p2': 'free', 'w1': 'free'}
    state.pos = {
        'a': rv.BUFFERS['input'],
        'b': rv.BUFFERS['input'],
        'c': rv.BUFFERS['input'],
        'o1': rv.BUFFERS['input'],
        'o2': rv.BUFFERS['input'],
        'o3': rv.BUFFERS['input'],
        'o4': rv.BUFFERS['input'],
        'o5': rv.BUFFERS['input'],
        'o6': rv.BUFFERS['input'],
    }
    state.cond = {'p1': OK, 'pck1': OK, 'a1': OK, 'p2': OK, 'w1': OK}

tasks = {
    1: ['order', ['paint', ['pack', 'o1', 'o2'], 'red']],
    2: ['order', ['pack', 'a1', ['assemble', 'b1', 'c1']]],
    3: ['order', ['wrap', ['pack', 'o3', 'o4']]],
    7: ['order', ['assemble', ['paint', 'o5', 'green'], 'o6']]
}

eventsEnv = {
    5: [damage, ['p1', 'pck1']],
    20: [damage, ['p2', 'a1']],
    30: [damage, ['w1', 'p1']],
    50: [damage, ['p2', 'pck1']]
}