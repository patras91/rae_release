__author__ = 'patras'

from domain_SDNdefence import *
from timer import DURATION
from state import state

DURATION.TIME = {
    'turnOnSwitch': 2,
    'turnOffSwitch': 2,
    'turnOnComponent': 5,
    'turnOffComponent': 5,
    'disconnect': 20,
 }

DURATION.COUNTER = {
    'turnOnSwitch': 2,
    'turnOffSwitch': 2,
    'turnOnComponent': 5,
    'turnOffComponent': 5,
    'disconnect': 20,
 }

rv.SWITCHES = {'n1': ['s1', 's2', 's3']}
rv.COMPONENTS = {'n1': ['c1', 'c2', 'c3']}

def ResetState():
    state.status = {
    'n1': 'bad', 
    's1': 'on', 
    's2': 'on', 
    's3': 'off', 
    'c1': 'off', 
    'c2': 'on', 
    'c3': 'on',
    }
    state.powerSource = {'n1': 'plug1'}

tasks = {
    1: [['defend', 'n1']],
}

eventsEnv = {
    #3: #
}