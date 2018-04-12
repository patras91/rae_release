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
SUCCESS = 'Success'
FAILURE = 'Failure'

import copy
import rae1
import gui

def taxi_rate(dist):
	return (1.5 + 0.5 * dist)

def walk(a,x,y):
	rae1.state.loc.AcquireLock(a)
	if rae1.state.loc[a] == x:
		gui.Simulate('agent',a,'starts walking at location',x,'\n')
		start = globalTimer.GetTime()
		while(globalTimer.IsCommandExecutionOver('walk', start) == False):
			pass
		gui.Simulate('agent',a,'has reached location',y,'\n')
		rae1.state.loc[a] = y
		rae1.state.loc.ReleaseLock(a)
		#rae1.state.assign(assignments=[('loc', a, y)], preCond=[('loc', a, x)])
		res = SUCCESS
	else:
		rae1.state.loc.ReleaseLock(a)
		gui.Simulate('agent',a,"isn't at location",x,'\n')
		res = FAILURE
	return res

rae1.declare_prob(walk, [0.9, 0.1])
def walk_Sim(a,x,y, outcome):
	if outcome == 0:
		rae1.state.loc[a] = y
		res = SUCCESS
	else:
		res = FAILURE
	return res

def call_taxi(a,x):
	rae1.state.occupied.AcquireLock('taxi')
	if rae1.state.occupied['taxi'] == False:
		rae1.state.loc.AcquireLock('taxi')
		start = globalTimer.GetTime()
		gui.Simulate('a taxi is on its way to location',x,'\n')
		while(globalTimer.IsCommandExecutionOver('call_taxi', start) == False):
			pass
		gui.Simulate('a taxi appears at location',x,'\n')
		rae1.state.loc['taxi'] = x
		rae1.state.loc.ReleaseLock('taxi')
		rae1.state.occupied.ReleaseLock('taxi')
		#rae1.state.assign(assignments=[('loc', 'taxi', x)], preCond=[('occupied', 'taxi', False)])
		res = SUCCESS
	else:
		rae1.state.occupied.ReleaseLock('taxi')
		gui.Simulate('Taxi is occupied \n')
		res = FAILURE
	return res

rae1.declare_prob(call_taxi, [0.7, 0.3])
def call_taxi_Sim(a,x, outcome):
	if outcome == 0:
		rae1.state.loc['taxi'] = x
		res = SUCCESS
	else:
		res = FAILURE
	return res

def enter_taxi(a):
	rae1.state.occupied.AcquireLock('taxi')
	rae1.state.loc.AcquireLock('taxi')
	rae1.state.loc.AcquireLock(a)

	if rae1.state.loc['taxi'] == rae1.state.loc[a] and rae1.state.occupied['taxi'] == False:
		start = globalTimer.GetTime()
		while(globalTimer.IsCommandExecutionOver('enter_taxi', start) == False):
			pass
		gui.Simulate('agent',a,'enters taxi at location',rae1.state.loc[a],'\n')
		rae1.state.loc[a] = 'taxi'
		rae1.state.occupied['taxi'] = True
		#rae1.state.assign(assignments=[('loc', a, 'taxi'), ('occupied', 'taxi', True)], preCond=[])
		res = SUCCESS
	else:
		gui.Simulate("there's no taxi for agent",a,'to enter or the taxi is occupied','\n')
		res = FAILURE

	rae1.state.occupied.ReleaseLock('taxi')
	rae1.state.loc.ReleaseLock('taxi')
	rae1.state.loc.ReleaseLock(a)
	return res

rae1.declare_prob(enter_taxi, [0.9, 0.1])
def enter_taxi_Sim(a, outcome):
	if outcome == 0:
		rae1.state.loc[a] = 'taxi'
		rae1.state.occupied['taxi'] = True
		res = SUCCESS
	else:
		res = FAILURE
	return res

def taxi_carry(a,y):
	rae1.state.loc.AcquireLock('taxi')
	rae1.state.loc.AcquireLock(a)

	if rae1.state.loc[a]=='taxi':
		x = rae1.state.loc['taxi']
		start = globalTimer.GetTime()
		while(globalTimer.IsCommandExecutionOver('taxi_carry', start) == False):
			pass
		gui.Simulate('taxi carries agent',a,'from',x,'to',y,'\n')
		rae1.state.loc['taxi'] = y
		rae1.state.owe.AcquireLock(a)
		rae1.state.owe[a] = taxi_rate(rae1.state.dist[x][y])
		rae1.state.owe.ReleaseLock(a)
		res = SUCCESS
	else:
		gui.Simulate('agent',a,"isn't in a taxi",'\n')
		res = FAILURE
	rae1.state.loc.ReleaseLock('taxi')
	rae1.state.loc.ReleaseLock(a)
	return res

