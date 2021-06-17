import ast
from learning.convertDataFormat import ConvertToOneHot, ConvertToOneHotHelper

def ConvertToInt(a):
	x = a.split(" ")
	return [float(i) for i in x]

def GetStrDict(d1):
	d = {}
	for key in d1:
		d[str(key)] = d1[key]
	return d

def GetLocsSR(s):
	d = ast.literal_eval(s)
	nums = []
	for key in sorted(d.keys()):
		(x, y) = d[key]
		nums.append(str(int(x)-1))
		nums.append(str(int(y)-1))

	if len(nums) > 8:
		print("error")
		exit()

	while(len(nums) < 8):
		nums.append('0')
		print("appending 0")
	return " ".join(nums)

def GetMedsSR(s):
	d = ast.literal_eval(s)
	nums = []
	for key in sorted(d.keys()):
		val = d[key]
		nums.append(str(val))

	if len(nums) > 4:
		print("error")
		exit()

	while(len(nums) < 4):
		nums.append('0')
	return " ".join(nums)

def GetStatStr_SR(s):
	d = GetStrDict(ast.literal_eval(s))

	nums = []

	for key in sorted(d.keys()):
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
			nums.append('0')
		else:
			print("unknown status in SR ", d[key])
			exit()


	return (" ".join(nums))

def GetAltStr_SR(s):
	d = ast.literal_eval(s)
	nums = []
	for key in sorted(d.keys()):
		if d[key] == 'high':
			nums.append('1')
		else:
			nums.append('0')

	return (" ".join(nums))

def GetImgStr_SR(s):
	d = ast.literal_eval(s)
	nums = []
	for key in sorted(d.keys()):
		if d[key] == None:
			nums.append('0 0')
		else:
			d2 = d[key]
			if d2['loc'] != None:
				(l1, l2) = d2['loc']
				#nums.append(str(int(l1/6)) + ' ' + str(int(l2/6)))
				nums.append('1 1')
			else:
				nums.append('0 0')
	return (" ".join(nums))

def GetWeatherStr_SR(s):
	d = GetStrDict(ast.literal_eval(s))
	nums = []
	#"clear", "rainy", "dustStorm", "foggy"
	for key in sorted(d.keys()):
		if d[key] == 'clear':
			nums.append('0')
		elif d[key] == 'rainy':
			nums.append('1')
		elif d[key] == 'dustStorm':
			nums.append('2')
		else:
			nums.append('3')

	return (" ".join(nums))

def GetRobotStr_SR(s):
	d = GetStrDict(ast.literal_eval(s))
	nums = []
	#"w1", "w2", "None"
	for key in sorted(d.keys()):
		#print(d[key])
		if d[key] == None:
			nums.append('0')
		elif d[key] == 'w1':
			nums.append('1')
		elif d[key] == 'w2':
			nums.append('2')
		else:
			print("error  in robot str ")
			exit()

	return (" ".join(nums))

def ReadTaskAndArgs_SR(taskAndArgs):
	params = taskAndArgs.split(' ')
	task = params[0]
	if task == "getRobot":
		res = [0, 0, 0]
	else:
		robotStr = params[1]
		robot = robotStr[2:4]
		#print(robot)
		if robot == 'w1':
			res = [1, 0, 0]
		elif robot == 'w2':
			res =  [0, 1, 0]
		elif robot == 'a1':
			res =  [0, 0, 1]
		else:
			print(robot)
	if task == "moveTo" or task == "survey":
		targetx = int(int(params[2][1:-1]) - 1)
		targety = int(int(params[3][0:-2]) - 1)
		#print(targetx, targety)
		res += ConvertToOneHotHelper(targetx, 30) + ConvertToOneHotHelper(targety, 30)
	else:
		res += [0]*60
	return res

