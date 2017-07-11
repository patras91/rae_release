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