import ast
from convertDataFormat import ConvertToOneHot, ConvertToOneHotHelper

def ConvertToInt(a):
	x = a.split(" ")
	return [float(i) for i in x]
	
def GetNums(s):
	s = s[1:-1]
	nums = []
	items = s.split(",")
	for item in items:
		parts = item.split(": ")
		key = parts[0]
		val = parts[1]
		nums.append(int(val))

	if len(nums) > 10:
		print("error")
		exit()

	if len(nums) < 10:
		while(len(nums) < 10):
			nums.append('0')

	return " ".join(nums)

def GetObjWeights(s):
	s = s[1:-1]
	nums = []
	items = s.split(",")
	for item in items:
		parts = item.split(": ")
		key = parts[0]
		val = parts[1]
		nums.append(val)

	if len(nums) > 10:
		print("error")
		exit()

	if len(nums) < 10:
		while(len(nums) < 10):
			nums.append('0')
	return " ".join(nums)


def GetObjsString(v):
	v = v[1:-1]

	res = []
	items = v.split(",")
	for item in items:
		parts = item.split(": ")
		key = parts[0]
		val = parts[1]
		if val == 'True':
			res.append('1')
		elif val == 'False':
			res.append('0')
		else:
			print("error")
			exit()

	if len(res) > 10:
		print("error")
		exit()

	if len(res) < 10:
		while(len(res) < 10):
			res.append('0')

	return " ".join(res)


def GetObjClassString(v):
	v = v[1:-1]

	res = []
	items = v.split(",")
	i = 1

	classes = {}
	for item in items:
		parts = item.split(": ")
		key = parts[0]
		vals = parts[1].split(", ")
		for val in vals:
			classes[int(val[2])] = i
		i += 1

	for j in range(len(classes.keys())):
		res.append(i)

	if len(res) > 10:
		print("error")
		exit()

	if len(res) < 10:
		while(len(res) < 10):
			res.append('0')

	return " ".join(res)

def GetLocs(v):
	v = v[1:-1]

	res = []
	items = v.split(",")
	for item in items:
		parts = item.split(": ")
		key = parts[0]
		val = parts[1]
		res.append(str(1 + int(val)))

	if len(res) > 10:
		print("error")
		exit()

	if len(res) < 10:
		while(len(res) < 10):
			res.append('0')

	return " ".join(res)
	
def ReadOnlyTaskArgs_OF(taskAndArgs):
	return 

def ReadStateVars_OF(line, f):
	a1 = line[8:-1]
	a1 = GetObjsString(a1).split(' ')
	a1H = ConvertToOneHot(a1, 'OBJECTS', 'OF')
	a1Hs = [str(i) for i in a1H]

	a2 = f.readline()[11:-1]
	a2 = GetNums(a2).split(' ')
	a2H = ConvertToOneHot(a2, 'OBJ_WEIGHT', 'OF')
	a2Hs = [str(i) for i in a2H]

	a3 = f.readline()[10:-1]
	a3 = GetObjClassString(a3).split(' ')
	a3H = ConvertToOneHot(a3, 'OBJ_CLASS', 'OF')
	a3Hs = [str(i) for i in a3H]

	a4 = f.readline()[4:-1]
	a4 = GetLocs(a4).split(' ')
	a4H = ConvertToOneHot(a4, 'loc', 'OF')
	a4Hs = [str(i) for i in a4H]

	load = f.readline()

	a5 = f.readline()[5:-1]
	a5 = GetObjsString(a5).split(' ')
	a5H = ConvertToOneHot(a5, 'busy', 'OF')
	a5Hs = [str(i) for i in a5H]

	return a1Hs + a2Hs + a3Hs + a4Hs + a5Hs


def EncodeState_OF(state):
	a = state.split("\n")

	a1 = a[0][8:]
	a1H = ConvertToOneHot(ConvertToInt(GetObjsString(a1)), 'OBJECTS', 'OF')
	
	a2 = a[1][11:]
	a2H = ConvertToOneHot(ConvertToInt(GetNums(a2)), 'OBJ_WEIGHT', 'OF')

	a3 = a[2][10:]
	a3H = ConvertToOneHot(ConvertToInt(GetObjClassString(a3)), 'OBJ_CLASS', 'OF')

	a4 = a[3][4:]
	a4H = ConvertToOneHot(ConvertToInt(GetLocs(a4)), 'loc', 'OF')

	a5 = a[5][5:]
	a5H = ConvertToOneHot(ConvertToInt(GetObjsString(a5)), 'busy', 'OF')

	return a1H + a2H + a3H + a4H + a5H

def GetOneHotParamValue_OF(p, mLine, mName):
	return [0]

def GetOneHotInstantiatedParamValue_OF(mLine, mName):
	return []
