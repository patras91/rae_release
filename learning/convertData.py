import torch
import math
import ast

def GetLabel(yhat):
    r, predicted = torch.max(yhat, 0)
    return predicted.long()

methodCodes = {
	"CR": {
	'Search_Method1': 0, 
	'Search_Method2': 1,
	'Fetch_Method1': 2, 
	'Fetch_Method2': 3,
	'Recharge_Method1': 4, 
	'Recharge_Method2': 5,
	'Recharge_Method3': 6,
	'MoveTo_Method1': 7,
 	'Emergency_Method1': 8,
	'NonEmergencyMove_Method1': 9,
	},
	"SR": {
    'MoveTo_Method4' : 0,
    'MoveTo_Method3': 1, 
    'MoveTo_Method2': 2, 
    'MoveTo_Method1': 3,
    'Rescue_Method1': 4,
    'Rescue_Method2': 5,
    'HelpPerson_Method2': 6,
    'HelpPerson_Method1': 7, 
    'GetSupplies_Method2': 8,
    'GetSupplies_Method1': 9,
    'Survey_Method1': 10,
    'Survey_Method2': 11,
    'GetRobot_Method1': 12,
    'GetRobot_Method2': 13,
    'AdjustAltitude_Method1': 14,
    'AdjustAltitude_Method2': 15,
	},
	"SD": {
	"Fetch_Method1": 0,
	"MoveTo_Method1": 1,
	"MoveThroughDoorway_Method1": 2,
	"MoveThroughDoorway_Method3": 3,
	"MoveThroughDoorway_Method4": 4,
	"MoveThroughDoorway_Method2": 5,
	"Unlatch_Method1": 6,
	"Unlatch_Method2": 7,
	"Recover_Method1": 8,
	},
	"EE": {
	"Explore_Method1": 0,
    "GetEquipment_Method1": 1,
    "GetEquipment_Method2": 2,
    "GetEquipment_Method3": 3,
    "MoveTo_Method1": 4,
    "FlyTo_Method1": 5,
    "FlyTo_Method2": 6,
    "Recharge_Method1": 7,
    "Recharge_Method2": 8,
    "DepositData_Method1": 9,
    "DepositData_Method2": 10, 
    "DoActivities_Method1": 11, 
    "DoActivities_Method2": 12, 
    "DoActivities_Method3": 13,
    "HandleEmergency_Method2": 14, 
    "HandleEmergency_Method1": 15,
    "HandleEmergency_Method3": 16,
	}
}

taskCodes = {
	"CR": {
	'search': 1,
	'fetch': 2,
	'recharge': 3,
	'moveTo': 4,
	'emergency': 5,
	'nonEmergencyMove': 6
	},
	"SR": {
	'moveTo': 1,
	'rescue': 2,
	'helpPerson': 3,
	'getSupplies': 4,
	'survey': 5,
	'getRobot': 6,
	'adjustAltitude': 7,
	},
	"SD": {
	"fetch": 1,
	"moveTo": 2,
	"moveThroughDoorway": 3,
	"unlatch": 4,
	"collision": 5,
	},
	"EE": {
	'explore': 1,
	'getEquipment': 2,
	'flyTo': 3,
	'moveTo': 4,
	'recharge': 5,
	'depositData': 6, 
	'doActivities': 7,
	'handleEmergency': 8,
	}
}

