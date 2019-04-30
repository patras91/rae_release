# uncompyle6 version 3.3.1
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.2 (v3.6.2:5fd33b5926, Jul 16 2017, 20:11:06) 
# [GCC 4.2.1 (Apple Inc. build 5666) (dot 3)]
# Embedded file name: ../../shared/problems/CR/problem1056_CR.py
# Compiled at: 2019-03-13 17:18:47
# Size of source mod 2**32: 1153 bytes
__author__ = 'patras'
from domain_chargeableRobot import *
from timer import DURATION
from state import state
DURATION.TIME = {'put':2, 
 'take':2, 
 'perceive':3, 
 'charge':5, 
 'move':10, 
 'moveToEmergency':5, 
 'moveCharger':15, 
 'addressEmergency':10, 
 'wait':5}
DURATION.COUNTER = {'put':2, 
 'take':2, 
 'perceive':3, 
 'charge':5, 
 'move':10, 
 'moveToEmergency':5, 
 'moveCharger':15, 
 'addressEmergency':10, 
 'wait':5}
rv.LOCATIONS = [
 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
rv.EDGES = {1:[7],  2:[8],  3:[8],  4:[8, 9],  5:[7],  6:[7],  7:[1, 5, 6, 8],  8:[2, 3, 4, 7],  9:[4, 10],  10:[9]}
rv.OBJECTS = ['o1']
rv.ROBOTS = [
 'r1']

def ResetState():
    state.loc = {'r1': 1}
    state.charge = {'r1': 2}
    state.load = {'r1': NIL}
    state.pos = {'c1':1,  'o1':2}
    state.containers = {1:[],  2:['o1'],  3:[],  4:[],  5:[],  6:[],  7:[],  8:[],  9:[],  10:[]}
    state.emergencyHandling = {'r1':False,  'r2':False}
    state.view = {}
    for l in rv.LOCATIONS:
        state.view[l] = False


tasks = {6:[
  [
   'fetch', 'r1', 'o1']], 
 8:[
  [
   'emergency', 'r1', 2, 1]]}
eventsEnv = {}
# okay decompiling __pycache__/problem1056_CR.cpython-36.pyc
