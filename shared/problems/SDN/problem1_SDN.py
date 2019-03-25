__author__ = 'patras'

from domain_airsSDN import *
from timer import DURATION
from state import state

DURATION.TIME = {
    'applyRestart': 5
 }

DURATION.COUNTER = {
    'applyRestart': 5
 }

# Define common controller alternatives
c_alt1 = Controller('alt-1', 'Debian', 'Java2', 'OpenDaylight', '1.15.0')
c_alt2 = Controller('alt-2', 'Fedora', 'Java', 'ONOS', '1.15.0')
c_alt3 = Controller('alt-3', 'Ubuntu', 'Java', 'OpenDaylight', 'hydrogen')
c_alt4 = Controller('alt-4', 'Ubuntu', 'Java', 'ONOS', '1.12.0')
# For testing, last alternative has same config as c1

# Create 2 controllers, c1 and c2 with alternatives
c1 = Controller('c1', 'Ubuntu', 'Java', 'ONOS', '1.12.0',
                trust=1.0, health=1.0,
                alternatives=[{'instance': c_alt1}, {'instance': c_alt3},
                              {'instance': c_alt4}])

def ResetState():
    state.controllers = {c1.id: c1}

tasks = {
    5: [['restart', c1.id]]
}

eventsEnv = {
    #1: [simComponentAttack, [c1, 0.5]]
}