actingNodeCodes = {
	"CR": {
	'Search_Method1': 1, 
	'Search_Method2': 2,
	'Fetch_Method1': 3, 
	'Fetch_Method2': 4,
	'Recharge_Method1': 5, 
	'Recharge_Method2': 6,
	'Recharge_Method3': 7,
	'MoveTo_Method1': 8,
 	'Emergency_Method1': 9,
	'NonEmergencyMove_Method1': 10,
	"0": 0,
	"root": 11,
	"put": 12, 
	"take": 13, 
	"perceive": 14,
	"charge": 15, 
	"move": 16, 
	"moveToEmergency": 17, 
	"addressEmergency": 18, 
	"wait": 19, 
	"fail": 20,
	},
}
maxNum = 0
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
			res.append('0.1')
		elif val == '\'r1\'':
			res.append('0.3')
		elif val == '\'r2\'':
			res.append('0.6')
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
	locs = line[4:-1]
	locNumbers = GetNums(locs)

	charge = f.readline()[6:-1]
	chargeNumbers = GetNums(charge)

	load = f.readline()[5:-1]
	loadString = GetLoadString(load)

	pos = f.readline()[4:-1]
	posString = GetPosString(pos)

	containers = f.readline()[11:-1]

	emergencyHandling = f.readline()[18:-1]
	emergencyString = GetEmS(emergencyHandling)

	view = f.readline()[5:-1]
	viewString = GetViewString(view)

	return [locNumbers, chargeNumbers, loadString, posString, emergencyString, viewString]



def GetLocsSR(s):
	d = ast.literal_eval(s)
	nums = []
	for key in d:
		(x, y) = d[key]
		nums.append(str(x))
		nums.append(str(y))

	if len(nums) > 8:
		print("error")
		exit()

	while(len(nums) < 8):
		nums.append('0')
	return " ".join(nums)

def GetMedsSR(s):
	s = s[1:-1]
	nums = []
	items = s.split(",")
	for item in items:
		parts = item.split(": ")
		key = parts[0]
		val = parts[1]
		nums.append(val)

	if len(nums) > 4:
		print("error")
		exit()

	while(len(nums) < 4):
		nums.append('0')
	return " ".join(nums)

def GetStatStr_SR(s):
	d = ast.literal_eval(s)
	nums = []
	for key in d:
		if d[key] == 'free':
			nums.append('1')
		elif d[key] == 'Unknown':
			nums.append('2')
		elif d[key] == 'OK':
			nums.append('3')
		elif d[key] == 'dead':
			nums.append('4')
		elif d[key] == 'OK':
			nums.append('5')
		elif d[key] == 'injured':
			nums.append('6')
		elif d[key] == 'hasDebri':
			nums.append('7')
		elif d[key] == 'clear':
			nums.append('8')
		elif d[key] == 'busy':
			nums.append('9')
		else:
			print("unknown status in SR ", d[key])
			exit()


	return (" ".join(nums))

def ReadStateVars_SR(line, f):
	#loc {'w1': (7, 24), 'w2': (24, 11), 'p1': (22, 30), 'a1': (23, 15)}

	locs = line[4:-1]
	locNumbers = GetLocsSR(locs)

	#hasMedicine {'a1': 0, 'w1': 0, 'w2': 0}
	med = f.readline()[12:-1]
	medStr = GetMedsSR(med)

	#robotType {'w1': 'wheeled', 'a1': 'uav', 'w2': 'wheeled'}
	ty = f.readline()[10:-1]
	#tyStr = GetTypeStr_SR(ty)

	#status {'w1': 'free', 'w2': 'free', 'a1': 'Unknown', 'p1': 'Unknown', (22, 30): 'Unknown'}
	stat = f.readline()[7:-1]
	statStr = GetStatStr_SR(stat)

	#altitude {'a1': 'high'}
	alt = f.readline()[9:-1]
	altStr = GetAltStr_SR(alt)

	#currentImage {'a1': None}
	img = f.readline()[13:-1]
	imgStr = GetImgStr_SR(img)

	#realStatus {'w1': 'OK', 'p1': 'OK', 'w2': 'OK', 'a1': 'ok', (22, 30): 'hasDebri'}
	#realPerson {(22, 30): 'p1'}
	#newRobot {1: None}
	f.readline()
	f.readline()
	f.readline()
	
	#weather {(22, 30): 'clear'}
	w = f.readline()[8:-1]
	weatherStr = GetWeatherStr_SR(w)
	record = [locNumbers, medStr, statStr, altStr, imgStr, weatherStr]
	return record

def GetLoadString_SD(s):
	print("s")
	print(s)
	print("s")
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
		res.append('0')
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
		nums.append('0')

	return (" ".join(nums))