rae1.declare_prob(taxi_carry, [0.5, 0.5])
def taxi_carry_Sim(a,y, outcome):
	if outcome == 0:
		x = rae1.state.loc['taxi']
		rae1.state.loc['taxi'] = y
		rae1.state.owe[a] = taxi_rate(rae1.state.dist[x][y])
		res = SUCCESS
	else:
		res = FAILURE
	return res

def pay_driver(a):
	rae1.state.cash.AcquireLock(a)
	rae1.state.owe.AcquireLock(a)
	if rae1.state.cash[a] >= rae1.state.owe[a]:
		start = globalTimer.GetTime()
		while(globalTimer.IsCommandExecutionOver('pay_driver', start) == False):
			pass
		gui.Simulate('agent',a,'pays',rae1.state.owe[a],'to the taxi driver','\n')
		rae1.state.cash[a] = rae1.state.cash[a] - rae1.state.owe[a]
		rae1.state.owe[a] = 0
		res = SUCCESS
	else:
		gui.Simulate('agent',a,'cannot pay',rae1.state.owe[a],'to the taxi driver','\n')
		res = FAILURE

	rae1.state.cash.ReleaseLock(a)
	rae1.state.owe.ReleaseLock(a)
	return res

rae1.declare_prob(pay_driver, [0.9, 0.1])
def pay_driver_Sim(a, outcome):
	if outcome == 0:
		rae1.state.cash[a] = rae1.state.cash[a] - rae1.state.owe[a]
		rae1.state.owe[a] = 0
		res = SUCCESS
	else:
		res = FAILURE
	return res

def leave_taxi(a):
	rae1.state.loc.AcquireLock(a)
	if rae1.state.loc[a]=='taxi':
		start = globalTimer.GetTime()
		while(globalTimer.IsCommandExecutionOver('leave_taxi', start) == False):
			pass
		gui.Simulate('agent',a,'leaves taxi at location',rae1.state.loc['taxi'],'\n')
		rae1.state.occupied.AcquireLock('taxi')
		rae1.state.loc.AcquireLock('taxi')
		rae1.state.loc[a] = rae1.state.loc['taxi']
		rae1.state.occupied['taxi'] = False
		rae1.state.occupied.ReleaseLock('taxi')
		rae1.state.loc.ReleaseLock('taxi')
		res = SUCCESS
	else:
		gui.Simulate('agent',a,"isn't in a taxi",'\n')
		res = FAILURE
	rae1.state.loc.ReleaseLock(a)
	return res

rae1.declare_prob(leave_taxi, [0.9, 0.1])
def leave_taxi_Sim(a, outcome):
	if outcome == 0:
		rae1.state.loc[a] = rae1.state.loc['taxi']
		rae1.state.occupied['taxi'] = False
		res = SUCCESS
	else:
		res = FAILURE
	return res

def travel_by_foot(a,x,y):
	if rae1.state.dist[x][y] <= 2:
		rae1.do_command(walk,a,x,y)
		return SUCCESS
	return FAILURE

def travel_by_taxi(a,x,y):
	rae1.state.cash.AcquireLock(a)
	if rae1.state.cash[a] >= taxi_rate(rae1.state.dist[x][y]):
		rae1.state.cash.ReleaseLock(a)
		rae1.do_command(call_taxi,a,x)
		rae1.do_task('ride_taxi',a,y)
		return SUCCESS
	else:
		rae1.state.cash.ReleaseLock(a)
		gui.Simulate('agent',a,"has too little money for a taxi from",x,'to',y,'\n')
		return FAILURE

def ride_taxi_method(a,y):
	rae1.state.loc.AcquireLock(a)
	if rae1.state.dist[rae1.state.loc[a]][y] < 50:
		rae1.state.loc.ReleaseLock(a)
		rae1.do_command(enter_taxi,a)
		rae1.do_command(taxi_carry,a,y)
		rae1.do_command(pay_driver,a)
		rae1.do_command(leave_taxi,a)
		return SUCCESS
	else:
		rae1.state.loc.ReleaseLock(a)
		gui.Simulate('the taxi driver is unwilling to drive to',y,'\n')
		return FAILURE

rv = RV()

rae1.declare_commands([walk, call_taxi, enter_taxi, taxi_carry, pay_driver, leave_taxi], [walk_Sim, call_taxi_Sim, enter_taxi_Sim, taxi_carry_Sim, pay_driver_Sim, leave_taxi_Sim])

rae1.declare_methods('travel', travel_by_foot, travel_by_taxi)
rae1.declare_methods('ride_taxi', ride_taxi_method)
