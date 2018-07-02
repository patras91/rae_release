__author__ = 'patras'

from time import time
import globals

class Duration():
    def __init__(self):
        pass

DURATION = Duration()
DURATION.TIME = {}
DURATION.COUNTER = {}

class Timer():
    def __init__(self):
        self.mode = 'Counter'
        self.now = 0 # Only used in counter mode
        self.simCount = 0
        self.realCount = 0

    def SetMode(self, m):
    # Specify whether to use clock or global counter to simulate the running state of commands
        self.mode = m
        if m == 'Counter':
            self.now = 0
            self.simCount = 0
            self.realCount = 0
        elif self.mode == 'Clock':
            pass
        else:
            print("Invalid mode. Set mode to either 'Counter' or 'Clock'")

    def IncrementTime(self):
        if self.mode == 'Counter':
            self.now += 1
            mode = globals.GetPlanningMode()
            if mode == False:
                self.realCount += 1
            else:
                self.simCount += 1

    def GetTime(self):
        if self.mode == 'Counter':
            return self.now
        else:
            return time()

    def Callibrate(self, startTime):
        if self.mode == 'Counter':
            secsPerTick = (time() - startTime) / self.now
            print("Ticks per second is ", 1 / secsPerTick)

    def GetCounterValue(self):
        return self.now

    def IsCommandExecutionOver(self, cmd, start):
        mode = globals.GetPlanningMode()
        if mode == False:
            mult = 1  # This is the approx callibrated value
        else:
            mult = 1
        if self.mode == 'Counter':
            if self.now - start < DURATION.COUNTER[cmd] * mult:
                over = False
            else:
                over = True
        elif self.mode == 'Clock':
            if time() - start < DURATION.TIME[cmd]:
                over = False
            else:
                over = True

        return over

    def GetSimulationCounter(self):
        return self.simCount

    def GetRealCommandExecutionCounter(self):
        return self.realCount

    def UpdateSimCounter(self, step):
        self.simCount += step

    def ResetSimCounter(self):
        self.simCount = 0

globalTimer = Timer()

def SetMode(m):
    globalTimer.SetMode(m)