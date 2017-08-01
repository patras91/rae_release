from __future__ import print_function
import sys
from domain_constants import *
from timer import globalTimer
"""
File ste.py
Author: Dana Nau <nau@cs.umd.edu>, July 7, 2017
Based roughly on the "travel from home to the park" example in my lectures,
but modified to have multiple levels of tasks.

Sunandita: Updated the test cases to test RAE
Dana: tweaks to how verbosity is handled.
"""

import copy
import rae1
import gui

def taxi_rate(dist):
	return (1.5 + 0.5 * dist)

def walk(a,x,y):
	if rae1.state.loc[a] == x:
		gui.Simulate('agent',a,'starts walking at location',x,'\n')
		start = globalTimer.GetTime()
		while(globalTimer.IsCommandExecutionOver('walk', start) == False):
			pass
		gui.Simulate('agent',a,'has reached location',y,'\n')
		rae1.state.loc[a] = y
		res = SUCCESS
	else:
		gui.Simulate('agent',a,"isn't at location",x,'\n')
		res = FAILURE
	return res

def call_taxi(a,x):
	if rae1.state.occupied['taxi'] == False:
		start = globalTimer.GetTime()
		gui.Simulate('a taxi is on its way to location',x,'\n')
		while(globalTimer.IsCommandExecutionOver('call_taxi', start) == False):
			pass
		gui.Simulate('a taxi appears at location',x,'\n')
		rae1.state.loc['taxi'] = x
		res = SUCCESS
	else:
		gui.Simulate('Taxi is occupied \n')
		res = FAILURE
	return res

def enter_taxi(a):
	if rae1.state.loc['taxi'] == rae1.state.loc[a] and rae1.state.occupied['taxi'] == False:
		start = globalTimer.GetTime()
		while(globalTimer.IsCommandExecutionOver('enter_taxi', start) == False):
			if rae1.state.loc['taxi'] != rae1.state.loc[a]:
				gui.Simulate('taxi is gone away from of agent',a,'\'s location \n')
				return FAILURE
		gui.Simulate('agent',a,'enters taxi at location',rae1.state.loc[a],'\n')
		rae1.state.loc[a] = 'taxi'
		rae1.state.occupied['taxi'] = True
		return SUCCESS
	else:
		gui.Simulate("there's no taxi for agent",a,'to enter or the taxi is occupied','\n')
		return FAILURE

def taxi_carry(a,y):
	if rae1.state.loc[a]=='taxi':
		x = rae1.state.loc['taxi']
		start = globalTimer.GetTime()
		while(globalTimer.IsCommandExecutionOver('taxi_carry', start) == False):
			if rae1.state.loc['taxi'] != x:
				gui.Simulate('taxi is gone out of agent',a,'\'s route \n')
				return FAILURE
		gui.Simulate('taxi carries agent',a,'from',x,'to',y,'\n')
		rae1.state.loc['taxi'] = y
		rae1.state.owe[a] = taxi_rate(rae1.state.dist[x][y])
		return SUCCESS
	else:
		gui.Simulate('agent',a,"isn't in a taxi",'\n')
		return FAILURE

def pay_driver(a):
	if rae1.state.cash[a] >= rae1.state.owe[a]:
		start = globalTimer.GetTime()
		while(globalTimer.IsCommandExecutionOver('pay_driver', start) == False):
			pass
		gui.Simulate('agent',a,'pays',rae1.state.owe[a],'to the taxi driver','\n')
		rae1.state.cash[a] = rae1.state.cash[a] - rae1.state.owe[a]
		rae1.state.owe[a] = 0
		return SUCCESS
	else:
		gui.Simulate('agent',a,'cannot pay',rae1.state.owe[a],'to the taxi driver','\n')
		return FAILURE

def leave_taxi(a):
	if rae1.state.loc[a]=='taxi':
		start = globalTimer.GetTime()
		while(globalTimer.IsCommandExecutionOver('leave_taxi', start) == False):
			pass
		gui.Simulate('agent',a,'leaves taxi at location',rae1.state.loc['taxi'],'\n')
		rae1.state.loc[a] = rae1.state.loc['taxi']
		rae1.state.occupied['taxi'] = False
		return SUCCESS
	else:
		gui.Simulate('agent',a,"isn't in a taxi",'\n')
		return FAILURE

def travel_by_foot(a,x,y,stackid):
	if rae1.state.dist[x][y] <= 2:
		rae1.do_command(walk,a,x,y,stackid)
		return SUCCESS
	return FAILURE

def travel_by_taxi(a,x,y,stackid):
	if rae1.state.cash[a] >= taxi_rate(rae1.state.dist[x][y]):
		rae1.do_command(call_taxi,a,x,stackid)
		rae1.do_task('ride_taxi',a,y,stackid)
		return SUCCESS
	else:
		gui.Simulate('agent',a,"has too little money for a taxi from",x,'to',y,'\n')
		return FAILURE

def ride_taxi_method(a,y,stackid):
	if rae1.state.dist[rae1.state.loc[a]][y] < 50:
		rae1.do_command(enter_taxi,a,stackid)
		rae1.do_command(taxi_carry,a,y,stackid)
		rae1.do_command(pay_driver,a,stackid)
		rae1.do_command(leave_taxi,a,stackid)
		return SUCCESS
	else:
		gui.Simulate('the taxi driver is unwilling to drive to',y,'\n')
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
	print("* Call rae1 on simple travel domain. For different amounts of")
	print("* printout, try verbosity(0), verbosity(1), or verbosity(2).")
	print('*********************************************************')
	sys.stdout.flush()

	rae1.state.loc = {'Dana':'home', 'Paolo':'home', 'Malik':'home2'}
	rae1.state.cash = {'Dana':20, 'Paolo': 5, 'Malik': 100}
	rae1.state.owe = {'Dana':0, 'Paolo': 0, 'Malik': 0}
	rae1.state.dist = {'home':{'park':8}, 'park':{'home':8}, 'home2':{'park2':80}, 'park2':{'home2':80}}
	rae1.state.occupied = {'taxi':False}