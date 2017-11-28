__author__ = 'patras'

from domain_ste import *
from timer import DURATION
from rae1 import state

DURATION.TIME = {
    'walk': 60,
    'call_taxi': 5,
    'enter_taxi': 5,
    'taxi_carry': 10,
    'pay_driver': 5,
    'leave_taxi': 5
 }

DURATION.COUNTER = {
    'walk': 60,
    'call_taxi': 5,
    'enter_taxi': 5,
    'taxi_carry': 10,
    'pay_driver': 5,
    'leave_taxi': 5
}

state.loc = {'Dana':'home', 'Paolo':'home', 'Malik':'home2', 'taxi':'home'}
state.cash = {'Dana':20, 'Paolo': 5, 'Malik': 100}
state.owe = {'Dana':0, 'Paolo': 0, 'Malik': 0}
state.dist = {'home':{'park': 8}, 'park':{'home': 8}, 'home2':{'park2': 80}, 'park2':{'home2': 80}}
state.occupied = {'taxi':False}

tasks = {
    1: ['travel', 'Malik', 'home2', 'park2']
}

eventsEnv = {}