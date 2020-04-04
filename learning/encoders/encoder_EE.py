import ast
from convertData import ConvertToOneHot, ConvertToOneHotHelper

def ConvertToInt(a):
	x = a.split(" ")
	return [float(i) for i in x]
	
def GetChargeStr_EE(s):
	d = ast.literal_eval(s)
	nums = [str(int(item/10)) for item in d.values()]
	if len(nums) > 3:
		print(" too many robots in EE")
		exit()
	while(len(nums) < 3):
		nums.append('0')
	return (" ".join(nums))

def GetLocsStr_EE(s):
	d = ast.literal_eval(s)
	nums = []
	for item in d.values():
		if item[0] == 'b':
			nums.append('0')
		else:
			nums.append(item[1:])

	if len(nums) > 3:
		print(" too many robots in EE")
		exit()
	while(len(nums) < 3):
		nums.append('0')
	return (" ".join(nums))

def GetPosStr_EE(s):
	d = ast.literal_eval(s)
	nums = []
	for item in d.values():
		if item[0] == 'b':
			nums.append('0')
		elif item[0] == 'z':
			nums.append(item[1:])
		elif item == "UAV":
			nums.append('8')
		elif item == "r1":
			nums.append('9')
		elif item == 'r2':
			nums.append('10')
		else:
			print("Unconsidered position ", item)

	if len(nums) > 3:
		print(" too many robots in EE")
		exit()
	while(len(nums) < 3):
		nums.append('0')
	return (" ".join(nums))

def GetDataStr_EE(s):
	d = ast.literal_eval(s)
	nums = []
	for item in d.values():
		nums.append(str(item))

	if len(nums) > 3:
		print(" too many robots in EE")
		exit()
	while(len(nums) < 3):
		nums.append('0')
	return (" ".join(nums))

def EncodeState_EE(state):
	a = state.split("\n")
	#loc {'r1': 'base', 'r2': 'z5', 'UAV': 'base'}
	a1 = a[0][4:]
	a1H = ConvertToOneHot(ConvertToInt(GetLocsStr_EE(a1)), 'loc', 'EE')

	#charge {'UAV': 80, 'r1': 80, 'r2': 15}
	a2 = a[1][7:]
	a2H = ConvertToOneHot(ConvertToInt(GetChargeStr_EE(a2)), 'charge', 'EE')

	#data {'UAV': 3, 'r1': 3, 'r2': 1}
	a3 = a[2][5:]
	a3H = ConvertToOneHot(ConvertToInt(GetDataStr_EE(a3)), 'data', 'EE')

	#pos {'c1': 'base', 'e1': 'base', 'e2': 'base', 'e3': 'base', 'e4': 'base', 'e5': 'base', 'o1': 'UAV'}
	a4 = a[3][4:]
	a4H = ConvertToOneHot(ConvertToInt(GetPosStr_EE(a4)), 'pos', 'EE')

	#load {'r1': 'nil', 'r2': 'nil', 'UAV': 'o1'}
	a5 = a[4][5:]
	a5H = ConvertToOneHot(ConvertToInt(GetLoadStr_EE(a5)), 'load', 'EE')

	#storm {'active': True}

	return a1H + a2H + a3H + a4H + a5H

def GetPosStr_EE(s):
	d = ast.literal_eval(s)
	pos = [str(item) for item in d.values()]
	for i in range(0, len(pos)):
		if pos[i] not in ['base', 'z1', 'z2', 'z3', 'z4', 'z5', 'z6', 'z7']:
			if pos[i] == 'r1':
				pos[i] = '8'
			elif pos[i] == 'r2':
				pos[i] = '9'
			elif pos[i] == 'UAV':
				pos[i] = '10'
			else:
				print(" invalid position in EE ", pos[i])
				exit()
		else:
			if pos[i] == 'base':
				pos[i] = '0'
			else:
				pos[i] = pos[i][1:]
	if len(pos) > 7:
		print(" too many objects in EE", len(pos), pos)
		exit()
	while(len(pos) < 7):
		pos.append('0')
	return " ".join(pos)

