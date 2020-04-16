import ast
from convertDataFormat import ConvertToOneHot, ConvertToOneHotHelper
import pdb

def ConvertToInt(a):
	x = a.split(" ")
	return [float(i) for i in x]
	
def GetObjWeights(s):
	d = ast.literal_eval(s)

	nums = []
	for key in d:
		if key[0] == 'o':
			nums.append(str(round(float(d[key]))))
	if len(nums) > 12:
		print("error in limit of obj weights")
		exit()

	if len(nums) < 12:
		while(len(nums) < 12):
			nums.append('0')

	return " ".join(nums)

def GetObjsString(v):
	v = v.replace("frozenset", "")
	d = ast.literal_eval(v)
	res = []
	for key in d:
		if key[0] == 'o':
			if d[key] == True:
				res.append('1')
			elif d[key] == False:
				res.append('0')
			else:
				print("error in the number of objects")
				exit()

	if len(res) > 12:
		print("error in the number of objects")
		exit()

	if len(res) < 12:
		while(len(res) < 12):
			res.append('0')

	return " ".join(res)

def GetObjClassString(v):
	d = ast.literal_eval(v)
	res = []
	i = 0

	classes = {}
	for key in d:
		for val in d[key]:
			classes[int(val[1:])] = i
		i += 1

	#for j in range(len(classes.keys())):
	#	res.append(str(i))

	for key in classes:
		res.append(str(classes[key]))

	if len(res) > 12:
		print("error in building obj class string")
		exit()

	if len(res) < 12:
		while(len(res) < 12):
			res.append('0')

	#print(res)
	return " ".join(res)

def GetLocs(v):
	d = ast.literal_eval(v)
	res = []
	for key in d:
		if type(d[key]) == str:
			v = d[d[key]]
		else:
			v = d[key]

		if v == 200:
			res.append('0')
		else:
			res.append(str(v))

	if len(res) > 21:
		print("error")
		exit()

	if len(res) < 21:
		while(len(res) < 21):
			res.append('0')

	return " ".join(res)
	
def ReadOnlyTaskArgs_OF(taskAndArgs):
	tParts = taskAndArgs.split(' ')
	t = tParts[0]
	res = []
	if t == 'order':
		res += ConvertToOneHot([int(tParts[1][6])], 'OBJ_CLASS', 'OF')
	elif t == 'pickupAndLoad':
		o = ConvertToOneHot([int(tParts[3][1:])], 'nObjects', 'OF')
		m = ConvertToOneHot([int(tParts[4][1:])], 'nMachines', 'OF')
		res += o + m 
	elif t == 'unloadAndDeliver':
		m = ConvertToOneHot([int(tParts[1][1:])], 'nMachines', 'OF')
		if tParts[3][2] == 'o':
			o = ConvertToOneHot([int(tParts[3][3])], 'nObjects', 'OF')
		else:
			o = ConvertToOneHot([int(tParts[2][19])], 'nObjects', 'OF')
		res += m + o
	elif t == 'moveToPallet':
		o = ConvertToOneHot([int(tParts[1][1:])], 'nObjects', 'OF')
		p = ConvertToOneHot([int(tParts[2][1:])], 'nPallets', 'OF')
		res += o + p
	return res

def ReadTaskAndArgs_OF(taskAndArgs):
	tParts = taskAndArgs.split(' ')
	t = tParts[0]
	res = []
	if t == 'order':
		res += ConvertToOneHot([int(tParts[1][6])], 'OBJ_CLASS', 'OF')
	elif t == 'pickupAndLoad':
		o = ConvertToOneHot([int(tParts[3][1:])], 'nObjects', 'OF')
		m = ConvertToOneHot([int(tParts[4][1:])], 'nMachines', 'OF')
		res += o + m 
	elif t == 'unloadAndDeliver':
		m = ConvertToOneHot([int(tParts[1][1:])], 'nMachines', 'OF')
		if tParts[3][2] == 'o':
			o = ConvertToOneHot([int(tParts[3][3])], 'nObjects', 'OF')
		else:
			o = ConvertToOneHot([int(tParts[2][19])], 'nObjects', 'OF')
		res += m + o
	elif t == 'moveToPallet':
		o = ConvertToOneHot([int(tParts[1][1:])], 'nObjects', 'OF')
		p = ConvertToOneHot([int(tParts[2][1:])], 'nPallets', 'OF')
		res += o + p
	return res

