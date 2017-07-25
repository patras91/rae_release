from __future__ import print_function
from timer import globalTimer
"""
File rae1.py
Author: Dana Nau <nau@cs.umd.edu>, July 7, 2017
Sunandita Patra <patras@cs.umd.edu>, July 9, 2017
This has multiple execution stacks
"""

import sys, pprint

############################################################
# States and goals

class State():
	"""A state is just a collection of variable bindings."""
	def __init__(self):
		pass

### A goal is identical to a state except for the class name.
### I don't know if we'll need it or not, but it was trivial to write,
### and it might be useful if we want to reason about goals.

class Goal():
	"""A goal is just a collection of variable bindings."""
	def __init__(self):
		pass


def print_state(depth=0):
	"""Print each variable in state, indented by depth spaces."""
	global state
	if state != False:
		for (name,val) in vars(state).items():
			print('   state.' + name + ' =', val)
	else: print('False')

def print_stack(stackid, depth):
	stackdepth = depth[stackid]
	print(' stack {}.{}:'.format(stackid,stackdepth),end=' '*stackdepth)

### Print_goal is identical to print_state except for the word 'goal'

def print_goal(goal, depth=0):
	"""Print each variable in goal, indented by indent spaces."""
	if goal != False:
		for (name,val) in vars(goal).items():
			print('	goal.' + name + ' =', val)
	else: print('False')

### for debugging

verbose = 0
state = State()

def verbosity(level):
	"""
	Specify how much debugging printout to produce:
	
	verbosity(0) makes Rae1 run silently; the only printout will be
	whatever the domain author has put into the commands and methods.
	
	verbosity(1) makes Rae1 print messages at the start and end, and
	print the name and args of each task and command.
	
	verbosity(2) makes Rae1 print a lot of stuff.
	"""
	
	global verbose
	verbose = level

############################################################
# Helper functions that may be useful in domain models

def forall(seq,cond):
	"""True if cond(x) holds for all x in seq, otherwise False."""
	for x in seq:
		if not cond(x): return False
	return True

def find_if(cond,seq):
	"""
	Return the first x in seq such that cond(x) holds, if there is one.
	Otherwise return None.
	"""
	for x in seq:
		if cond(x): return x
	return None

############################################################
# Functions to tell Rae1 what the commands and methods are

commands = {}
methods = {}

def declare_commands(*cmd_list):
	"""
	Call this after defining the commands, to tell Rae1 what they are. 
	cmd_list must be a list of functions, not strings.
	"""
	commands.update({cmd.__name__:cmd for cmd in cmd_list})
	return commands

def declare_methods(task_name,*method_list):
	"""
	Call this once for each task, to tell Rae1 what the methods are.
	task_name must be a string.
	method_list must be a list of functions, not strings.
	"""
	methods.update({task_name:list(method_list)})
	return methods[task_name]

############################################################
# The user can use these to see what the commands and methods are.

def print_commands(olist=commands):
	"""Print out the names of the commands"""
	print('commands:', ', '.join(olist))

def print_methods(mlist=methods):
	"""Print out a table of what the methods are for each task"""
	print('{:<14}{}'.format('TASK:','METHODS:'))
	for task in mlist:
		print('{:<14}'.format(task) + ', '.join([f.__name__ for f in mlist[task]]))

############################################################
# Stuff for debugging printout

depth = {}
depth_increment = 1

class Failed_command(Exception):
	pass

class Failed_task(Exception):
	pass

class Incorrect_return_code(Exception):
	pass

#****************************************************************
#Functions to control Progress of each stack step by step
class IpcArgs():
	""" IPCArgs is just a collection of variable bindings to share data among the processes."""
	def __init__(self):
		pass

ipcArgs = IpcArgs()

def BeginCriticalRegion(stackid):
	while(ipcArgs.nextStack != stackid):
		pass
	ipcArgs.sem.acquire()

def EndCriticalRegion():
	ipcArgs.nextStack = 0
	ipcArgs.sem.release()

#****************************************************************

############################################################
# The actual acting engine

