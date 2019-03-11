import random
import math
import numpy as np


def generateProblems():
    num = 11
    while num < 30:
        locations = list(range(max(2, int(np.random.normal(20, 5)))))
        factory = frozenset(locations)
        shippingDoc = int(np.random.uniform(0, len(locations) - 1))
        locations.append(200)

        edges = {}

        # set up the edges s.t. the graph is connected
        for loc in locations:
            currEdges = []

            for loc2 in locations:
                if loc != loc2 and loc2 != 200:
                    if np.random.uniform() < 2/len(locations):
                        currEdges.append(loc2)

            if len(currEdges) == 0:
                if loc == 0:
                    currEdges.append(1)
                else:
                    currEdges.append(0)

            edges[loc] = currEdges

        weights = {}


        # make the edges undirected
        for loc in edges.keys():
            for dest in edges[loc]:
                if loc not in edges[dest]:
                    edges[dest].append(loc)

        # need to gen weights for all edges (i,j), i<j
        for loc in edges.keys():
            for dest in edges[loc]:
                if loc < dest:
                    weights[(loc, dest)] = max(1, np.random.normal(8,4))


        # set up robots
        robots = []
        robotCapacity = {}

        maxCapacity = 0

        for i in range(max(1, int(np.random.normal(10, 5)))):
            r = 'r' + str(i)
            robots.append(r)
            robotCapacity[r] = np.random.normal(8,2)

            if robotCapacity[r] > maxCapacity:
                maxCapacity = robotCapacity[r]

        # machines
        machines = []
        for i in range(min(len(locations) - 1, max(int(np.random.normal(5,5)), 1))):
            m = 'm' + str(i)
            machines.append(m)

        # fixer robot
        repairBots = []
        for i in range(max(1, int(np.random.normal(2,1)))):
            f = 'fixer' + str(i)
            repairBots.append(f)

        # objects
        objects = []
        obj_weight = {}
        obj_class = {}

        for typeNum in range(max(1, int(np.random.normal(5,1)))):
            type = 'type' + str(typeNum)
            tempType = []

            for i in range(max(1, int(np.random.normal(5,2)))):
                obj = 'o' + str(len(objects))
                objects.append(obj)
                obj_weight[obj] = min(maxCapacity, np.random.normal(7,2))

                tempType.append(obj)

            obj_class[type] = tempType

        # note: need to list that the objs are UNK when printing
        stateLoc = {}

        for r in robots:
            stateLoc[r] = np.random.choice(list(factory))
        for m in machines:
            stateLoc[m] = np.random.choice(list(factory))
        for f in repairBots:
            stateLoc[f] = np.random.choice(list(factory))

        storedLoc = {}
        for o in objects:
            storedLoc[o] = np.random.choice(list(factory))

        busy = {}
        for a in stateLoc.keys():
            busy[a] = False

        numUses = {}
        for m in machines:
            numUses[m] = max(1, int(np.random.normal(10,3)))

        orderTypes = []

        for oc in obj_class.keys():
            for i in range(max(0, min(len(obj_class[oc]), int(np.random.uniform(0,10))))):
                orderTypes.append(oc)

        if orderTypes == []:
            orderTypes.append('type0')

        writeProblem(num, locations, factory, shippingDoc, edges, weights, robots,
                     robotCapacity, machines, repairBots, objects, obj_weight,
                     obj_class, stateLoc, storedLoc, busy, numUses, orderTypes)

        num += 1


