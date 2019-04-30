import numpy
from domain_constants import *
from domain_springDoor import rv
from state import state

commandProb = {
    'turnOnSwitch': [0.8, 0.2],
    'turnOffSwitch': [0.9, 0.1],
    'turnOnComponent': [0.7, 0.3],
    'turnOffComponent': [0.8, 0.2],
    'disconnect': [0.9, 0.1],
}

def Sense(cmd, d=None):
    p = commandProb[cmd]
    outcome = numpy.random.choice(len(p), 50, p=p)
    res = outcome[0]
    if res == 0:
        return SUCCESS
    else:
        return FAILURE