def rae1(task, *args):
	"""
	Rae1 is the Rae actor with a single execution stack. The first argument is the name (which
	should be a string) of the task to accomplish, and args[0:-1] are the arguments for the task.
	The current stack is args[-1].
	"""
	# To Sunandita: I think it's getting unwieldy to have multiple unnamed args at the end of
	# the arglist. Perhaps put them before the args variable and give them names? --Dana
	#
	# To Dana: Only using the stackid at the end now. Removed other arguments which consisted of state
	# and thread communication parameters. They are now global variables --Sunandita

	stackid = args[-1]
	taskArgs = args[0:-1]

	global depth
	depth.update({stackid: 1})

	if verbose > 0:
		print('\n---- Rae1: Create stack {}, task {}{}\n'.format(stackid, task, taskArgs))

	BeginCriticalRegion(stackid)

	if verbose > 1:
		print_stack(stackid,depth)
		print('Initial state is:')
		print_state(depth[stackid])

	try:
		retcode = do_task(task, *args)
	except Failed_command,e:
		if verbose > 0:
			print_stack(stackid, depth)
			print('Failed command {}'.format(e))
		retcode = 'Failure'
	except Failed_task, e:
		if verbose > 0:
			print_stack(stackid, depth)
			print('Failed task {}'.format(e))
		retcode = 'Failure'
	else:
		pass
	if verbose > 1:
		print_stack(stackid, depth)
		print('Final state is:')
		print_state(depth[stackid])
	if verbose > 0:
		print("\n---- Rae1: Done with stack %d\n" %stackid)

	EndCriticalRegion()
	return retcode

def choose_candidate(candidates):
	return(candidates[0],candidates[1:])

def do_task(task, *args):
	"""
	This is the workhorse for rae1. The arguments are the same as for rae1.
	"""
	stackid = args[-1]
	taskArgs = args[0:-1]
	global depth

	if verbose > 0:
		print_stack(stackid,depth)
		print('Begin task {}{}'.format(task,taskArgs))
	depth.update({stackid: depth[stackid]+1})
	retcode = 'Failure'
	candidates = methods[task]
	while (retcode == 'Failure' and candidates != []):
		(m,candidates) = choose_candidate(candidates)
		if verbose > 0:
			print_stack(stackid, depth)
			print('Try method {}{}'.format(m.__name__,taskArgs))

		try:
			EndCriticalRegion()
			BeginCriticalRegion(stackid)
			if verbose > 0:
				print_stack(stackid, depth)
				print("Executing method {}{}".format(m.__name__, taskArgs))
			if verbose > 1:
				print_stack(stackid, depth)
				print('Current state is:'.format(stackid))
				print_state(depth[stackid])
			retcode = m(*args)
		except Failed_command,e:
			if verbose > 0:
				print_stack(stackid,depth)
				print('Failed command {}'.format(e))
			retcode = 'Failure'
		except Failed_task,e:
			if verbose > 0:
				print_stack(stackid,depth)
				print('Failed task {}'.format(e))
			retcode = 'Failure'
		else:
			pass

		if verbose > 1:
			print_stack(stackid,depth)
			print('{} for method {}{}'.format(retcode,m.__name__,taskArgs))

	depth.update({stackid: depth[stackid]-1})
	if retcode == 'Failure':
		raise Failed_task('{}{}'.format(task, taskArgs))
	elif retcode == 'Success':
		return retcode
	else:
		raise Incorrect_return_code('{} for {}{}'.format(retcode, task, taskArgs))


def do_command(cmd, *args):
	"""
	Perform command cmd(args). Last arg must be the current state
	"""

	stackid = args[-1]
	cmdArgs = args[0:-1]

	global depth
	depth.update({stackid: depth[stackid]+1})

	if verbose > 0:
		print_stack(stackid,depth)
		print('Begin command {}{}'.format(cmd.__name__,cmdArgs))

	start = globalTimer.GetTime()

	EndCriticalRegion()
	BeginCriticalRegion(stackid)

	while (globalTimer.IsCommandExecutionOver(cmd.__name__, start) == False):
		if verbose > 0:
			print_stack(stackid, depth)
			print('Command {}{} is running'.format( cmd.__name__, cmdArgs))
		EndCriticalRegion()
		BeginCriticalRegion(stackid)

	if verbose > 0:
		print_stack(stackid, depth)
	retcode = cmd(*cmdArgs)

	if verbose > 1:
		print_stack(stackid, depth)
		print('Command {}{} returned {}'.format( cmd.__name__, cmdArgs, retcode))
		print_stack(stackid, depth)
		print('Current state is')
		print_state(depth[stackid])

	depth.update({stackid: depth[stackid]-1})

	if retcode == 'Failure':
		raise Failed_command('{}{}'.format(cmd.__name__, cmdArgs))
	elif retcode == 'Success':

		EndCriticalRegion()
		BeginCriticalRegion(stackid)
		return retcode
	else:
		raise Incorrect_return_code('{} for {}{}'.format(retcode, cmd.__name__, cmdArgs))