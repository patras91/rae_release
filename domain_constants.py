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
LOCATIONS_CHARGEABLEROBOT = [1, 2, 3, 4, 5, 6, 7, 8]
EDGES_CHARGEABLEROBOT = {1: [7], 2: [8], 3: [8], 4: [8], 5: [7], 6: [7], 7:[1, 5, 6, 8], 8: [2, 3, 4, 7]}

# Using Dijsktra's algorithm
def GETDISTANCE(l0, l1):
    visitedDistances = {l0: 0}
    locs = list(LOCATIONS_CHARGEABLEROBOT)

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

        for l in EDGES_CHARGEABLEROBOT[min_loc]:
            dist = current_dist + 1
            if l not in visitedDistances or dist < visitedDistances[l]:
                visitedDistances[l] = dist

    return visitedDistances[l1]

#****************************************************************

#****************************************************************
#spring door example, with dynamic environment, domain_springDoor.py

LOCATIONS_SPRINGDOOR = [1, 2, 3, 4, 5, 6]
EDGES_SPRINGDOOR = {1: [4], 2: [5], 3: [6], 4: [1, 5], 5: [2, 4, 6], 6: [3, 5]}
DOORLOCATIONS_SPRINGDOOR = {(1, 4): 'd1', (2, 5): 'd2', (3, 6): 'd3'}

def GETDOOR_SPRINGDOOR(l1, l2):
    if (l1, l2) in DOORLOCATIONS_SPRINGDOOR:
        return DOORLOCATIONS_SPRINGDOOR[l1, l2]
    else:
        return DOORLOCATIONS_SPRINGDOOR[l2, l1]

# Using Dijsktra's algorithm
def GETPATH_SPRINGDOOR(l0, l1):
    visitedDistances = {l0: 0}
    locs = list(LOCATIONS_SPRINGDOOR)
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

        for l in EDGES_SPRINGDOOR[min_loc]:
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