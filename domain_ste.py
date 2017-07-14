from __future__ import print_function
import sys
from domain_constants import *
"""
File ste.py
Author: Dana Nau <nau@cs.umd.edu>, July 7, 2017
Based roughly on the "travel from home to the park" example in my lectures,
but modified to have multiple levels of tasks.

Sunandita: Updated the test cases to test RAE
"""

import copy
import rae1

def taxi_rate(dist):
	return (1.5 + 0.5 * dist)

def walk(a,x,y,state):
	if state.loc[a] == x:
		print('agent',a,'walks from',x,'to',y,'\n')
		sys.stdout.flush()
		state.loc[a] = y
		return SUCCESS
	else:
		print('agent',a,"isn't at location",x,'\n')
		sys.stdout.flush()
	return FAILURE

def call_taxi(a,x,state):
	print('a taxi appears at location',x,'\n')
	sys.stdout.flush()
	state.loc['taxi'] = x
	return SUCCESS

def enter_taxi(a,state):
	if state.loc['taxi'] == state.loc[a]:
		print('agent',a,'enters taxi at location',state.loc[a],'\n')
		sys.stdout.flush()
		state.loc[a] = 'taxi'
		return SUCCESS
	else:
		print("there's no taxi for agent",a,'to enter','\n')
		sys.stdout.flush()
		return FAILURE

def taxi_carry(a,y,state):
	if state.loc[a]=='taxi':
		x = state.loc['taxi']
		print('taxi carries agent',a,'from',x,'to',y,'\n')
		sys.stdout.flush()
		state.loc['taxi'] = y
		state.owe[a] = taxi_rate(state.dist[x][y])
		return SUCCESS
	else:
		print('agent',a,"isn't in a taxi",'\n')
		sys.stdout.flush()
		return FAILURE

def pay_driver(a,state):
	if state.cash[a] >= state.owe[a]:
		print('agent',a,'pays',state.owe[a],'to the taxi driver','\n')
		sys.stdout.flush()
		state.cash[a] = state.cash[a] - state.owe[a]
		state.owe[a] = 0
		return SUCCESS
	else:
		print('agent',a,'cannot pay',state.owe[a],'to the taxi driver','\n')
		sys.stdout.flush()
		return FAILURE

def leave_taxi(a,state):
	if state.loc[a]=='taxi':
		print('agent',a,'leaves taxi at location',state.loc['taxi'],'\n')
		sys.stdout.flush()
		state.loc[a] = state.loc['taxi']
		return SUCCESS
	else:
		print('agent',a,"isn't in a taxi",'\n')
		sys.stdout.flush()
		return FAILURE

def travel_by_foot(a,x,y,state,ipcArgs,stackid):
	if state.dist[x][y] <= 2:
		rae1.do_command(walk,a,x,y,state,ipcArgs,stackid)
		return SUCCESS
	return FAILURE

def travel_by_taxi(a,x,y,state,ipcArgs,stackid):
	if state.cash[a] >= taxi_rate(state.dist[x][y]):
		rae1.do_command(call_taxi,a,x,state,ipcArgs,stackid)
		rae1.do_task('ride_taxi',a,y,state,ipcArgs,stackid)
		return SUCCESS
	else:
		print('agent',a,"has too little money for a taxi from",x,'to',y,'\n')
		sys.stdout.flush()
		return FAILURE

def ride_taxi_method(a,y,state, ipcArgs,stackid):
	if state.dist[state.loc[a]][y] < 50:
		rae1.do_command(enter_taxi,a,state,ipcArgs,stackid)
		rae1.do_command(taxi_carry,a,y,state,ipcArgs,stackid)
		rae1.do_command(pay_driver,a,state,ipcArgs,stackid)
		rae1.do_command(leave_taxi,a,state,ipcArgs,stackid)
		return SUCCESS
	else:
		print('the taxi driver is unwilling to drive to',y,'\n')
		sys.stdout.flush()
		return FAILURE

def ste_init():
	rae1.declare_commands(walk, call_taxi, enter_taxi, taxi_carry, pay_driver, leave_taxi)
	print('')
	rae1.print_commands()
	rae1.declare_methods('travel', travel_by_foot, travel_by_taxi)
	rae1.declare_methods('ride_taxi', ride_taxi_method)
	print('')
	rae1.print_methods()
	print('\n*********************************************************')
	print("* Call rae1 on simple travel using verbosity level 1.")
	print("* For a different amout of printout, try 0 or 2 instead.")
	print('*********************************************************')
	sys.stdout.flush()

	state = rae1.State()
	state.loc = {'Dana':'home', 'Paolo':'home', 'Malik':'home2'}
	state.cash = {'Dana':20, 'Paolo': 5, 'Malik': 100}
	state.owe = {'Dana':0, 'Paolo': 0, 'Malik': 0}
	state.dist = {'home':{'park':8}, 'park':{'home':8}, 'home2':{'park2':80}, 'park2':{'home2':80}}
	rae1.verbosity(0)

	return state

def ste_run_travel1(state, ipcArgs, stackid):
	rae1.rae1('travel','Dana','home','park',state, ipcArgs, stackid)

def ste_run_travel2(state, ipcArgs, stackid):
	rae1.rae1('travel','Paolo','home','park',state, ipcArgs, stackid)

def ste_run_travel3(state, ipcArgs, stackid):
	rae1.rae1('travel','Malik','home2','park2',state, ipcArgs, stackid)
