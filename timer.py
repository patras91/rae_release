__author__ = 'patras'

from time import time

class Duration():
    def __init__(self):
        pass

DURATION = Duration()
DURATION.TIME = {}
DURATION.COUNTER = {}

class Timer():
    def __init__(self):
        self.mode = 'Counter'
        self.now = 0 #Only used in counter mode

    def SetMode(self, m):
    #Specify whether to use clock or global counter to simulate the running state of commands
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

    def GetCounterValue(self):
        return self.now

    def IsCommandExecutionOver(self, cmd, start):
        if self.mode == 'Counter':
            if self.now - start < DURATION.COUNTER[cmd]:
                over = False
            else:
                over = True
        elif self.mode == 'Clock':
            if time() - start < DURATION.TIME[cmd]:
                over = False
            else:
                over = True

        return over

globalTimer = Timer()

def SetMode(m):
    globalTimer.SetMode(m)