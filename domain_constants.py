__author__ = 'patras'

'''List of constants shared by all the domains'''

#****************************************************************
# for all commands
SUCCESS = 'Success'
FAILURE = 'Failure'
#****************************************************************

#****************************************************************
#for simple harbour domain, domain_simpleFetch.py
UNK = 'Unknown'
NIL = 'nil'
#****************************************************************

#****************************************************************
#for simple harbour domain, domain_simpleFetch.py and simple opendoor domain, domain_simpleOpenDoor.py
LOCATIONS = [1, 2, 3, 4, 5, 6]
#****************************************************************

#****************************************************************
#for the simple Open door domain, domain_simpleOpenDoor.py
#rigid relations
ADJACENT = [(1, 'd1'), (2, 'd1'),(3, 'd2'), (4, 'd2')]
TOWARDSIDE = [(2, 'd1'), (3, 'd2')]
AWAYSIDE = [(1, 'd1'), (4, 'd2')]
HANDLE = [('d1', 'o1'), ('d2', 'o2')]
TYPE = [('d1', 'slides'), ('d2', 'rotates')]
SIDE = [('d1', 'right'), ('d2', 'left')]
#****************************************************************

#****************************************************************
#chargeable robot domain, domain_chargeableRobot.py
CR_LOCATIONS = [1, 2, 3, 4, 5, 6, 7, 8]
CR_EDGES = {1: [7], 2: [8], 3: [8], 4: [8], 5: [7], 6: [7], 7:[1, 5, 6, 8], 8: [2, 3, 4, 7]}

# Using Dijsktra's algorithm
def CR_GETDISTANCE(l0, l1):
    visitedDistances = {l0: 0}
    locs = list(CR_LOCATIONS)

    while locs:
        min_loc = None
        for loc in locs:
            if loc in visitedDistances:
                if min_loc is None:
                    min_loc = loc
                elif visitedDistances[loc] < visitedDistances[min_loc]:
                    min_loc = loc

        if min_loc is None:
            break

        locs.remove(min_loc)
        current_dist = visitedDistances[min_loc]

        for l in CR_EDGES[min_loc]:
            dist = current_dist + 1
            if l not in visitedDistances or dist < visitedDistances[l]:
                visitedDistances[l] = dist

    return visitedDistances[l1]

#****************************************************************

#****************************************************************
#spring door example, with dynamic environment, domain_springDoor.py

SD_LOCATIONS = [1, 2, 3, 4, 5, 6]
SD_EDGES = {1: [4], 2: [5], 3: [6], 4: [1, 5], 5: [2, 4, 6], 6: [3, 5]}
SD_DOORLOCATIONS = {(1, 4): 'd1', (2, 5): 'd2', (3, 6): 'd3'}

def SD_GETDOOR(l1, l2):
    if (l1, l2) in SD_DOORLOCATIONS:
        return SD_DOORLOCATIONS[l1, l2]
    else:
        return SD_DOORLOCATIONS[l2, l1]

# Using Dijsktra's algorithm
def SD_GETPATH(l0, l1):
    visitedDistances = {l0: 0}
    locs = list(SD_LOCATIONS)
    path = {}

    while locs:
        min_loc = None
        for loc in locs:
            if loc in visitedDistances:
                if min_loc is None:
                    min_loc = loc
                elif visitedDistances[loc] < visitedDistances[min_loc]:
                    min_loc = loc

        if min_loc is None:
            break

        locs.remove(min_loc)
        current_dist = visitedDistances[min_loc]

        for l in SD_EDGES[min_loc]:
            dist = current_dist + 1
            if l not in visitedDistances or dist < visitedDistances[l]:
                visitedDistances[l] = dist
                path[l] = min_loc

    l = l1
    path2 = {}
    while l != l0:
        path2[path[l]] = l
        l = path[l]

    return path2
#****************************************************************

DURATION_TIME = {
    'walk': 60, #for domain STE
    'call_taxi': 5,
    'enter_taxi': 5,
    'taxi_carry': 10,
    'pay_driver': 5,
    'leave_taxi': 5,

    'put': 2, #for domain CR
    'take': 2,
    'perceive': 3,
    'charge': 5,
    'move': 10,
    'moveCharger': 5,

    'moveBy': 3, # for domain SOD
    'pull': 2,
    'push': 3,
    'grasp': 1,
    'ungrasp': 1,
    'turn': 2,
    'moveClose': 3,
    'getStatus': 2,

    'moveTo': 10, # for domain SF
    'addressEmergency': 15,
    'moveToEmergency': 5,
    'wait': 5,

    'openDoor': 5, #for domain SD
    'holdDoor': 2,
    'passDoor': 3,
    'releaseDoor': 2,
    'closeDoors': 3,

    'survey': 5, # for domain EE
    'monitor': 5,
    'screen': 5,
    'sample': 5,
    'process': 5,
    'fly': 3,
    'deposit': 1,
    'transferData': 1

}