def GetAltStr_SR(s):
	d = ast.literal_eval(s)
	nums = []
	for key in d:
		if d[key] == 'high':
			nums.append('1')
		else:
			nums.append('0')

	return (" ".join(nums))

def GetImgStr_SR(s):
	d = ast.literal_eval(s)
	nums = []
	for key in d:
		if d[key] == None:
			nums.append('0 0')
		else:
			d2 = d[key]
			if d2['loc'] != None:
				(l1, l2) = d2['loc']
				nums.append(str(l1) + ' ' + str(l2))
			else:
				nums.append('0 0')
	return (" ".join(nums))

def GetWeatherStr_SR(s):
	d = ast.literal_eval(s)
	nums = []
	#"clear", "rainy", "dustStorm", "foggy"
	for key in d:
		if d[key] == 'clear':
			nums.append('0')
		elif d[key] == 'rainy':
			nums.append('1')
		elif d[key] == 'dustStorm':
			nums.append('2')
		else:
			nums.append('3')

	return (" ".join(nums))


def GetLocStr_SD(s):
	d = ast.literal_eval(s)
	nums = [str(item) for item in d.values()]
	if len(nums) > 4:
		print(" too many robots in SD")
		exit()
	while(len(nums) < 4):
		nums.append('0')
	return (" ".join(nums))

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

def GetPosStr_SD(s):
	d = ast.literal_eval(s)
	pos = [str(item) for item in d.values()]
	for i in range(0, len(pos)):
		if pos[i] not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']:
			if pos[i] == 'r1':
				pos[i] = '12'
			elif pos[i] == 'r2':
				pos[i] = '13'
			elif pos[i] == 'r3':
				pos[i] = '14'
			elif pos[i] == 'r4':
				pos[i] = '15'
			else:
				print(" invalid position in SD ", pos[i])
				exit()
	if len(pos) > 2:
		print(" too many objects in SD")
		exit()
	while(len(pos) < 2):
		pos.append('0')
	return " ".join(pos)

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
		res.append('0')

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
		res.append('0')

	return " ".join(res)

def ReadStateVars_SD(line, f):
	#load {'r1': 'nil', 'r2': 'nil', 'r3': 'nil'}
	print("reading stat vars")
	a1 = line[5:-1]

	#status {'r1': 'busy', 'r2': 'free', 'r3': 'busy'}
	a2 = f.readline()[7:-1]

	#loc {'r1': 2, 'r2': 1, 'r3': 2}
	a3 = f.readline()[4:-1]

	#pos {'o1': 1}
	a4 = f.readline()[4:-1]

	#doorStatus {'d1': 'closed', 'd2': 'closed'}
	a5 = f.readline()[11:-1]

	#doorType {'d1': 'Unknown', 'd2': 'Unknown'}
	a6 = f.readline()[9:-1]

	return [GetLoadString_SD(a1), 
		GetStatusString_SD(a2), 
		GetLocStr_SD(a3), 
		GetPosStr_SD(a4), 
		GetDoorStatusStr_SD(a5), 
		GetDoorTypeStr_SD(a6)]

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
	#loc {'r1': 'base', 'r2': 'z5', 'UAV': 'base'}
	a1 = line[4:-1]

	#charge {'UAV': 80, 'r1': 80, 'r2': 15}
	a2 = f.readline()[7:-1]

	#data {'UAV': 3, 'r1': 3, 'r2': 1}
	a3 = f.readline()[5:-1]

	#pos {'c1': 'base', 'e1': 'base', 'e2': 'base', 'e3': 'base', 'e4': 'base', 'e5': 'base', 'o1': 'UAV'}
	a4 = f.readline()[4:-1]

	#load {'r1': 'nil', 'r2': 'nil', 'UAV': 'o1'}
	a5 = f.readline()[5:-1]

	#storm {'active': True}
	f.readline()

	return [GetLocsStr_EE(a1), 
		GetChargeStr_EE(a2),
		GetChargeStr_EE(a3),
		GetPosStr_EE(a4),
		GetLoadStr_EE(a5),
		] 

