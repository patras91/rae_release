__author__ = 'patras' # Sunandita Patra patras@umd.edu

'''
This file shows how to use RAE and RAEplan.
Check the usage of the following methods:

	# verbosity may be 0, 1, 2 the level of terminal debugging output
	# startState: Initial State of the SDN network
	InitializeSecurityDomain(verbosity, startState)

	# How to create a new task?
	# enqueue it in the task queue with its params
	taskQ.put([task, args...])

	# cmd is the command the security manager needs to execute
	# args: arguments of the cmd
	# id: a unique identifier for the command
	[id, cmd, args] = cmdExecQ.get()

	# cmdStatus can be 'Success' or 'Failure'
	# id: id of the command you are taking about
	cmdStatusQ.put([id, cmdStatus, currentState])
'''

from testRAEandRAEplan import InitializeSecurityDomain
from state import State, state # the State class and the acting state
from domain_airsSDN import * # import the domain file
import time
import threading

# define some controllers
c_alt1 = Controller('alt-1', 'Debian', 'Java2', 'OpenDaylight', '1.15.0')
c_alt2 = Controller('alt-2', 'Fedora', 'Java', 'ONOS', '1.15.0')
c_alt3 = Controller('alt-3', 'Ubuntu', 'Java', 'OpenDaylight', 'hydrogen')
c_alt4 = Controller('alt-4', 'Ubuntu', 'Java', 'ONOS', '1.12.0')

# Create 2 controllers, c1 and c2 with alternatives
c1 = Controller('c1', 'Ubuntu', 'Java', 'ONOS', '1.12.0',
            trust=1.0, health=1.0,
            alternatives=[{'instance': c_alt1}, {'instance': c_alt3},
                          {'instance': c_alt4}])
c2 = Controller('c2', 'Debian', 'Java', 'OpenDaylight', 'Oxygen-SR3',
                    trust=1.0, health=1.0,
                    alternatives=[{'instance': c_alt1}, {'instance': c_alt2},
                                  {'instance': c_alt3}])

def ExecuteCmds(cmdExecQ, cmdStatusQ):
	while(True):
		if cmdExecQ.empty() == False:
			[id, cmd, args] = cmdExecQ.get()
			# You may execute the command in whatever way you want.
			# I am just executing the functions in the domain description.
			# Feel free to change this.
			# This is just to show how to use the command execution 
			# queue and the command status queue
			t = threading.Thread(target=cmd,args=args)
			time.sleep(5)
			t.start()
			t.join(5)
			cmdStatusQ.put([id, 'Success', state])

if __name__ == "__main__":
	

	state.controllers = {c2.id: c2, c1.id: c1}

	# InitializeSecurityDomain(verbosity, startState) 
	# verbosity may be 0, 1, 2 the level of terminal debugging output
	# startState: Initial State of the SDN network
	taskQ, cmdExecQ, cmdStatusQ = InitializeSecurityDomain(1, state) # returns a tuple of queues

	taskQ.put(['recover', c2.id])
	time.sleep(5)
	taskQ.put(['recover', c1.id])

	cmdExecutionThread = threading.Thread(target=ExecuteCmds, args=(cmdExecQ, cmdStatusQ))
	cmdExecutionThread.start()


