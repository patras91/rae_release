__author__ = 'patras'

'''List of constants shared by all the domains'''

# for all commands
SUCCESS = 'Success'
FAILURE = 'Failure'

#for simple harbour domain, simpleFetch.py
UNK = 'Unknown'
NIL = 'nil'
OBJECTS = ['o1']

#for simple harbour domain, simpleFetch.py and simple opendoor domain, simpleOpenDoor.py
LOCATIONS = [1, 2, 3, 4, 5, 6]
ROBOTS = ['r1']

#for thesimpleOpendoor domain, simpleOpenDoor.py
#rigid relations
ADJACENT = [(1, 'd1'), (2, 'd1'),(3, 'd2'), (4, 'd2')]
TOWARDSIDE = [(2, 'd1'), (3, 'd2')]
AWAYSIDE = [(1, 'd1'), (4, 'd2')]
HANDLE = [('d1', 'o1'), ('d2', 'o2')]
TYPE = [('d1', 'slides'), ('d2', 'rotates')]
SIDE = [('d1', 'right'), ('d2', 'left')]

#chargeable robot domain, ChargeableRobot.py
LOCATIONS2 = [1, 2, 3, 4, 5, 6, 7, 8]
EDGES = {1: [7], 2: [8], 3: [8], 4: [8], 5: [7], 6: [7], 7:[1, 5, 6, 8], 8: [2, 3, 4, 7]}

def GETDISTANCE(l0, l1):
    visitedDistances = {l0: 0}
    locs = list(LOCATIONS2)

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

        for l in EDGES[min_loc]:
            dist = current_dist + 1
            if l not in visitedDistances or dist < visitedDistances[l]:
                visitedDistances[l] = dist

    return visitedDistances[l1]

#spring door example, with dynamic environment, SpringDoor.py
