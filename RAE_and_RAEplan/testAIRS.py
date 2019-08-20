__author__ = 'patras'

from testRAEandRAEplan import InitializeSecurityDomain
from state import State
from domain_airsSDN import *

if __name__ == "__main__":
	
	startState = State()
	c_alt1 = Controller('alt-1', 'Debian', 'Java2', 'OpenDaylight', '1.15.0')
	c_alt2 = Controller('alt-2', 'Fedora', 'Java', 'ONOS', '1.15.0')
	c_alt3 = Controller('alt-3', 'Ubuntu', 'Java', 'OpenDaylight', 'hydrogen')
	c_alt4 = Controller('alt-4', 'Ubuntu', 'Java', 'ONOS', '1.12.0')

	# Create 2 controllers, c1 and c2 with alternatives
	c2 = Controller('c2', 'Debian', 'Java', 'OpenDaylight', 'Oxygen-SR3',
	                    trust=1.0, health=1.0,
	                    alternatives=[{'instance': c_alt1}, {'instance': c_alt2},
	                                  {'instance': c_alt3}])

	state.controllers = {c2.id: c2}
	taskQ, cmdExecQ, cmdStatusQ = InitializeSecurityDomain(0, startState) # returns a tuple of queues
	
	taskQ.put(['recover', c2.id])