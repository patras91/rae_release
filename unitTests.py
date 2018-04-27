from testAPE import testAPE, globals, SetMode, verbosity

def TestAPE1():
	# test the problem 12 of EE
	taskInfo = testAPE('EE', 'problem12', False)

def RunUnitTests():
	verbosity(0)
	SetMode('Counter')
	globals.SetConcurrent('n')
	globals.SetLazy('n')
	globals.SetSimulationMode('off')
	TestAPE1()

if __name__ == "__main__":
	RunUnitTests()