domain = None

def AddToRecords(l, new):
	for item in l:
		if new == item:
			print("found match")
			return
	l.append(new)

import argparse

def ConvertToInt(a):
	x = a.split(" ")
	return [float(i) for i in x]

def EncodeState_CR(state):
	a = state.split("\n")
	locs = a[0][4:]
	locNumbers = ConvertToInt(GetNums(locs))

	charge = a[1][6:]
	chargeNumbers = ConvertToInt(GetNums(charge))

	load = a[2][5:]
	loadString = ConvertToInt(GetLoadString(load))

	pos = a[3][4:]
	posString = ConvertToInt(GetPosString(pos))

	emergencyHandling = a[5][18:]
	emergencyString = ConvertToInt(GetEmS(emergencyHandling))

	view = a[6][5:]
	viewString = ConvertToInt(GetViewString(view))

	return locNumbers + chargeNumbers + loadString + posString + emergencyString + viewString

def EncodeState_SD(state):
	a = state.split("\n")
	#load {'r1': 'nil', 'r2': 'nil', 'r3': 'nil'}	
	a1 = a[0][5:]

	#status {'r1': 'busy', 'r2': 'free', 'r3': 'busy'}
	a2 = a[1][7:]

	#loc {'r1': 2, 'r2': 1, 'r3': 2}
	a3 = a[2][4:]

	#pos {'o1': 1}
	a4 = a[3][4:]

	#doorStatus {'d1': 'closed', 'd2': 'closed'}
	a5 = a[4][11:]

	#doorType {'d1': 'Unknown', 'd2': 'Unknown'}
	a6 = a[5][9:]

	return ConvertToInt(GetLoadString_SD(a1)) + ConvertToInt(GetStatusString_SD(a2)) + ConvertToInt(GetLocStr_SD(a3)) + ConvertToInt(GetPosStr_SD(a4)) + ConvertToInt(GetDoorStatusStr_SD(a5)) + ConvertToInt(GetDoorTypeStr_SD(a6))

def EncodeState_SR(state):

	a = state.split("\n")
	#loc {'w1': (7, 24), 'w2': (24, 11), 'p1': (22, 30), 'a1': (23, 15)}

	locs = a[0][4:]
	locNumbers = ConvertToInt(GetLocsSR(locs))

	#hasMedicine {'a1': 0, 'w1': 0, 'w2': 0}
	med = a[1][12:]
	medStr = ConvertToInt(GetMedsSR(med))

	#robotType {'w1': 'wheeled', 'a1': 'uav', 'w2': 'wheeled'}
	#ty = a[2][10:]
	#tyStr = ConvertToInt(GetTypeStr_SR(ty))

	#status {'w1': 'free', 'w2': 'free', 'a1': 'Unknown', 'p1': 'Unknown', (22, 30): 'Unknown'}
	stat = a[3][7:]
	statStr = ConvertToInt(GetStatStr_SR(stat))

	#altitude {'a1': 'high'}
	alt = a[4][9:]
	altStr = ConvertToInt(GetAltStr_SR(alt))

	#currentImage {'a1': None}
	img = a[5][13:]
	imgStr = ConvertToInt(GetImgStr_SR(img))

	#realStatus {'w1': 'OK', 'p1': 'OK', 'w2': 'OK', 'a1': 'ok', (22, 30): 'hasDebri'}
	#realPerson {(22, 30): 'p1'}
	#newRobot {1: None}
	
	#weather {(22, 30): 'clear'}
	w = a[9][8:]
	weatherStr = ConvertToInt(GetWeatherStr_SR(w))

	record = locNumbers + medStr + statStr + altStr + imgStr + weatherStr
	return record

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

