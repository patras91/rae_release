import random
import math

class Map():
    def __init__(self, initIndex):
        if initIndex == 1:
            self.locations = ['base', 'z1', 'z2', 'z3', 'z4', 'z5', 'z6', 'z7']
            self.edges = {
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
        elif initIndex == 2:
            self.LOCATIONS = ['base', 'z1', 'z2', 'z3', 'z4', 'z5', 'z6', 'z7']
            self.EDGES = {
                'base': {
                    'z1': 15,
                    'z4': 215,
                    'z5': 35,
                    'z6': 35,
                    'z7': 35
                },
                'z1': {
                    'base': 15,
                    'z2': 90
                },
                'z2': {
                    'z1': 90,
                    'z3': 30
                },
                'z3': {
                    'z2': 30,
                    'z4': 90
                },
                'z4': {
                    'z3': 90,
                    'base': 215
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

        elif initIndex == 3:
            self.LOCATIONS = ['base', 'z1', 'z2', 'z3', 'z4']
            self.EDGES = {
                'base': {
                    'z1': 20,
                    'z2': 10,
                    'z3': 20,
                    'z4': 10
                },
                'z1': {
                    'base': 20,
                    'z2': 30,
                    'z4': 50
                },
                'z2': {
                    'base': 10,
                    'z1': 30,
                    'z3': 30
                },
                'z3': {
                    'base': 20,
                    'z2': 30,
                    'z4': 30
                },
                'z4': {
                    'base': 10,
                    'z3': 30,
                    'z1': 50
                }
            }

    def GetLocationsString(self):
        return "rv.LOCATIONS = " + str(self.locations) + "\n"

    def GetEdgesString(self):
        return "rv.EDGES = " + str(self.edges) + "\n"

MAPS = [Map(1), Map(2), Map(3)]

ChooseLocation(l):
    l1 = random.sample(l, 1)
    l2 = random.sample(l, 2)
    l3 = random.sample(l, 3)

def generateProblems():
    num = 1
    for map in MAPS: # 3 
        for loc in map.locations[1:3]: # 3
            for charge in range(60, 81, 20): # 2
                chargerLoc = ChooseLocation(map.locations) # 1
                locs = random.randint(1, len(map.locations)) # 3
                for weather in ['normal', 'stormy']: # 2
                    writeProblem(num, map, loc, charge, chargerLoc, locs, weather)
                    num += 1


def writeProblem(num, map, loc, charge, chargerLoc, locs, weather):
    
    fname = 'auto/problem{}_EE.py'.format(num)
    file = open(fname,"w") 
    writeHeader(file)

    file.write("rv.TYPE = {'e1': 'survey', 'e2': 'monitor', 'e3': 'screen', 'e4': 'sample', 'e5':'process'}")
    file.write("rv.EQUIPMENT = {'survey': 'e1', 'monitor': 'e2', 'screen': 'e3', 'sample': 'e4', 'process': 'e5'}")
    file.write(map.GetLocationsString())
    file.write(map.GetEdgesString())

    if chargerLoc == 'r2':
        file.write("rv.ROBOTS=['r1','r2']\n\n")
        locString = "    state.loc = {{'r1': {}, 'r2': {}}}\n".format(loc, 1)
        chargeString = "    state.charge = {{'r1': {}, 'r2': 3}}\n".format(charge)
        loadString = "    state.load = {'r1': NIL, 'r2': NIL}\n"
    else:
        file.write("rv.ROBOTS=['r1']\n\n")
        locString = "    state.loc = {{'r1': {}}}\n".format(loc)
        chargeString = "    state.charge = {{'r1': {}}}\n".format(charge)
        loadString = "    state.load = {'r1': NIL}\n"

    file.write("def ResetState():\n")
    file.write(locString)

    file.write(chargeString)
    
    file.write(loadString)

    if chargerLoc == 'r2':
        chargerLoc = '\'r2\''
    if pos == True:
        posString = "    state.pos = {{'c1': {}, 'o1': {}}}\n".format(chargerLoc, obj_loc)
    else:
        posString = "    state.pos = {{'c1': {}, 'o1': UNK}}\n".format(chargerLoc)

    file.write(posString)
    file.write(map.GetContainerString(obj_loc))

    file.write("    state.emergencyHandling = {'r1': False, 'r2': False}\n")
    
    file.write("'e1': 'base', 'e2': 'base', 'e3': 'base', 'e4': 'base', 'e5': 'base'}\n")
    if weather == 'normal':
        file.write("    state.storm = {'active': False}\n")
    elif weather == 'stormy':
        file.write("    state.storm = {'active': True}\n")

    file.write("tasks = {\n")

    time = random.randint(1, 8)
    #taskString = "    {}: [['fetch', 'r1', 'o1']],\n".format(time)

    #file.write(taskString)

    if emergency == True:
        emergencyString = "    {}: [['emergency', 'r1', 2, 1]],\n".format(time+2)
        file.write(emergencyString)
    file.write("}\n")
    
    file.write("eventsEnv = {\n")
    file.write("}")

    file.close() 

def writeHeader(file):
    file.write("__author__ = 'patras'\n")
    file.write("from domain_exploreEnv import *\n") 
    file.write("from timer import DURATION\n") 
    file.write("from state import state\n\n") 

    file.write("DURATION.TIME = {\n")
    file.write("    'survey': 5,\n") 
    file.write("    'monitor': 5,\n") 
    file.write("    'screen': 5,\n") 
    file.write("    'sample': 5,\n") 
    file.write("    'process': 5,\n") 
    file.write("    'fly': 3,\n") 
    file.write("    'deposit': 1,\n") 
    file.write("    'transferData': 1,\n") 
    file.write("    'take': 2,\n") 
    file.write("    'put': 2,\n") 
    file.write("    'move': 10,\n") 
    file.write("    'charge': 5,\n") 
    file.write("    'negotiate': 5,\n") 
    file.write("    'handleAlien': 5,\n") 
    file.write("}\n\n") 

    file.write("DURATION.COUNTER = {\n") 
    file.write("    'survey': 5,\n") 
    file.write("    'monitor': 5,\n") 
    file.write("    'screen': 5,\n") 
    file.write("    'sample': 5,\n") 
    file.write("    'process': 5,\n") 
    file.write("    'fly': 3,\n") 
    file.write("    'deposit': 1,\n") 
    file.write("    'transferData': 1,\n") 
    file.write("    'take': 2,\n") 
    file.write("    'put': 2,\n") 
    file.write("    'move': 10,\n") 
    file.write("    'charge': 5,\n") 
    file.write("    'negotiate': 5,\n") 
    file.write("    'handleAlien': 5,\n") 
    file.write("}\n\n") 

if __name__=="__main__":
    generateProblems()