def GetLoadStr_EE(s):
	s = s[1:-1]
	res = []
	items = s.split(",")
	for item in items:
		parts = item.split(": ")
		key = parts[0]
		val = parts[1]
		if val == '\'nil\'':
			res.append('0')
		elif val == '\'o1\'':
			res.append('1')
		elif val == '\'e1\'':
			res.append('2')
		elif val == '\'e2\'':
			res.append('3')
		elif val == '\'e3\'':
			res.append('4')
		elif val == '\'e4\'':
			res.append('5')
		elif val == '\'e5\'':
			res.append('6')
		elif val == '\'c1\'':
			res.append('7')
		else:
			print("error load = ", val, " in EE")
			exit()
	if len(res) > 3:
		print("error more than 3 robots in EE")
		exit()

	while len(res) < 3:
		res.append('0')
	return " ".join(res)

def ReadTaskAndArgs_EE(taskAndArgs):
	params = taskAndArgs.split(' ')
	task = params[0]
	robotStr = params[1]
	robot = robotStr[2:4]
	#print("robot = ", robot)
	if robot == "r1":
		res = [1, 0, 0]
	elif robot == "r2":
		res = [0, 1, 0]
	elif robot == "UA":
		res = [0, 0, 1]
	else:
		print("unknown robot ", robot)
	
	if task == "moveTo" or task == "flyTo" or task == "handleEmergency":
		if params[2][1] == 'b':
			l = 0
		else:
			l = int(params[2][2:3])
		#print(" l = ", l)

		res += ConvertToOneHotHelper(l, 8)
	elif task == "explore":
		if params[3][1] == 'b':
			l = 0
		else:
			#print(params[3])
			l = int(params[3][2:3])
		#print(" l = ", l)
		#print(" l = ",l)
		res +=  ConvertToOneHotHelper(l, 8)
	else:
		res += [0]*8

	if task == "moveThroughDoorway":
		door = params[2][1:3]
	elif task == "unlatch":
		door = params[2][1:3]
	else:
		door = None

	#print("door = ", door)
	if door == None:
		res += [0, 0, 0]
	elif door == "d1":
		res += [1, 0, 0]
	elif door == "d2":
		res += [0, 1, 0]
	else:
		res += [0, 0, 1]

	#print(task)
	#print(res)
	return res

def ReadStateVars_EE(line, f):
	for i in range(0, 6):
		if line[0:3] == "loc":
			#loc {'r1': 'base', 'r2': 'z5', 'UAV': 'base'}
			a1 = line[4:-1]
			a1 = GetLocsStr_EE(a1).split(' ')
			a1H = ConvertToOneHot(a1, 'loc', 'EE')
			a1Hs = [str(i) for i in a1H]

		elif line[0:3] == "cha":
			#charge {'UAV': 80, 'r1': 80, 'r2': 15}
			a2 = line[7:-1]
			a2 = GetChargeStr_EE(a2).split(' ')
			a2H = ConvertToOneHot(a2, 'charge', 'EE')
			a2Hs = [str(i) for i in a2H]

		elif line[0:3] == "dat":
			#data {'UAV': 3, 'r1': 3, 'r2': 1}
			a3 = line[5:-1]
			a3 = GetDataStr_EE(a3).split(' ')
			a3H = ConvertToOneHot(a3, 'data', 'EE')
			a3Hs = [str(i) for i in a3H]

		elif line[0:3] == "pos":
			#pos {'c1': 'base', 'e1': 'base', 'e2': 'base', 'e3': 'base', 'e4': 'base', 'e5': 'base', 'o1': 'UAV'}
			a4 = line[4:-1]
			a4 = GetPosStr_EE(a4).split(' ')
			a4H = ConvertToOneHot(a4, 'pos', 'EE')
			a4Hs = [str(i) for i in a4H]

		elif line[0:3] == "loa":
			#load {'r1': 'nil', 'r2': 'nil', 'UAV': 'o1'}
			a5 = line[5:-1]
			a5 = GetLoadStr_EE(a5).split(' ')
			a5H = ConvertToOneHot(a5, 'load', 'EE')
			a5Hs = [str(i) for i in a5H]

		else:
			pass
			#storm {'active': True}
		
		if i < 5:
			line = f.readline()

	return a1Hs + a2Hs + a3Hs + a4Hs + a5Hs







