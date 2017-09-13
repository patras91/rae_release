__author__ = 'patras'

from domain_simpleOpenDoor import *
from timer import DURATION
from rae1 import state

DURATION.TIME = {
    'moveBy': 3, # for domain SOD
    'pull': 2,
    'push': 3,
    'grasp': 1,
    'ungrasp': 1,
    'turn': 2,
    'moveClose': 3,
    'getStatus': 2,
 }

DURATION.COUNTER = {
    'moveBy': 3, # for domain SOD
    'pull': 2,
    'push': 3,
    'grasp': 1,
    'ungrasp': 1,
    'turn': 2,
    'moveClose': 3,
    'getStatus': 2,
 }

rv.ADJACENT = [(1, 'd1'), (2, 'd1'),(3, 'd2'), (4, 'd2')]
rv.TOWARDSIDE = [(2, 'd1'), (3, 'd2')]
rv.AWAYSIDE = [(1, 'd1'), (4, 'd2')]
rv.HANDLE = [('d1', 'o1'), ('d2', 'o2')]
rv.TYPE = [('d1', 'slides'), ('d2', 'rotates')]
rv.SIDE = [('d1', 'right'), ('d2', 'left')]

state.doorStatus = { 'd1':'unknown', 'd2':'unknown'}
state.loc = {'r1':2, 'r2':3}
state.reachable = {('r1','o1'):False, ('r2','o2'):False}

tasks = {
    1: ['openDoor', 'r1', 'd1', 'o1'],
    2: ['openDoor', 'r2', 'd2', 'o2']
}