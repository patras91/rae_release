__author__ = 'patras'

import multiprocessing

taskQueue = multiprocessing.Queue()
cmdStatusQueue = multiprocessing.Queue()
cmdStatusStack = {}
cmdExecQueue = multiprocessing.Queue()

cmdStackTable = {}

def AddToCommandStackTable(cmdid, stackid):
	cmdStackTable[cmdid] = stackid

def UpdateCommandStatus():
	while(cmdStatusQueue.empty() == False):
		(id, res, nextState) = cmdStatusQueue.get()
		stackid = cmdStackTable[id]
		cmdStatusStack[stackid] = (id, res, nextState)