def ReadStateVars_OF(line, f):
	a1 = line[8:-1]
	a1 = GetObjsString(a1).split(' ')
	a1H = ConvertToOneHot(a1, 'OBJECTS', 'OF')
	a1Hs = [str(i) for i in a1H]

	a2 = f.readline()[11:-1]
	a2 = GetObjWeights(a2).split(' ')
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

	f.readline()
	f.readline()
	f.readline()

	return a1Hs + a2Hs + a3Hs + a4Hs + a5Hs

def EncodeState_OF(state):
	a = state.split("\n")

	a1 = a[0][8:]
	a1H = ConvertToOneHot(ConvertToInt(GetObjsString(a1)), 'OBJECTS', 'OF')
	
	a2 = a[1][11:]
	a2H = ConvertToOneHot(ConvertToInt(GetObjWeights(a2)), 'OBJ_WEIGHT', 'OF')

	a3 = a[2][10:]
	a3H = ConvertToOneHot(ConvertToInt(GetObjClassString(a3)), 'OBJ_CLASS', 'OF')

	a4 = a[3][4:]
	a4H = ConvertToOneHot(ConvertToInt(GetLocs(a4)), 'loc', 'OF')

	a5 = a[5][5:]
	a5H = ConvertToOneHot(ConvertToInt(GetObjsString(a5)), 'busy', 'OF')

	return a1H + a2H + a3H + a4H + a5H

def GetIntParamValue_OF(p, mLine, mName):
	mParts = mLine.split(' ')
	if mName == 'Order_Method1':
		if p == 'm':
			return [int(mParts[2][1])]
		elif p == 'objList':
			assert(len(mParts[3]) == 7)
			return [int(mParts[3][3])]
	elif mName == 'Order_Method2':
		if p == 'm':
			return [int(mParts[2][1])]
		elif p == 'objList':
			assert(len(mParts[3]) == 7)
			return [int(mParts[3][3])]
		elif p == "p":
			return [int(mParts[4][1])]
	elif mName == 'UnloadAndDeliver_Method1':
		return [int(mParts[-1][1])]
	elif mName == 'MoveToPallet_Method1':
		return [int(mParts[-1][1])]
	elif mName == 'PickupAndLoad_Method1':
		return [int(mParts[-1][1])]
	else:
		print("Incorrect method in OF")
		exit()

def GetOneHotInstantiatedParamValue_OF(mLine, mName):
	tParts = mLine.split(' ')
	res = []
	if mName[0:5] == 'Order':
		res += ConvertToOneHot([int(tParts[1][6])], 'OBJ_CLASS', 'OF')
	elif mName == 'PickupAndLoad_Method1':
		o = ConvertToOneHot([int(tParts[3][1:])], 'nObjects', 'OF')
		m = ConvertToOneHot([int(tParts[4][1:])], 'nMachines', 'OF')
		res += o + m 
	elif mName == 'UnloadAndDeliver_Method1':
		m = ConvertToOneHot([int(tParts[1][1:])], 'nMachines', 'OF')
		if tParts[3][2] == 'o':
			o = ConvertToOneHot([int(tParts[3][3])], 'nObjects', 'OF')
		else:
			o = ConvertToOneHot([int(tParts[2][19])], 'nObjects', 'OF')
		res += m
	elif mName == 'MoveToPallet_Method1':
		o = ConvertToOneHot([int(tParts[1][1:])], 'nObjects', 'OF')
		p = ConvertToOneHot([int(tParts[2][1:])], 'nPallets', 'OF')
		res += o + p
	return res