def writeProblem(num, locations, factory, shippingDoc, edges, weights, robots,
                 robotCapacity, machines, repairBots, objects, obj_weight,
                 obj_class, stateLoc, storedLoc, busy, numUses, orderTypes):
    fname = 'problem{}_OF.py'.format(num)
    file = open(fname, "w")
    writeHeader(file)


    file.write("rv.LOCATIONS = " + str(locations) + '\n')
    file.write("rv.FACTORY1 = " + str(factory) + '\n')
    file.write("rv.FACTORY_UNION = rv.FACTORY1\n")
    file.write("rv.SHIPPING_DOC = {rv.FACTORY1: " + str(shippingDoc)+ "}\n\n")

    file.write("rv.GROUND_EDGES = " + str(edges) + '\n')
    file.write("rv.GROUND_WEIGHTS = " + str(weights) + '\n\n')

    # rv.Robots things
    robotString = "rv.ROBOTS = {"
    for r in robots:
        robotString += " '" + r + "': rv.FACTORY1, "
    robotString += "}\n"

    file.write(robotString)

    file.write("rv.ROBOT_CAPACITY = " + str(robotCapacity) + '\n')

    # rv.MACHINES things
    machineString = "rv.MACHINES = {"
    for m in machines:
        machineString += " '" + m + "': rv.FACTORY1, "
    machineString += "}\n"

    file.write(machineString)

    # rv.REPAIR_BOT things
    repairString = "rv.REPAIR_BOT = {"
    for r in repairBots:
        repairString += " '" + r + "': rv.FACTORY1, "
    repairString += "}\n\n"

    file.write(repairString)

    file.write("rv.OBJECTS = " + str(objects) + '\n')
    file.write("rv.OBJ_WEIGHT = " + str(obj_weight) + '\n')
    file.write("rv.OBJ_CLASS = " + str(obj_class) + '\n\n')

    file.write("def ResetState():\n")

    stateLocString = "    state.loc = {"
    # state.loc things

    for r in stateLoc.keys():
        stateLocString += " '" + r + "': " + str(stateLoc[r]) + ","
    for o in objects:
        stateLocString += " '" + o + "': UNK,"
    stateLocString += "}\n"

    file.write(stateLocString)

    file.write("    state.storedLoc = " + str(storedLoc) + '\n')

    # state.load things

    stateLoadString = "    state.load = {"

    for r in robots:
        stateLoadString += " '" + r + "': NIL,"
    for f in repairBots:
        stateLoadString += " '" + f + "': False,"

    stateLoadString += "}\n"

    file.write(stateLoadString)
    file.write("    state.busy = " + str(busy) + '\n')
    file.write("    state.numUses = " + str(numUses) + '\n')

    file.write("    state.var1 = {'temp': 'r0', 'temp1': 'r0', 'temp2': 1, 'redoId': 0}\n")
    file.write("    state.shouldRedo = {}\n\n")

    file.write("tasks = {\n")

    randTimes = random.sample(range(1,2*len(orderTypes)), len(orderTypes))

    # how many tasks you want
    i = 0
    num_tasks = 2

    for idx, o in enumerate(orderTypes):
        if i < num_tasks:
            time = randTimes[idx]
            file.write("    " + str(time) + ": [['order', '" + str(o) + "', 200]],\n")
            i += 1
    file.write("}\n")

    file.write("eventsEnv = {\n")
    file.write("}")

    file.close()


def writeHeader(file):
    file.write("__author__ = 'mason'\n")
    file.write("from domain_orderFulfillment import *\n")
    file.write("from timer import DURATION\n")
    file.write("from state import state\n")
    file.write("import numpy as np\n\n")

    file.write("def GetCostOfMove(id, r, loc1, loc2, dist):\n")
    file.write("    return 1 + dist\n\n")

    file.write("def GetCostOfLookup(id, item):\n")
    file.write("    return max(1, np.random.beta(2, 2))\n\n")

    file.write("def GetCostOfWrap(id, m, item):\n")
    file.write("    return max(1, np.random.normal(5, .5))\n\n")

    file.write("def GetCostOfPickup(id, r, item):\n")
    file.write("    return max(1, np.random.normal(4, 1))\n\n")

    file.write("def GetCostOfPutdown(id, r, item):\n")
    file.write("    return max(1, np.random.normal(4, 1))\n\n")

    file.write("def GetCostOfLoad(id, r, m, item):\n")
    file.write("    return max(1, np.random.normal(3, .5))\n\n")


    file.write("DURATION.TIME = {\n")
    file.write("    'lookupDB': GetCostOfLookup,\n")
    file.write("    'wrap': GetCostOfWrap,\n")
    file.write("    'pickup': GetCostOfPickup,\n")
    file.write("    'putdown': GetCostOfPutdown,\n")
    file.write("    'acquireRobot': 1,\n")
    file.write("    'freeRobot': 1,\n")
    file.write("    'loadMachine': GetCostOfLoad,\n")
    file.write("    'moveRobot': GetCostOfMove,\n")
    file.write("    'repair': 5,\n")
    file.write("    'wait': 1\n")
    file.write("}\n\n")

    file.write("DURATION.COUNTER = {\n")
    file.write("    'lookupDB': GetCostOfLookup,\n")
    file.write("    'wrap': GetCostOfWrap,\n")
    file.write("    'pickup': GetCostOfPickup,\n")
    file.write("    'putdown': GetCostOfPutdown,\n")
    file.write("    'acquireRobot': 1,\n")
    file.write("    'freeRobot': 1,\n")
    file.write("    'loadMachine': GetCostOfLoad,\n")
    file.write("    'moveRobot': GetCostOfMove,\n")
    file.write("    'repair': 5,\n")
    file.write("    'wait': 1\n")
    file.write("}\n\n")



if __name__ == "__main__":
    generateProblems()