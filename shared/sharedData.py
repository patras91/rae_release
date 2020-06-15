__author__ = 'patras'

import multiprocessing

taskQueue = multiprocessing.Queue() # where the tasks come in
cmdExecQueue = multiprocessing.Queue() # where commands go out
cmdStatusQueue = multiprocessing.Queue() # where the status of commands come in
cmdStatusStack = {} # where the command statuses are saved after reading from cmdStatusQueue

cmdStackTable = {} # keeps track of which command belongs to which stack/job

# RAE updates which stack a new command belongs to 
def AddToCommandStackTable(cmdid, stackid):
	cmdStackTable[cmdid] = stackid

# RAE reads the cmdStatusQueue and updates the cmdStatusStack  
def UpdateCommandStatus():
	while(cmdStatusQueue.empty() == False):
		(id, res, nextState) = cmdStatusQueue.get()
		stackid = cmdStackTable[id]
		cmdStatusStack[stackid] = (id, res, nextState)