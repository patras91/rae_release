
from __future__ import print_function
import domain_ste
import domain_simpleFetch
import domain_chargeableRobot
import domain_simpleOpenDoor
import domain_springDoor

import threading
import sys

__author__ = 'patras'

class IpcArgs():
	""" IPCArgs is just a collection of variable bindings to share data among the processes."""
	def __init__(self):
		pass

def GetNextAlive(nextStack, NUMSTACKS, threadList):
    nextAlive = -1
    i = 1
    j = nextStack
    while i <= NUMSTACKS: #TODO: change this to the number of tasks
        if threadList[j-1].isAlive() == True:
            nextAlive = j
            break
        i = i + 1
        j = j % NUMSTACKS + 1

    return nextAlive

def testRAE(domain):

    ipcArgs = IpcArgs()
    ipcArgs.sem = threading.Semaphore(1)  #the semaphore to control progress of each stack and master
    ipcArgs.nextStack = 0                 #the master thread is the next in line to be executed, which adds a new stack for every new task

    threadList = []
    if domain == 'SF':
        domain_simpleFetch.simpleFetch_init()
        threadList.append(threading.Thread(target = domain_simpleFetch.simpleFetch_run_1, args=(ipcArgs, 1,)))
        threadList.append(threading.Thread(target = domain_simpleFetch.simpleFetch_run_2, args=(ipcArgs, 2,)))
        threadList.append(threading.Thread(target = domain_simpleFetch.simpleFetch_run_3, args=(ipcArgs, 3,)))
        NUMSTACKS = 3
    elif domain == 'CR':
        domain_chargeableRobot.chargeableRobot_init()
        threadList.append(threading.Thread(target = domain_chargeableRobot.chargeableRobot_run_1, args=(ipcArgs, 1,)))
        threadList.append(threading.Thread(target = domain_chargeableRobot.chargeableRobot_run_2, args=(ipcArgs, 2,)))
        NUMSTACKS = 2
    elif domain == 'STE':
        domain_ste.ste_init()
        #TODO: move the following to an incoming task stream
        threadList.append(threading.Thread(target = domain_ste.ste_run_travel1, args=(ipcArgs, 1,)))
        threadList.append(threading.Thread(target = domain_ste.ste_run_travel2, args=(ipcArgs, 2,)))
        threadList.append(threading.Thread(target = domain_ste.ste_run_travel3, args=(ipcArgs, 3,)))
        NUMSTACKS = 3
    elif domain == 'SOD':
        domain_simpleOpenDoor.simpleOpenDoor_init()
        threadList.append(threading.Thread(target = domain_simpleOpenDoor.simpleOpenDoor_run_1, args=(ipcArgs, 1,)))
        threadList.append(threading.Thread(target = domain_simpleOpenDoor.simpleOpenDoor_run_2, args=(ipcArgs, 2,)))
        NUMSTACKS = 2
    elif domain == 'SD':
        domain_springDoor.springDoor_init()
        threadList.append(threading.Thread(target = domain_springDoor.springDoor_run_1, args=(ipcArgs, 1,)))
        threadList.append(threading.Thread(target = domain_springDoor.springDoor_run_2, args=(ipcArgs, 2,)))
        NUMSTACKS = 2
    else:
        print("Invalid domain\n")
        return

    for i in range(0, NUMSTACKS):
        threadList[i].start()
    nextStack = 1

    while (True):
        # TODO: Create a new thread for every incoming task stream
        if ipcArgs.nextStack == 0 or threadList[ipcArgs.nextStack-1].isAlive() == False:
            ipcArgs.sem.acquire()
            print("Control acquired by master\n")
            res = GetNextAlive(nextStack, NUMSTACKS, threadList)
            if res != -1:
                ipcArgs.nextStack = res
                nextStack = res % NUMSTACKS + 1
                ipcArgs.sem.release()
            else:
                break