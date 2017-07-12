
from __future__ import print_function
#import domain_ste
import domain_simpleFetch
import domain_chargeableRobot
import threading
import sys

__author__ = 'patras'

NUMSTACKS = 1

class IpcArgs():
	""" IPCArgs is just a collection of variable bindings to share data among the processes."""
	def __init__(self):
		pass

#ste.ste_init()
#domain_simpleFetch.simpleFetch_init()
domain_chargeableRobot.chargeableRobot_init()

ipcArgs = IpcArgs()
ipcArgs.sem = threading.Semaphore(1)  #the semaphore to control progress of each stack and master
ipcArgs.nextStack = 0                 #the master thread is the next in line to be executed, which adds a new stack for every new task

threadList = []
#TODO: move the following to an incoming task stream
#threadList.append(threading.Thread(target = ste.ste_run_travel1, args=(ipcArgs, 1,)))
#threadList.append(threading.Thread(target = domain_simpleFetch.simpleFetch_run_1, args=(ipcArgs, 1,)))
threadList.append(threading.Thread(target = domain_chargeableRobot.chargeableRobot_run_1, args=(ipcArgs, 1,)))
threadList[0].start()
#threadList.append(threading.Thread(target = ste.ste_run_travel2, args=(ipcArgs, 2,)))
#threadList[1].start()
#threadList.append(threading.Thread(target = ste.ste_run_travel3, args=(ipcArgs, 3,)))
#threadList[2].start()

nextStack = 1

def GetNextAlive():
    nextAlive = -1
    i = 1
    j = nextStack
    print("nextStack initialized to %d" %nextStack)
    while i <= NUMSTACKS: #TODO: change this to the number of tasks
        if threadList[j-1].isAlive() == True:
            nextAlive = j
            break
        i = i + 1
        j = j % NUMSTACKS + 1

    return nextAlive

while (True):
    # TODO: Create a new thread for every incoming task stream
    if ipcArgs.nextStack == 0 or threadList[ipcArgs.nextStack-1].isAlive() == False:
        ipcArgs.sem.acquire()
        print("Acquired in master\n")
        res = GetNextAlive()
        if res != -1:
            ipcArgs.nextStack = res
            nextStack = res % NUMSTACKS + 1
            ipcArgs.sem.release()
        else:
            break