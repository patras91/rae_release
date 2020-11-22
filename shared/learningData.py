import GLOBALS

outputFolder = "AIJ2020"

def GetStr(a):
	return " ".join(str(item) for item in a)

class TrainingDataItem():
	def __init__(self, state, method, eff_sub, t, taskArgs, main_t, main_targs, treeNodes):
		self.s = state.copy()
		self.m = method
		self.e1 = eff_sub
		self.task = t
		self.taskArgs = taskArgs
		self.mainTask = main_t
		self.mainTaskArgs = main_targs
		self.actingTreeNodes = treeNodes

	def WriteInFile(self, f):
		f.write(self.s.GetFeatureString() + "\n")
		f.write(self.task + " " + GetStr(self.taskArgs) + "\n")
		f.write(self.mainTask + " " + GetStr(self.mainTaskArgs) + "\n")
		f.write(self.m.GetName() + " " + GetStr(self.m.GetParams()) + "\n")
		f.write(str(self.e1) + "\n")

		#if GLOBALS.GetLearningMode() == "genEffDataPlanner":
		#	for item in self.actingTreeNodes:
		#		f.write(str(item)+"\n")

class TrainingData():
	def __init__(self):
		self.l = []

	def Add(self, state, method, eff_sub, task, taskArgs, mainTask, mainTaskArgs, treeNodes=None):
		self.l.append(TrainingDataItem(state, method, eff_sub, task, taskArgs, mainTask, mainTaskArgs, treeNodes))

	#def AddBulk(self, l2, mainTask, curUtil):
	#	for item in l2:
	#		item.maintask = mainTask
	#		item.e1 = item.e1 + curUtil
	#		self.l.append(item)
	#	print("added in bulk")

	def PrintInFile(self, suffix):
		domain = GLOBALS.GetDomain()
		fname = "../../../raeResults/{}/learning/{}/{}_data_{}.txt".format(outputFolder, domain, domain, suffix)
		f = open(fname, "a")
		for item in self.l:
			item.WriteInFile(f)

trainingDataRecords = TrainingData()

def WriteTrainingData():
	if GLOBALS.GetDataGenerationMode() == "learnM1":
		trainingDataRecords.PrintInFile("actor")
	elif GLOBALS.GetDataGenerationMode() == "learnM2":
		trainingDataRecords.PrintInFile("planner")
	elif GLOBALS.GetDataGenerationMode() == "learnH":
		trainingDataRecords.PrintInFile("eff_planner")
	