__author__ = 'patras'

from domain_constants import *
from time import time

class Timer():
    def __init__(self):
        self.mode = 'Counter'
        self.now = 0 #Only used in counter mode

    def SetMode(self, m):
	"""
	Specify whether to use clock or global counter to simulate the running state of commands
	"""
        self.mode = m
        if m == 'Counter':
            self.now = 0
        elif self.mode == 'Clock':
            pass
        else:
            print("Invalid mode. Set mode to either 'Counter' or 'Clock'")

    def IncrementTime(self):
        if self.mode == 'Counter':
            self.now += 1

    def GetTime(self):
        if self.mode == 'Counter':
            return self.now
        else:
            return time()

    def IsCommandExecutionOver(self, cmd, start):
        if self.mode == 'Counter':
		    if self.now - start < DURATION_COUNTER[cmd]:
			    over = False
		    else:
			    over = True
        elif self.mode == 'Clock':
            if time() - start < DURATION_TIME[cmd]:
                over = False
            else:
                over = True

        return over

globalTimer = Timer()

def SetMode(m):
    globalTimer.SetMode(m)