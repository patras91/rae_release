__author__ = 'patras'

from time import time
import GLOBALS

class Duration():
    def __init__(self):
        pass

DURATION = Duration()
DURATION.TIME = {}
DURATION.COUNTER = {}

class Timer():
    def __init__(self):
        self.mode = 'Counter'
        self.simCount = 0
        self.realCount = 0

    def SetMode(self, m):
    # Specify whether to use clock or global counter to simulate the running state of commands
        self.mode = m
        if m == 'Counter':
            self.simCount = 0
            self.realCount = 0
        elif self.mode == 'Clock':
            pass
        else:
            print("Invalid mode. Set mode to either 'Counter' or 'Clock'")

    def IncrementTime(self):
        if self.mode == 'Counter':
            mode = GLOBALS.GetPlanningMode()
            if mode == False:
                self.realCount += 1
            else:
                self.simCount += 1

    #def Callibrate(self, startTime):
    #    if self.mode == 'Counter':
    #        secsPerTick = (time() - startTime) / self.now
    #        print("Ticks per second is ", 1 / secsPerTick)

    def IsCommandExecutionOver(self, cmd, start):
        mode = GLOBALS.GetPlanningMode()
        if mode == False:
            if self.mode == 'Counter':
                self.realCount += DURATION.COUNTER[cmd]
                return True
            elif self.mode == 'Clock':
                if time() - start < DURATION.TIME[cmd]:
                    over = False
                else:
                    over = True
            return over
        else:
            self.simCount += 1
            return True

    def GetSimulationCounter(self):
        return self.simCount

    def GetRealCommandExecutionCounter(self):
        return self.realCount

    def UpdateSimCounter(self, step):
        self.simCount += step

    def ResetSimCounter(self):
        self.simCount = 0

    def GetTime(self):
        mode = GLOBALS.GetPlanningMode()
        if mode == False:
            return self.realCount
        else:
            return self.simCount

globalTimer = Timer()

def SetMode(m):
    globalTimer.SetMode(m)