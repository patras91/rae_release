from __future__ import print_function
import sys
"""
File ste.py
Author: Dana Nau <nau@cs.umd.edu>, July 7, 2017
Based roughly on the "travel from home to the park" example in my lectures,
but modified to have multiple levels of tasks.
"""

import copy
import rae1

def taxi_rate(dist):
	return (1.5 + 0.5 * dist)

def walk(a,x,y,state):
	if state.loc[a] == x:
		print('agent',a,'walks from',x,'to',y)
		state.loc[a] = y
		return 'Success'
	else:
		print('agent',a,"isn't at location",x)
	return 'Failure'

def call_taxi(a,x,state):
	print('a taxi appears at location',x)
	state.loc['taxi'] = x
	return 'Success'

def enter_taxi(a,state):
	if state.loc['taxi'] == state.loc[a]:
		print('agent',a,'enters taxi at location',state.loc[a])
		state.loc[a] = 'taxi'
		return 'Success'
	else:
		print("there's no taxi for agent",a,'to enter')
		return 'Failure'

def taxi_carry(a,y,state):
	if state.loc[a]=='taxi':
		x = state.loc['taxi']
		print('taxi carries agent',a,'from',x,'to',y)
		state.loc['taxi'] = y
		state.owe[a] = taxi_rate(state.dist[x][y])
		return 'Success'
	else:
		print('agent',a,"isn't in a taxi")
		return 'Failure'

def pay_driver(a,state):
	if state.cash[a] >= state.owe[a]:
		print('agent',a,'pays',state.owe[a],'to the taxi driver')
		state.cash[a] = state.cash[a] - state.owe[a]
		state.owe[a] = 0
		return 'Success'
	else:
		print('agent',a,'cannot pay',state.owe[a],'to the taxi driver')
		return 'Failure'

def leave_taxi(a,state):
	if state.loc[a]=='taxi':
		print('agent',a,'leaves taxi at location',state.loc['taxi'])
		state.loc[a] = state.loc['taxi']
		return 'Success'
	else:
		print('agent',a,"isn't in a taxi")
		return 'Failure'

def travel_by_foot(a,x,y,state,ipcArgs,stackid):
	if state.dist[x][y] <= 2:
		rae1.do_command(walk,a,x,y,state,ipcArgs,stackid)
		return 'Success'
	return 'Failure'

def travel_by_taxi(a,x,y,state,ipcArgs,stackid):
	if state.cash[a] >= taxi_rate(state.dist[x][y]):
		rae1.do_command(call_taxi,a,x,state,ipcArgs,stackid)
		rae1.do_task('ride_taxi',a,y,state,ipcArgs,stackid)
		return 'Success'
	else:
		print('agent',a,"has too little money for a taxi from",x,'to',y)
		return 'Failure'

def ride_taxi_method(a,y,state, ipcArgs,stackid):
	if state.dist[state.loc[a]][y] < 50:
		rae1.do_command(enter_taxi,a,state,ipcArgs,stackid)
		rae1.do_command(taxi_carry,a,y,state,ipcArgs,stackid)
		rae1.do_command(pay_driver,a,state,ipcArgs,stackid)
		rae1.do_command(leave_taxi,a,state,ipcArgs,stackid)
		return 'Success'
	else:
		print('the taxi driver is unwilling to drive to',y)
		print("%d task done \n" %stackid)
		return 'Failure'

def ste_init():
	rae1.declare_commands(walk, call_taxi, enter_taxi, taxi_carry, pay_driver, leave_taxi)
	print('')
	rae1.print_commands()
	rae1.declare_methods('travel', travel_by_foot, travel_by_taxi)
	rae1.declare_methods('ride_taxi', ride_taxi_method)
	print('')
	rae1.print_methods()
	print('\n*********************************************************')
	print("* Call rae1 on several problems using verbosity level 1.")
	print("* For a different amout of printout, try 0 or 2 instead.")
	print('*********************************************************')

	rae1.verbosity(1)

def ste_run_travel1(ipcArgs, stackid):
	state = rae1.State()
	state.loc = {'me':'home'}
	state.cash = {'me':20}
	state.owe = {'me':0}
	state.dist = {'home':{'park':8}, 'park':{'home':8}}

	print("in travel 1\n")
	sys.stdout.flush()
	rae1.rae1('travel','me','home','park',state, ipcArgs, stackid)

def ste_run_travel2(ipcArgs, stackid):
	state = rae1.State()
	state.loc = {'me':'home'}
	state.cash = {'me':5}
	state.owe = {'me':0}
	state.dist = {'home':{'park':8}, 'park':{'home':8}}

	print("in travel 2\n")
	sys.stdout.flush()
	rae1.rae1('travel','me','home','park',state, ipcArgs, stackid)

def ste_run_travel3(ipcArgs, stackid):
	state = rae1.State()
	state.loc = {'me':'home'}
	state.cash = {'me':100}
	state.owe = {'me':0}
	state.dist = {'home':{'park':80}, 'park':{'home':80}}

	print("in travel 3\n")
	sys.stdout.flush()
	rae1.rae1('travel','me','home','park',state, ipcArgs, stackid)
