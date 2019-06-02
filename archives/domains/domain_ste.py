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
import ape
import gui

def taxi_rate(dist):
	return (1.5 + 0.5 * dist)

def walk(a,x,y):
	ape.state.loc.AcquireLock(a)
	if ape.state.loc[a] == x:
		gui.Simulate('agent',a,'starts walking at location',x,'\n')
		start = globalTimer.GetTime()
		while(globalTimer.IsCommandExecutionOver('walk', start) == False):
			pass
		gui.Simulate('agent',a,'has reached location',y,'\n')
		ape.state.loc[a] = y
		ape.state.loc.ReleaseLock(a)
		#ape.state.assign(assignments=[('loc', a, y)], preCond=[('loc', a, x)])
		res = SUCCESS
	else:
		ape.state.loc.ReleaseLock(a)
		gui.Simulate('agent',a,"isn't at location",x,'\n')
		res = FAILURE
	return res

ape.declare_prob(walk, [0.9, 0.1])
def walk_Sim(a,x,y, outcome):
	if outcome == 0:
		ape.state.loc[a] = y
		res = SUCCESS
	else:
		res = FAILURE
	return res

def call_taxi(a,x):
	ape.state.occupied.AcquireLock('taxi')
	if ape.state.occupied['taxi'] == False:
		ape.state.loc.AcquireLock('taxi')
		start = globalTimer.GetTime()
		gui.Simulate('a taxi is on its way to location',x,'\n')
		while(globalTimer.IsCommandExecutionOver('call_taxi', start) == False):
			pass
		gui.Simulate('a taxi appears at location',x,'\n')
		ape.state.loc['taxi'] = x
		ape.state.loc.ReleaseLock('taxi')
		ape.state.occupied.ReleaseLock('taxi')
		#ape.state.assign(assignments=[('loc', 'taxi', x)], preCond=[('occupied', 'taxi', False)])
		res = SUCCESS
	else:
		ape.state.occupied.ReleaseLock('taxi')
		gui.Simulate('Taxi is occupied \n')
		res = FAILURE
	return res

ape.declare_prob(call_taxi, [0.7, 0.3])
def call_taxi_Sim(a,x, outcome):
	if outcome == 0:
		ape.state.loc['taxi'] = x
		res = SUCCESS
	else:
		res = FAILURE
	return res

def enter_taxi(a):
	ape.state.occupied.AcquireLock('taxi')
	ape.state.loc.AcquireLock('taxi')
	ape.state.loc.AcquireLock(a)

	if ape.state.loc['taxi'] == ape.state.loc[a] and ape.state.occupied['taxi'] == False:
		start = globalTimer.GetTime()
		while(globalTimer.IsCommandExecutionOver('enter_taxi', start) == False):
			pass
		gui.Simulate('agent',a,'enters taxi at location',ape.state.loc[a],'\n')
		ape.state.loc[a] = 'taxi'
		ape.state.occupied['taxi'] = True
		#ape.state.assign(assignments=[('loc', a, 'taxi'), ('occupied', 'taxi', True)], preCond=[])
		res = SUCCESS
	else:
		gui.Simulate("there's no taxi for agent",a,'to enter or the taxi is occupied','\n')
		res = FAILURE

	ape.state.occupied.ReleaseLock('taxi')
	ape.state.loc.ReleaseLock('taxi')
	ape.state.loc.ReleaseLock(a)
	return res

ape.declare_prob(enter_taxi, [0.9, 0.1])
def enter_taxi_Sim(a, outcome):
	if outcome == 0:
		ape.state.loc[a] = 'taxi'
		ape.state.occupied['taxi'] = True
		res = SUCCESS
	else:
		res = FAILURE
	return res

def taxi_carry(a,y):
	ape.state.loc.AcquireLock('taxi')
	ape.state.loc.AcquireLock(a)

	if ape.state.loc[a]=='taxi':
		x = ape.state.loc['taxi']
		start = globalTimer.GetTime()
		while(globalTimer.IsCommandExecutionOver('taxi_carry', start) == False):
			pass
		gui.Simulate('taxi carries agent',a,'from',x,'to',y,'\n')
		ape.state.loc['taxi'] = y
		ape.state.owe.AcquireLock(a)
		ape.state.owe[a] = taxi_rate(ape.state.dist[x][y])
		ape.state.owe.ReleaseLock(a)
		res = SUCCESS
	else:
		gui.Simulate('agent',a,"isn't in a taxi",'\n')
		res = FAILURE
	ape.state.loc.ReleaseLock('taxi')
	ape.state.loc.ReleaseLock(a)
	return res

