import GLOBALS

class TrainingDataItem():
	def __init__(self, state, method, eff_sub, t, main_t, treeNodes):
		self.s = state.copy()
		self.m = method
		self.e1 = eff_sub
		self.task = t
		self.maintask = main_t
		self.actingTreeNodes = treeNodes

	def WriteInFile(self, f):
		f.write(self.s.GetFeatureString() + "\n")
		f.write(self.task + "\n")
		f.write(self.maintask + "\n")
		f.write(self.m.GetName() + "\n")
		f.write(str(self.e1) + "\n")
		if GLOBALS.GetLearningMode() == "genEffDataPlanner":
			for item in self.actingTreeNodes:
				f.write(str(item)+"\n")

class TrainingData():
	def __init__(self):
		self.l = []

	def Add(self, state, method, eff_sub, task, mainTask, treeNodes=None):
		self.l.append(TrainingDataItem(state, method, eff_sub, task, mainTask, treeNodes))

	def PrintInFile(self, suffix):
		domain = GLOBALS.GetDomain()
		fname = "{}_data_{}.txt".format(domain, suffix)
		f = open(fname, "a")
		for item in self.l:
			item.WriteInFile(f)

trainingDataRecords = TrainingData()

def WriteTrainingData():
	if GLOBALS.GetLearningMode() == "genDataActor":
		trainingDataRecords.PrintInFile("actor")
	elif GLOBALS.GetLearningMode() == "genDataPlanner":
		trainingDataRecords.PrintInFile("planner")
	elif GLOBALS.GetLearningMode() == "genEffDataPlanner":
		trainingDataRecords.PrintInFile("eff_planner")
	