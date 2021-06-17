import ast
from learning.convertDataFormat import ConvertToOneHot, ConvertToOneHotHelper

def ConvertToInt(a):
	x = a.split(" ")
	return [float(i) for i in x]

def GetDoor_OneHot(d):
	return {
		None: [0, 0, 0],
		"d1": [1, 0, 0],
		"d2": [0, 1, 0],
		"d3": [0, 0, 1],
	}[d]

def GetLoadString_SD(s):
	d = ast.literal_eval(s)
	res = []
	for key in d:
		val = d[key]
		if val == 'nil':
			res.append('0')
		elif val == 'o1':
			res.append('1')
		elif val == 'o1':
			res.append('2')
		elif val == 'H':
			res.append('3')
		else:
			print("error load = ", val, " in SD")
			exit()
	if len(res) > 4:
		print("error more than 4 robots in SD")
		exit()

	while len(res) < 4:
		res.append('4')
	return " ".join(res)

def GetStatusString_SD(s):
	d = ast.literal_eval(s)
	nums = []
	for key in d:
		if d[key] == 'busy':
			nums.append('1')
		else:
			nums.append('0')
	if len(nums) > 4:
		print(" too many robots in SD")
		exit()
	while(len(nums) < 4):
		nums.append('2')

	return (" ".join(nums))

def GetDoorStatusStr_SD(s):
	d = ast.literal_eval(s)
	res = []
	for key in d:
		if d[key] == "opened":
			res.append('0')
		elif d[key] == "closed":
			res.append('1')
		elif d[key] == "held":
			res.append('2')
		else:
			print("invalid door status")
			exit()

	while(len(res) < 4):
		res.append('3')

	return " ".join(res)

def GetDoorTypeStr_SD(s):
	d = ast.literal_eval(s)
	res = []
	for key in d:
		if d[key] == "Unknown":
			res.append('0')
		elif d[key] == "ordinary":
			res.append('1')
		elif d[key] == "spring":
			res.append('2')
		else:
			print("invalid door type")
			exit()

	while(len(res) < 4):
		res.append('3')

	return " ".join(res)

def GetLocStr_SD(s):
	d = ast.literal_eval(s)
	nums = [str(item) for item in d.values()]
	if len(nums) > 4:
		print(" too many robots in SD")
		exit()
	while(len(nums) < 4):
		nums.append('0')
	return (" ".join(nums))

def GetPosStr_SD(s):
	d = ast.literal_eval(s)
	pos = [str(item) for item in d.values()]
	for i in range(0, len(pos)):
		if pos[i] not in ['1', '2', '3', '4', '5', '6', '7']:
			if pos[i] == 'r1':
				pos[i] = '8'
			elif pos[i] == 'r2':
				pos[i] = '9'
			elif pos[i] == 'r3':
				pos[i] = '10'
			elif pos[i] == 'r4':
				pos[i] = '11'
			else:
				print(" invalid position in SD ", pos[i])
				exit()
	if len(pos) > 2:
		print(" too many objects in SD")
		exit()
	while(len(pos) < 2):
		pos.append('0')
	return " ".join(pos)

def ReadTaskAndArgs_SD(taskAndArgs):
	params = taskAndArgs.split(' ')
	task = params[0]
	robotStr = params[1]
	robot = robotStr[2:4]
	#print("robot = ", robot)
	if robot == "r1":
		res = [1, 0, 0, 0]
	elif robot == "r2":
		res = [0, 1, 0, 0]
	elif robot == "r3":
		res = [0, 0, 1, 0]
	elif robot == "r4":
		res = [0, 0, 0, 1]
	
	# the location
	if task == "moveTo":
		#print(" l = ", int(params[2][0:1]))
		res += ConvertToOneHotHelper(int(params[2][0:1]), 8)
	elif task == "fetch":
		#print(" l = ",int(params[3][0:1]))
		res +=  ConvertToOneHotHelper(int(params[3][0:1]), 8)
	elif task == "moveThroughDoorway":
		#print(" l = ",int(params[3][0:1]))
		res += ConvertToOneHotHelper(int(params[3][0:1]), 8)
	else:
		res += [0]*8

	if task == "moveThroughDoorway":
		door = params[2][1:3]
	elif task == "unlatch":
		door = params[2][1:3]
	else:
		door = None
	res += GetDoor_OneHot(door)

	return res

def ReadOnlyTaskArgs_SD(taskAndArgs):
	params = taskAndArgs.split(' ')
	task = params[0]
	robot = params[1]

	res = {
		"r1": [1, 0, 0, 0],
		"r2": [0, 1, 0, 0],
		"r3": [0, 0, 1, 0],
		"r4": [0, 0, 0, 1],
	}[robot]
	
	if task == "moveThroughDoorway":
		#print(" l = ",int(params[3][0:1]))
		res += ConvertToOneHotHelper(int(params[3][0:1]), 8)
		door = params[2]
		res += GetDoor_OneHot(door)

	return res

