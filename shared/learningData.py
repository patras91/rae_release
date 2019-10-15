import GLOBALS

class TrainingDataItem():
	def __init__(self, state, method, eff_sub, t, main_t):
		self.s = state.copy()
		self.m = method
		self.e1 = eff_sub
		self.task = t
		self.maintask = main_t

	def WriteInFile(self, f):
		f.write(self.s.GetFeatureString() + "\n")
		f.write(self.task + "\n")
		f.write(self.maintask + "\n")
		f.write(self.m.GetName() + "\n")
		f.write(str(self.e1) + "\n")

class TrainingData():
	def __init__(self):
		self.l = []

	def Add(self, state, method, eff_sub, task, mainTask):
		self.l.append(TrainingDataItem(state, method, eff_sub, task, mainTask))

	def PrintInFile(self):
		domain = GLOBALS.GetDomain()
		fname = "{}_data.txt".format(domain)
		f = open(fname, "a")
		for item in self.l:
			item.WriteInFile(f)

trainingDataRecords = TrainingData()

def WriteTrainingData():
	trainingDataRecords.PrintInFile()