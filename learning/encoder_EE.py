import ast
from convertData import ConvertToOneHot, ConvertToOneHotHelper

def ConvertToInt(a):
	x = a.split(" ")
	return [float(i) for i in x]
	
def GetChargeStr_EE(s):
	d = ast.literal_eval(s)
	nums = [str(item/10) for item in d.values()]
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

def EncodeState_EE(state):
	a = state.split("\n")
	#loc {'r1': 'base', 'r2': 'z5', 'UAV': 'base'}
	a1 = a[0][4:]

	#charge {'UAV': 80, 'r1': 80, 'r2': 15}
	a2 = a[1][7:]

	#data {'UAV': 3, 'r1': 3, 'r2': 1}
	a3 = a[2][5:]

	#pos {'c1': 'base', 'e1': 'base', 'e2': 'base', 'e3': 'base', 'e4': 'base', 'e5': 'base', 'o1': 'UAV'}
	a4 = a[3][4:]

	#load {'r1': 'nil', 'r2': 'nil', 'UAV': 'o1'}
	a5 = a[4][5:]

	#storm {'active': True}

	return ConvertToInt(GetLocsStr_EE(a1)) + \
		ConvertToInt(GetChargeStr_EE(a2)) + \
		ConvertToInt(GetChargeStr_EE(a3)) + \
		ConvertToInt(GetPosStr_EE(a4)) + \
		ConvertToInt(GetLoadStr_EE(a5))

def GetPosStr_EE(s):
	d = ast.literal_eval(s)
	pos = [str(item) for item in d.values()]
	for i in range(0, len(pos)):
		if pos[i] not in ['base', 'z1', 'z2', 'z3', 'z4', 'z5', 'z6', 'z7', 'z8', 'z9', 'z10', 'z11']:
			if pos[i] == 'r1':
				pos[i] = '12'
			elif pos[i] == 'r2':
				pos[i] = '13'
			elif pos[i] == 'r3':
				pos[i] = '14'
			elif pos[i] == 'r4':
				pos[i] = '15'
			elif pos[i] == "UAV":
				pos[i] = '16'
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
		elif val == '\'o1\'':
			res.append('2')
		elif val == '\'e1\'':
			res.append('3')
		elif val == '\'e2\'':
			res.append('4')
		elif val == '\'e3\'':
			res.append('5')
		elif val == '\'e4\'':
			res.append('6')
		elif val == '\'e5\'':
			res.append('7')
		elif val == '\'c1\'':
			res.append('8')
		else:
			print("error load = ", val, " in EE")
			exit()
	if len(res) > 4:
		print("error more than 4 robots in EE")
		exit()

	while len(res) < 4:
		res.append('0')
	return " ".join(res)

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







