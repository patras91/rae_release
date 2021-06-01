__author__ = 'patras'
from planners.opPlanner import OpPlanner

class APEPlanChoice(OpPlanner):
	def __init__(self, l):
		self.b = l[0]
