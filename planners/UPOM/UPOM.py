__author__ = 'patras'
from opPlanner import OpPlanner

class UPOMChoice(OpPlanner):
	def __init__(self, l):
		self.n_ro = l[0]
		self.maxSearchDepth = l[1]
