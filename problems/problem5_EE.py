__author__ = 'patras'

from domain_exploreEnv import *
from timer import DURATION
from rae1 import state

DURATION.TIME = {
    'survey': 5, # for domain EE
    'monitor': 5,
    'screen': 5,
    'sample': 5,
    'process': 5,
    'fly': 3,
    'deposit': 1,
    'transferData': 1,
    'take': 2,
    'put': 2,
    'move': 10,
    'charge': 5,
 }

DURATION.COUNTER = {
    'survey': 5, # for domain EE
    'monitor': 5,
    'screen': 1,
    'sample': 1,
    'process': 1,
    'fly': 3,
    'deposit': 1,
    'transferData': 1,
    'take': 2,
    'charge': 5,
    'put': 2,
    'move': 5,
 }

rv.TYPE = {'e1': 'survey', 'e2': 'monitor', 'e3': 'screen', 'e4': 'sample', 'e5':'process'}
rv.EQUIPMENT = {'survey': 'e1', 'monitor': 'e2', 'screen': 'e3', 'sample': 'e4', 'process': 'e5'}
rv.LOCATIONS = ['base', 'z1', 'z2', 'z3', 'z4', 'z5', 'z6', 'z7']
rv.EDGES = {
    'base': {
        'z1': 15,
        'z4': 15,
        'z5': 35,
        'z6': 35,
        'z7': 35
    },
    'z1': {
        'base': 15,
        'z2': 30
    },
    'z2': {
        'z1': 30,
        'z3': 30
    },
    'z3': {
        'z2': 30,
        'z4': 30
    },
    'z4': {
        'z3': 30,
        'base': 15
    },
    'z5': {
        'base': 35
    },
    'z6': {
        'base': 35
    },
    'z7': {
        'base': 35
    }
}

def ResetState():
    state.loc = {'r1': 'base', 'UAV': 'base', 'r2d2': 'base', 'bb8': 'base', 'c3po': 'base'}
    state.charge = {'r1':75, 'UAV': 75, 'r2d2': 100, 'bb8': 50, 'c3po': 100}
    state.data = {'r1': 0, 'UAV': 0, 'r2d2': 0, 'bb8': 0, 'c3po': 0}
    state.load = {'r1': NIL, 'UAV': NIL, 'r2d2': NIL, 'bb8': NIL, 'c3po': NIL}
    state.pos = {'c1': 'base', 'e1': 'base', 'e2': 'base', 'e3': 'base', 'e4': 'base', 'e5': 'base'}

tasks =  {
    1: ['explore', 'UAV', 'survey', 'z1'],
    2: ['explore', 'r2d2', 'sample', 'z4'],
    3: ['explore', 'r1', 'process', 'z5'],
    4: ['explore', 'bb8', 'screen', 'z2' ],
    5: ['explore', 'c3po', 'monitor', 'z1'],
    6: ['explore', 'c3po', 'monitor', 'z4']
}

eventsEnv = {}