DURATION_COUNTER = {
    'walk': 60, #for domain STE
    'call_taxi': 5,
    'enter_taxi': 5,
    'taxi_carry': 10,
    'pay_driver': 5,
    'leave_taxi': 5,

    'put': 2, #for domain CR
    'take': 2,
    'perceive': 3,
    'charge': 5,
    'move': 10,
    'moveCharger': 5,

    'moveBy': 3, # for domain SOD
    'pull': 2,
    'push': 3,
    'grasp': 1,
    'ungrasp': 1,
    'turn': 2,
    'moveClose': 3,
    'getStatus': 2,

    'moveTo': 10, # for domain SF
    'addressEmergency': 15,
    'moveToEmergency': 5,
    'wait': 5,

    'openDoor': 5, #for domain SD
    'holdDoor': 2,
    'passDoor': 3,
    'releaseDoor': 2,
    'closeDoors': 3,

    'survey': 5, # for domain EE
    'monitor': 5,
    'screen': 5,
    'sample': 5,
    'process': 5,
    'fly': 3,
    'deposit': 1,
    'transferData': 1,

    'paint': 5, # for domain IP
    'assemble': 5,
    'pack': 5,
}

#*******************************************************
# Constants for explore environment domain

EE_TYPE = {'e1': 'survey', 'e2': 'monitor', 'e3': 'screen', 'e4': 'sample', 'e5':'process'}
EE_EQUIPMENT = {'survey': 'e1', 'monitor': 'e2', 'screen': 'e3', 'sample': 'e4', 'process': 'e5'}
EE_LOCATIONS = ['base', 'z1', 'z2', 'z3', 'z4', 'z5', 'z6', 'z7']
EE_EDGES = {
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
# Using Dijsktra's algorithm
def EE_GETPATH(l0, l1):
    visitedDistances = {l0: 0}
    locs = list(EE_LOCATIONS)
    path = {}

    while locs:
        min_loc = None
        for loc in locs:
            if loc in visitedDistances:
                if min_loc is None:
                    min_loc = loc
                elif visitedDistances[loc] < visitedDistances[min_loc]:
                    min_loc = loc

        if min_loc is None:
            break

        locs.remove(min_loc)
        current_dist = visitedDistances[min_loc]

        for l in EE_EDGES[min_loc]:
            dist = current_dist + EE_EDGES[min_loc][l]
            if l not in visitedDistances or dist < visitedDistances[l]:
                visitedDistances[l] = dist
                path[l] = min_loc
    l = l1
    path2 = {}
    while l != l0:
        path2[path[l]] = l
        l = path[l]

    return path2

# Using Dijsktra's algorithm
def EE_GETDISTANCE(l0, l1):
    visitedDistances = {l0: 0}
    locs = list(EE_LOCATIONS)

    while locs:
        min_loc = None
        for loc in locs:
            if loc in visitedDistances:
                if min_loc is None:
                    min_loc = loc
                elif visitedDistances[loc] < visitedDistances[min_loc]:
                    min_loc = loc

        if min_loc is None:
            break

        locs.remove(min_loc)
        current_dist = visitedDistances[min_loc]

        for l in EE_EDGES[min_loc]:
            dist = current_dist + EE_EDGES[min_loc][l]
            if l not in visitedDistances or dist < visitedDistances[l]:
                visitedDistances[l] = dist

    return visitedDistances[l1]
#*******************************************************

#*******************************************************

#Constants for IP domain

IP_MACHINE_LOCATION = {'paint': 3, 'pack': 4, 'assemble': 8, 'input': 1, 'output': 11}
IP_LOCATIONS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
IP_EDGES = {1: [2], 2: [1, 3, 5], 3: [2, 4, 6], 4: [3, 7], 5: [2, 6, 8], 6: [3, 5, 7, 9], 7: [4, 6, 10], 8: [5, 9], 9: [6, 8, 10], 10: [7, 9, 11], 11: [10]}

# Using Dijsktra's algorithm
def IP_GETDISTANCE(l0, l1):
    visitedDistances = {l0: 0}
    locs = list(IP_LOCATIONS)

    while locs:
        min_loc = None
        for loc in locs:
            if loc in visitedDistances:
                if min_loc is None:
                    min_loc = loc
                elif visitedDistances[loc] < visitedDistances[min_loc]:
                    min_loc = loc

        if min_loc is None:
            break

        locs.remove(min_loc)
        current_dist = visitedDistances[min_loc]

        for l in IP_EDGES[min_loc]:
            dist = current_dist + IP_EDGES[min_loc][l]
            if l not in visitedDistances or dist < visitedDistances[l]:
                visitedDistances[l] = dist

    return visitedDistances[l1]

# Using Dijsktra's algorithm
def IP_GETPATH(l0, l1):
    visitedDistances = {l0: 0}
    locs = list(IP_LOCATIONS)
    path = {}

    while locs:
        min_loc = None
        for loc in locs:
            if loc in visitedDistances:
                if min_loc is None:
                    min_loc = loc
                elif visitedDistances[loc] < visitedDistances[min_loc]:
                    min_loc = loc

        if min_loc is None:
            break

        locs.remove(min_loc)
        current_dist = visitedDistances[min_loc]

        for l in IP_EDGES[min_loc]:
            dist = current_dist + IP_EDGES[min_loc][l]
            if l not in visitedDistances or dist < visitedDistances[l]:
                visitedDistances[l] = dist
                path[l] = min_loc
    l = l1
    path2 = {}
    while l != l0:
        path2[path[l]] = l
        l = path[l]

    return path2

def GetNewName():
    GetNewName.current += 1
    return 'TMPOBJECT' + GetNewName.current.__str__()

GetNewName.current = 0

IP_ROBOTS = ['r1', 'r2']