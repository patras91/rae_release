__author__ = 'patras'

from domains.domain_IndustryPlant import *
from timer import DURATION
from rae1 import state

DURATION.TIME = {
    'paint': 5, # for domain IP
    'assemble': 5,
    'pack': 5,
    'move': 10,
    'take': 2,
    'put': 2,
 }

DURATION.COUNTER = {
    'paint': 5, # for domain IP
    'assemble': 5,
    'pack': 5,
    'move': 10,
    'take': 2,
    'put': 2,
 }

rv.MACHINE_LOCATION = {'paint': 3, 'pack': 4, 'assemble': 8, 'input': 1, 'output': 11}
rv.LOCATIONS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
rv.EDGES = {1: [2], 2: [1, 3, 5], 3: [2, 4, 6], 4: [3, 7], 5: [2, 6, 8], 6: [3, 5, 7, 9], 7: [4, 6, 10], 8: [5, 9], 9: [6, 8, 10], 10: [7, 9, 11], 11: [10]}
rv.ROBOTS = ['r1', 'r2']

state.load = {'r1': NIL, 'r2': NIL}
state.loc = {'r1': 2, 'r2': 4}
state.status = {'r1': 'free', 'r2': 'free', 'paint': 'free', 'assemble': 'free', 'pack': 'free'}
state.pos = {'a': rv.MACHINE_LOCATION['input'], 'b': rv.MACHINE_LOCATION['input'], 'c': rv.MACHINE_LOCATION['input'], 'o1': rv.MACHINE_LOCATION['input']}

tasks = {
    1: ['order', ['pack', ['paint', 'o1', 'white'], ['assemble', ['assemble', 'a', 'b'], 'c']]],
    2: ['order', ['assemble', 'a1', ['paint', ['assemble', 'b1', 'c1'], 'pink']]]
}