__author__ = 'patras'

class OpPlanner():
	def __init__(self):
		pass

	def InitializePlanningTree(self):
        root = rTree.PlanningTree('root', 'root', 'root') # initialize the root of the refinement tree being built
        self.planLocals.SetCurrentNode(root)
        self.planLocals.SetPlanningTree(root)