def ReadStateVars_SD(line, f):
	#load {'r1': 'nil', 'r2': 'nil', 'r3': 'nil'}
	
	for i in range(6):
		if line[0:3] == "loa":
			a1 = line[5:-1]
			a1 = GetLoadString_SD(a1).split(' ')
			a1H = ConvertToOneHot(a1, 'load', 'SD')
			a1Hs = [str(i) for i in a1H]

		elif line[0:3] == "sta":
			#status {'r1': 'busy', 'r2': 'free', 'r3': 'busy'}
			a2 = line[7:-1]
			a2 = GetStatusString_SD(a2).split(' ')
			a2H = ConvertToOneHot(a2, 'status', 'SD')
			a2Hs = [str(i) for i in a2H]

		elif line[0:3] == "loc":
			#loc {'r1': 2, 'r2': 1, 'r3': 2}
			a3 = line[4:-1]
			a3 = GetLocStr_SD(a3).split(' ')
			a3H = ConvertToOneHot(a3, 'loc', 'SD')
			a3Hs = [str(i) for i in a3H]

		elif line[0:3] == "pos":
			#pos {'o1': 1}
			a4 = line[4:-1]
			a4 = GetPosStr_SD(a4).split(' ')
			a4H = ConvertToOneHot(a4, 'pos', 'SD')
			a4Hs = [str(i) for i in a4H]

		elif line[0:5] == "doorS":	
			#doorStatus {'d1': 'closed', 'd2': 'closed'}
			a5 = line[11:-1]
			a5 = GetDoorStatusStr_SD(a5).split(' ')
			a5H = ConvertToOneHot(a5, 'doorStatus', 'SD')
			a5Hs = [str(i) for i in a5H]

		elif line[0:5] == "doorT":
			#doorType {'d1': 'Unknown', 'd2': 'Unknown'}
			a6 = line[9:-1]
			a6 = GetDoorTypeStr_SD(a6).split(' ')
			a6H = ConvertToOneHot(a6, 'doorType', 'SD')
			a6Hs = [str(i) for i in a6H]

		if i < 5:
			line = f.readline()

	a = a1Hs + a2Hs + a3Hs + a4Hs + a5Hs + a6Hs
	return a

def EncodeState_SD(state):
	a = state.split("\n")
	#load {'r1': 'nil', 'r2': 'nil', 'r3': 'nil'}	
	a1 = a[0][5:]
	a1H = ConvertToOneHot(ConvertToInt(GetLoadString_SD(a1)), "load", "SD")

	#status {'r1': 'busy', 'r2': 'free', 'r3': 'busy'}
	a2 = a[1][7:]
	a2H = ConvertToOneHot(ConvertToInt(GetStatusString_SD(a2)), "status", "SD")

	#loc {'r1': 2, 'r2': 1, 'r3': 2}
	a3 = a[2][4:]
	a3H = ConvertToOneHot(ConvertToInt(GetLocStr_SD(a3)), "loc", "SD")

	#pos {'o1': 1}
	a4 = a[3][4:]
	a4H = ConvertToOneHot(ConvertToInt(GetPosStr_SD(a4)), "pos", "SD")

	#doorStatus {'d1': 'closed', 'd2': 'closed'}
	a5 = a[4][11:]
	a5H = ConvertToOneHot(ConvertToInt(GetDoorStatusStr_SD(a5)), "doorStatus", "SD")

	#doorType {'d1': 'Unknown', 'd2': 'Unknown'}
	a6 = a[5][9:]
	a6H = ConvertToOneHot(ConvertToInt(GetDoorTypeStr_SD(a6)), "doorType", "SD")

	return a1H + a2H + a3H + a4H + a5H + a6H

def GetIntParamValue_SD(p, mLine, mName): # uninstantiated params
	mParts = mLine.split(' ')
	if mName == 'MoveThroughDoorway_Method2':
		robot = mParts[4]
	elif mName == 'Recover_Method1':
		robot = mParts[2]
	return {
		'r1': [0],
		'r2': [1],
		'r3': [2],
		'r4': [3],
	}[robot]

def GetOneHotInstantiatedParamValue_SD(mLine, mName): # instantiated params
	mParts = mLine.split(' ')
	robot = mParts[1]
	res = {
		"r1": [1, 0, 0, 0],
		"r2": [0, 1, 0, 0],
		"r3": [0, 0, 1, 0],
		"r4": [0, 0, 0, 1],
	}[robot]
	
	if mName == "MoveThroughDoorway_Method2":
		res += GetDoor_OneHot(mParts[2])
		res += ConvertToOneHotHelper(int(mParts[3]), 8)

	return res