def ReadStateVars_SR(line, f):
	#loc {'w1': (7, 24), 'w2': (24, 11), 'p1': (22, 30), 'a1': (23, 15)}

	for i in range(0, 10):
		if line[0:3] == "loc":
			a1 = line[4:-1]
			a1 = GetLocsSR(a1).split(' ')
			a1H = ConvertToOneHot(a1, 'loc', 'SR')
			a1Hs = [str(i) for i in a1H]

		elif line[0:3] == "has":
			#hasMedicine {'a1': 0, 'w1': 0, 'w2': 0}
			a2 = line[12:-1]
			a2 = GetMedsSR(a2).split(' ')
			a2H = ConvertToOneHot(a2, 'medicine', 'SR')
			a2Hs = [str(i) for i in a2H]

		elif line[0:3] == "sta":
			#status {'w1': 'free', 'w2': 'free', 'a1': 'Unknown', 'p1': 'Unknown', (22, 30): 'Unknown'}
			a4 = line[7:-1]
			a4 = GetStatStr_SR(a4).split(' ')
			a4H = ConvertToOneHot(a4, 'status', 'SR')
			a4Hs = [str(i) for i in a4H]

		elif line[0:3] == "alt":
			#altitude {'a1': 'high'}
			a5 = line[9:-1]
			a5 = GetAltStr_SR(a5).split(' ')
			a5H = ConvertToOneHot(a5, 'altitude', 'SR')
			a5Hs = [str(i) for i in a5H]

		elif line[0:3] == "cur":
			#currentImage {'a1': None}
			a6 = line[13:-1]
			a6 = GetImgStr_SR(a6).split(' ')
			a6H = ConvertToOneHot(a6, 'currentImage', 'SR')
			a6Hs = [str(i) for i in a6H]

		elif line[0:3] == "wea":
			#weather {(22, 30): 'clear'}
			a7 = line[8:-1]
			a7 = GetWeatherStr_SR(a7).split(' ')
			a7H = ConvertToOneHot(a7, 'weather', 'SR')
			a7Hs = [str(i) for i in a7H]
		
		elif line[0:3] == "new":
			#newRobot {1: None}
			a8 = line[9:-1]
			a8 = GetRobotStr_SR(a8).split(' ')
			a8H = ConvertToOneHot(a8, 'robot', 'SR')
			a8Hs = [str(i) for i in a8H]
		else:
			pass
			#robotType {'w1': 'wheeled', 'a1': 'uav', 'w2': 'wheeled'}
			#tyStr = GetTypeStr_SR(ty)
			#realStatus {'w1': 'OK', 'p1': 'OK', 'w2': 'OK', 'a1': 'ok', (22, 30): 'hasDebri'}
			#realPerson {(22, 30): 'p1'}

		if i < 9:
			line = f.readline()
	
	return a1Hs + a2Hs + a4Hs + a5Hs + a6Hs + a7Hs + a8Hs

def EncodeState_SR(state):

	a = state.split("\n")
	
	#loc {'w1': (7, 24), 'w2': (24, 11), 'p1': (22, 30), 'a1': (23, 15)}
	a1 = a[0][4:]
	a1H = ConvertToOneHot(ConvertToInt(GetLocsSR(a1)), 'loc', 'SR')

	#hasMedicine {'a1': 0, 'w1': 0, 'w2': 0}
	a2 = a[1][12:]
	a2H = ConvertToOneHot(ConvertToInt(GetMedsSR(a2)), 'medicine', 'SR')

	#robotType {'w1': 'wheeled', 'a1': 'uav', 'w2': 'wheeled'}
	#ty = a[2][10:]
	#tyStr = ConvertToInt(GetTypeStr_SR(ty))

	#status {'w1': 'free', 'w2': 'free', 'a1': 'Unknown', 'p1': 'Unknown', (22, 30): 'Unknown'}
	a3 = a[3][7:]
	a3H = ConvertToOneHot(ConvertToInt(GetStatStr_SR(a3)), 'status', 'SR')

	#altitude {'a1': 'high'}
	a4 = a[4][9:]
	a4H = ConvertToOneHot(ConvertToInt(GetAltStr_SR(a4)), 'altitude', 'SR')

	#currentImage {'a1': None}
	a5 = a[5][13:]
	a5H = ConvertToOneHot(ConvertToInt(GetImgStr_SR(a5)), 'currentImage', 'SR')

	#realStatus {'w1': 'OK', 'p1': 'OK', 'w2': 'OK', 'a1': 'ok', (22, 30): 'hasDebri'}
	#realPerson {(22, 30): 'p1'}
	#newRobot {1: None}
	a8 = a[8][9:]
	a8H = ConvertToOneHot(ConvertToInt(GetRobotStr_SR(a8)), 'robot', 'SR')
	
	#weather {(22, 30): 'clear'}
	a6 = a[9][8:]
	a6H = ConvertToOneHot(ConvertToInt(GetWeatherStr_SR(a6)), 'weather', 'SR')

	return a1H + a2H + a3H + a4H + a5H + a6H + a8H