def Encode(domain, state, task, mainTask):
	if domain == "CR":
		x = EncodeState_CR(state)
	elif domain == "SR":
		x = EncodeState_SR(state)
	elif domain == "SD":
		x = EncodeState_SD(state)
	elif domain == "EE":
		x = EncodeState_EE(state)
	elif domain == "OF":
		x = EncodeState_OF(state)

	taskCode = taskCodes[domain][task]
	x.append(taskCode)
	mainTaskCode = taskCodes[domain][mainTask]
	x.append(mainTaskCode)
	return x

def Decode(domain, yhat):
	label = GetLabel(yhat)
	for m in methodCodes[domain]:
		if methodCodes[domain][m] == label:
			return m
	return None

def normalize(l):
	l2 = []
	for item in l:
		res = []
		for x in item:
			p = x.split(' ')
			for y in p:
				res.append(float(y))
		l2.append(res)

	n = len(l2)
	sums = [0]*len(l2[0])
	for item in l2:
		for i in range(len(item)):
			sums[i] += item[i]

	means = [x/n for x in sums]

	var = [0]*len(l2[0])
	for item in l2:
		for i in range(len(item)):
			var[i] += (item[i] - means[i])*(item[i] - means[i])/(n-1)

	sigmas = [math.sqrt(x) for x in var]

	#print(l2)
	print(sigmas[-1])
	print(means[-1])

	for item in l2:
		for i in range(len(item)):
			if sigmas[i] != 0:
				item[i] = (item[i] - means[i])/sigmas[i]

	return l2

if __name__ == "__main__":

	argparser = argparse.ArgumentParser()
	argparser.add_argument("--domain", help="domain in ['CR', 'SD', SR', EE']",
                           type=str, required=True)
	argparser.add_argument("--dataFrom", help="actor (a) or planner (p) ?",
                           type=str, required=True)
	argparser.add_argument("--learnWhat", help="method (m) or efficiency(e)",
						   type=str, required=True)
	args = argparser.parse_args()
	domain = args.domain

	if args.dataFrom == 'a':
		suffix = 'actor'
	elif args.dataFrom == 'p':
		suffix = 'planner'
	else:
		print("Invalid value for --dataFrom")
		exit()

	learnWhat = args.learnWhat
	if learnWhat == "m":
		fname = "{}_data_{}.txt".format(domain, suffix)
		fwrite = open("numericData_{}_{}.txt".format(domain, suffix), "w")
	elif learnWhat == "e":
		fname = "{}_data_eff_{}.txt".format(domain, suffix)
		fwrite = open("numericData_eff_{}_{}.txt".format(domain, suffix), "w")
	
	f = open(fname)
	
	recordL = []
	line = f.readline()
	while(line != ""):
		if domain == "CR":
			record = ReadStateVars_CR(line, f)
		elif domain == "SR":
			record = ReadStateVars_SR(line, f)
		elif domain == "SD":
			record = ReadStateVars_SD(line, f)
		elif domain == "EE":
			record = ReadStateVars_EE(line, f)

		task = f.readline()[0:-1]
		mainTask = f.readline()[0:-1]
		method = f.readline()[0:-1]

		taskCode = taskCodes[domain][task]
		mainTaskCode = taskCodes[domain][mainTask]
		methodCode = methodCodes[domain][method]

		record.append(str(taskCode))
		record.append(str(mainTaskCode))

		eff = f.readline()[0:-1]

		if learnWhat == "m":
			record.append(str(methodCode))
		else:
			record.append(str(methodCode))

			if domain == "SD":
				for i in range(5):
					actingTreeNode = f.readline()[0:-1]
				#record.append(str(actingNodeCodes[domain][actingTreeNode]))
			if eff == "inf":
				eff = 1
			record.append(str(eff))


		if domain == "EE" and (taskCode == 1 or taskCode == 4):
			pass
		else:
			AddToRecords(recordL, record)
		
		line = f.readline()
	f.close()
	if learnWhat == "e":
		recordN = normalize(recordL)
		for item in recordN:
			fwrite.write(" ".join([str(i) for i in item]) + "\n")
	else:
		for item in recordL:
			fwrite.write(" ".join(item) + "\n")

