__author__ = 'patras'
from opPlanner import OpPlanner

class RAEPlanChoice(OpPlanner):
	def __init__(self, l):
		self.b = l[0]
		self.k = l[1]
		self.maxSearchDepth = l[2]
