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
		nums.append(val)

	if len(nums) > 2:
		print("error")
		exit()

	if len(nums) == 1:
		nums.append('0')
	return " ".join(nums)

def GetLoadString(s):
	d = ast.literal_eval(s)
	res = []
	for key in d:
		if d[key] == 'nil':
			res.append('0')
		elif d[key] == 'o1':
			res.append('1')
		elif d[key] == 'c1':
			res.append('2')
		else:
			print("error ", d[key])
			exit()
	if len(res) > 2:
		print("error")
		exit()

	if len(res) == 1:
		res.append('0')
	return " ".join(res)

def GetPosString(pos):
	pos = pos[1:-1]

	res = []
	items = pos.split(",")
	for item in items:
		parts = item.split(": ")
		key = parts[0]
		val = parts[1]
		if val == '\'Unknown\'':
			res.append('0')
		elif val == '\'r1\'':
			res.append('11')
		elif val == '\'r2\'':
			res.append('12')
		else:
			res.append(val)

	if len(res) > 2:
		print("error")
		exit()

	if len(res) == 1:
		res.append('0')
	return " ".join(res)

def GetEmS(e):
	e = e[1:-1]

	res = []
	items = e.split(",")
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

	if len(res) > 2:
		print("error")
		exit()

	if len(res) == 1:
		res.append('0')
	return " ".join(res)

def GetViewString(v):
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
	
def ReadStateVars_CR(line, f):
	a1 = line[4:-1]
	a1 = GetNums(a1).split(' ')
	a1H = ConvertToOneHot(a1, 'loc', 'CR')
	a1Hs = [str(i) for i in a1H]

	a2 = f.readline()[6:-1]
	a2 = GetNums(a2).split(' ')
	a2H = ConvertToOneHot(a2, 'charge', 'CR')
	a2Hs = [str(i) for i in a2H]

	a3 = f.readline()[5:-1]
	a3 = GetLoadString(a3).split(' ')
	a3H = ConvertToOneHot(a3, 'load', 'CR')
	a3Hs = [str(i) for i in a3H]

	a4 = f.readline()[4:-1]
	a4 = GetPosString(a4).split(' ')
	a4H = ConvertToOneHot(a4, 'pos', 'CR')
	a4Hs = [str(i) for i in a4H]

	containers = f.readline()

	a5 = f.readline()[18:-1]
	a5 = GetEmS(a5).split(' ')
	a5H = ConvertToOneHot(a5, 'emergencyHandling', 'CR')
	a5Hs = [str(i) for i in a5H]

	a6 = f.readline()[5:-1]
	a6 = GetViewString(a6).split(' ')
	a6H = ConvertToOneHot(a6, 'view', 'CR')
	a6Hs = [str(i) for i in a6H]

	return a1Hs + a2Hs + a3Hs + a4Hs + a5Hs + a6Hs

def EncodeState_CR(state):
	a = state.split("\n")

	a1 = a[0][4:]
	a1H = ConvertToOneHot(ConvertToInt(GetNums(a1)), 'loc', 'CR')
	
	a2 = a[1][6:]
	a2H = ConvertToOneHot(ConvertToInt(GetNums(a2)), 'charge', 'CR')

	a3 = a[2][5:]
	a3H = ConvertToOneHot(ConvertToInt(GetLoadString(a3)), 'load', 'CR')

	a4 = a[3][4:]
	a4H = ConvertToOneHot(ConvertToInt(GetPosString(a4)), 'pos', 'CR')

	a5 = a[5][18:]
	a5H = ConvertToOneHot(ConvertToInt(GetEmS(a5)), 'emergencyHandling', 'CR')

	a6 = a[6][5:]
	a6H = ConvertToOneHot(ConvertToInt(GetViewString(a6)), 'view', 'CR')

	return a1H + a2H + a3H + a4H + a5H + a6H 