ape.declare_prob(taxi_carry, [0.5, 0.5])
def taxi_carry_Sim(a,y, outcome):
	if outcome == 0:
		x = ape.state.loc['taxi']
		ape.state.loc['taxi'] = y
		ape.state.owe[a] = taxi_rate(ape.state.dist[x][y])
		res = SUCCESS
	else:
		res = FAILURE
	return res

def pay_driver(a):
	ape.state.cash.AcquireLock(a)
	ape.state.owe.AcquireLock(a)
	if ape.state.cash[a] >= ape.state.owe[a]:
		start = globalTimer.GetTime()
		while(globalTimer.IsCommandExecutionOver('pay_driver', start) == False):
			pass
		gui.Simulate('agent',a,'pays',ape.state.owe[a],'to the taxi driver','\n')
		ape.state.cash[a] = ape.state.cash[a] - ape.state.owe[a]
		ape.state.owe[a] = 0
		res = SUCCESS
	else:
		gui.Simulate('agent',a,'cannot pay',ape.state.owe[a],'to the taxi driver','\n')
		res = FAILURE

	ape.state.cash.ReleaseLock(a)
	ape.state.owe.ReleaseLock(a)
	return res

ape.declare_prob(pay_driver, [0.9, 0.1])
def pay_driver_Sim(a, outcome):
	if outcome == 0:
		ape.state.cash[a] = ape.state.cash[a] - ape.state.owe[a]
		ape.state.owe[a] = 0
		res = SUCCESS
	else:
		res = FAILURE
	return res

def leave_taxi(a):
	ape.state.loc.AcquireLock(a)
	if ape.state.loc[a]=='taxi':
		start = globalTimer.GetTime()
		while(globalTimer.IsCommandExecutionOver('leave_taxi', start) == False):
			pass
		gui.Simulate('agent',a,'leaves taxi at location',ape.state.loc['taxi'],'\n')
		ape.state.occupied.AcquireLock('taxi')
		ape.state.loc.AcquireLock('taxi')
		ape.state.loc[a] = ape.state.loc['taxi']
		ape.state.occupied['taxi'] = False
		ape.state.occupied.ReleaseLock('taxi')
		ape.state.loc.ReleaseLock('taxi')
		res = SUCCESS
	else:
		gui.Simulate('agent',a,"isn't in a taxi",'\n')
		res = FAILURE
	ape.state.loc.ReleaseLock(a)
	return res

ape.declare_prob(leave_taxi, [0.9, 0.1])
def leave_taxi_Sim(a, outcome):
	if outcome == 0:
		ape.state.loc[a] = ape.state.loc['taxi']
		ape.state.occupied['taxi'] = False
		res = SUCCESS
	else:
		res = FAILURE
	return res

def travel_by_foot(a,x,y):
	if ape.state.dist[x][y] <= 2:
		ape.do_command(walk,a,x,y)
		return SUCCESS
	return FAILURE

def travel_by_taxi(a,x,y):
	ape.state.cash.AcquireLock(a)
	if ape.state.cash[a] >= taxi_rate(ape.state.dist[x][y]):
		ape.state.cash.ReleaseLock(a)
		ape.do_command(call_taxi,a,x)
		ape.do_task('ride_taxi',a,y)
		return SUCCESS
	else:
		ape.state.cash.ReleaseLock(a)
		gui.Simulate('agent',a,"has too little money for a taxi from",x,'to',y,'\n')
		return FAILURE

def ride_taxi_method(a,y):
	ape.state.loc.AcquireLock(a)
	if ape.state.dist[ape.state.loc[a]][y] < 50:
		ape.state.loc.ReleaseLock(a)
		ape.do_command(enter_taxi,a)
		ape.do_command(taxi_carry,a,y)
		ape.do_command(pay_driver,a)
		ape.do_command(leave_taxi,a)
		return SUCCESS
	else:
		ape.state.loc.ReleaseLock(a)
		gui.Simulate('the taxi driver is unwilling to drive to',y,'\n')
		return FAILURE

rv = RV()

ape.declare_commands([walk, call_taxi, enter_taxi, taxi_carry, pay_driver, leave_taxi], [walk_Sim, call_taxi_Sim, enter_taxi_Sim, taxi_carry_Sim, pay_driver_Sim, leave_taxi_Sim])

ape.declare_methods('travel', travel_by_foot, travel_by_taxi)
ape.declare_methods('ride_taxi', ride_taxi_method)
