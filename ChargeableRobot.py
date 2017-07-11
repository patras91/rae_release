__author__ = 'patras'

'''A robot is searching for an object in the environment consisting of n locations.
It has a battery that needs to be recharged after some moves.
A move consumes 1/4 of the battery capacity.
Recharger is only at one location'''

from constants import *

def dist(x,y):
   return {
       (1,7):1,

   }[(x,y)]

# not checking the distance betwwen x and y explicitly
def moveOneStep(r, x, y, state):
    if state.loc[r] == x and state.charge[r] > 0:
        print("Robot has moved from %d to %d\n" %(x, y))
        state.loc = y
        return SUCCESS
    elif state.loc[r] != x and state.charge[r] > 0:
        print("Robot is not in location %d\n" %x)
        return FAILURE
    elif state.loc[r] == x and state.charge[r] == 0:
        print("Robot has no more charge to move :(\n")
        return FAILURE
    else:
        print("Robot is not at location %d and it doesn't have any charge!\n" %x)
        return FAILURE

def pickupObject(r, o, state):
    if state.loc[r] == state.loc[o]:
        print("Robot has picked up object %d" %o)
        state.loc[o] = r
        return SUCCESS
    elif state.loc[r] != state.loc[o]:
        print("Robot is not at object %d's location" %o)
        return FAILURE

def Find(r, o, state):
    return 1

def Fetch(r,o,state):
    Find(r, o, state)
    pickupObject(r, o, state)


