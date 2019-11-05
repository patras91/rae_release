import torch
import math
import ast
import numpy as np

def ConvertToOneHotHelper(label, upper):
	onehot = np.zeros(upper)
	onehot[int(label)]=1
	return list(onehot)

def ConvertToOneHot(a_int, varName, domain):
	aH = []
	for i in a_int:
		aH += ConvertToOneHotHelper(i, UpperLimits[domain][varName])
	return aH

from encoder_CR import *
from encoder_SR import *
from encoder_SD import *
from encoder_EE import *
from encoder_OF import *

def GetLabel(yhat):
    r, predicted = torch.max(yhat, 0)
    return predicted.long()

UpperLimits = {
	"CR": {
		"loc": 11,
		"charge": 5,
		"load": 4,
		"pos": 13,
		"emergencyHandling": 2,
		"view": 2,
	},
	"SR": {
		"loc": 30, #31
		"medicine": 6,
		"weather": 4,
		"status": 9,
		"currentImage": 2, #31
		"altitude": 2,
		"robot": 3,
	},
	"SD": {
		"loc": 8,
		"pos": 12,
		"status": 3,
		"doorType": 4,
		"doorStatus": 4,
		"load": 5,
	}, 
	"EE": {
		"loc": 8,
		"charge": 11, # 11 unit blocks 0 to 100
		"data": 5, # 0 to 4
		"pos": 11, # 8 locations + 3 robots
		"load": 8, # 5 equipments + 1 charger + nil
	},
	"OF": {
		"OBJECTS": 2,
		"OBJ_WEIGHT": 15,
		"OBJ_CLASS": 5,
		"loc": 15,
		"busy": 2,
	}
}

intervals = {
	# CR 100
	# SD 75
	# SR 10
	"CR": [0, 3.991874036777851e-05, 8.183341775394595e-05, 0.00012584382900942176, 0.00017205476082767136, 0.00022057623923683347, 0.0002715237915664537, 0.0003250187215125549, 0.0003811883979559612, 0.00044016655822153776, 0.0005020936265003931, 0.0005671170481931913, 0.0006353916409706295, 0.0007070799633869394, 0.0007823527019240649, 0.0008613890773880468, 0.0009443772716252277, 0.0010315148755742677, 0.0011230093597207596, 0.001219078568074576, 0.0013199512368460835, 0.0014258675390561662, 0.001537079656376753, 0.0016538523795633694, 0.0017764637389093164, 0.0019052056662225607, 0.0020403846899014672, 0.002182322664764319, 0.0023313575383703137, 0.0024878441556566077, 0.002652155103807217, 0.0028246815993653563, 0.0030058344197014027, 0.0031960448810542516, 0.003395765865474743, 0.0036054728991162586, 0.0038256652844398504, 0.004056867289029622, 0.004299629393848882, 0.004554529603909104, 0.004822174824472338, 0.005103202306063734, 0.005398281161734699, 0.005708113960189213, 0.006033438398566452, 0.006375029058862554, 0.00673369925217346, 0.007110302955149912, 0.0075057368432751865, 0.007920942425806725, 0.00835690828746484, 0.008814672442205861, 0.009295324804683933, 0.009800009785285908, 0.010329929014917982, 0.01088634420603166, 0.011470580156701021, 0.012084027904903852, 0.012728148040516824, 0.013404474182910445, 0.014114616632423747, 0.014860266204412713, 0.01564319825500113, 0.016465276908118963, 0.01732845949389269, 0.018234801208955105, 0.019186460009770638, 0.02018570175062695, 0.021234905578526076, 0.02233656959782016, 0.023493316818078945, 0.02470790139935067, 0.025983215209685984, 0.027322294710538063, 0.028728328186432745, 0.03020466333612216, 0.03175481524329605, 0.03338247474582863, 0.03509151722348784, 0.03688601182503001, 0.03877023115664929, 0.04074866145484954, 0.042826013267959796, 0.045007232671725565, 0.047297513045679626, 0.049702307438331386, 0.05222734155061574, 0.05487862736851431, 0.05766247747730781, 0.06058552009154098, 0.06365471483648581, 0.06687736931867788, 0.07026115652497955, 0.07381413309159632, 0.07754475848654392, 0.0814619151512389, 0.08557492964916863, 0.08989359487199484, 0.09442819335596236, 0.09918952176412826, 1],
	"SR": [0, 0.00015524707093654436, 0.000426929445075497, 0.0009023735998186641, 0.0017344008706192066, 0.0031904485945201556, 0.0057385321113468165, 0.010197678265793472, 0.018001184036075122, 0.03165731913406801],
	"SD": [0, 3.489955672036314e-06, 7.398706024716986e-06, 1.1776506419719338e-05, 1.6679642862121975e-05, 2.217115567761293e-05, 2.8321650030962798e-05, 3.5210203706714654e-05, 4.292538382355673e-05, 5.156638555441986e-05, 6.124430749298656e-05, 7.208358006418127e-05, 8.422356534391934e-05, 9.782034885722598e-05, 0.00011304874639212942, 0.00013010455163122128, 0.00014920705349900416, 0.000170601855590921, 0.00019456403393386783, 0.0002214016736779683, 0.00025145983019136085, 0.0002851249654863605, 0.0003228299170167601, 0.0003650594627308077, 0.000412356553930541, 0.0004653292960742423, 0.0005246587672751877, 0.0005911077750202466, 0.0006655306636947125, 0.0007488842990101144, 0.0008422403705633646, 0.0009467991707030047, 0.0010639050268594016, 0.0011950635857545663, 0.0013419611717171507, 0.0015064864679952452, 0.0016907547998267112, 0.001897135331477953, 0.002128281526927344, 0.0023871652658306614, 0.0026771150534023774, 0.003001858815482699, 0.0033655718290126597, 0.0037729304041662155, 0.004229172008338198, 0.004740162605010818, 0.005312472073284153, 0.005953458677750289, 0.00667136367475236, 0.007475417271394681, 0.00837595729963408, 0.009384562131262207, 0.010514199542685709, 0.011779393443480031, 0.013196410612369673, 0.014783469841526072, 0.01656097617818124, 0.018551783275235025, 0.020781487223935267, 0.023278755646479538, 0.02607569627972912, 0.029208269788968653, 0.03271675211931693, 0.036646252329307, 0.04104729256449588, 0.045976457627907426, 0.051497122498928356, 0.057680267154471804, 0.06460538916868046, 0.07236152582459415, 0.0810483988792175, 0.09077769670039565, 0.10167451026011518, 0.11387894144700104, 0.12754790437631322, 1],
	"EE": [0, 0.00012771268983702522, 0.00026181101416590166, 0.000402614254711222, 0.0005504576572838083, 0.0007056932299850239, 0.0008686905813213004, 0.0010398378002243907, 0.0012195423800726356, 0.0014082321889132927, 0.0016063564881959825, 0.001814387002442807, 0.0020328190424019725, 0.0022621726843590965, 0.002502994008414077, 0.002755856398671806, 0.0030213619084424217, 0.0033001426937015682, 0.003592862518223672, 0.003900218333971881, 0.0042229419405075, 0.0045618017273699, 0.004917604503575421, 0.005291197418591217, 0.005683469979357803, 0.006095356168162719, 0.00652783666640788, 0.006981941189565299, 0.00745875093888059, 0.007959401175661645, 0.008485083924281753, 0.009037050810332866, 0.009616616040686535, 0.010225159532557888, 0.010864130199022808, 0.011535049398810974, 0.012239514558588549, 0.012979202976355003, 0.01375587581500978, 0.014571382295597294, 0.015427664100214185, 0.01632675999506192, 0.017270810684652044, 0.018262063908721673, 0.01930287979399478, 0.020395736473531545, 0.021543235987045148, 0.022748110476234432, 0.02401322868988318, 0.025341602814214364, 0.026736395644762108, 0.02820092811683724, 0.02973868721251613, 0.03135333426297896, 0.033048713665964936, 0.03482886203910021, 0.03669801783089225, 0.03866063141227389, 0.04072137567272461, 0.042885157146197866, 0.04515712769334479, 0.04754269676784906, 0.050047544296078536, 0.05267763420071949, 0.05543922860059249, 0.05833890272045914, 0.061383560546319126, 0.06458045126347212, 0.06793718651648276, 0.07146175853214393, 0.07516255914858815, 0.07904839979585458, 0.08312853247548434, 0.08741267178909558, 0.09191101806838739, 0.09663428166164378, 0.101593708434563, 0.10680110654612818, 0.11226887456327161, 0.11801003098127222, 0.12403824522017286, 0.13036787017101853, 0.1370139763694065, 0.14399238787771385, 0.15131971996143656, 0.15901341864934543, 0.16709180227164974, 0.17557410507506926, 0.18448052301865975, 0.19383226185942976, 0.20365158764223829, 0.21396187971418723, 0.22478768638973362, 0.23615478339905735, 0.24809023525884724, 0.2606224597116266, 0.273781295387045, 0.2875980728462343, 0.30210568917838304, 0.31733868632713924, 1],
}
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
	},
	"OF": {
	"OrderStart_Method1": 0,
	"Order_Method1": 1,
	"Order_Method2": 2,
	"PickupAndLoad_Method1": 3,
	"UnloadAndDeliver_Method1": 4,
	"MoveToPallet_Method1": 5,
	}
}

numMethods = {
	"CR": 10,
	"SR": 16,
	"EE": 17,	
	"SD": 9,
	"OF": 6,
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
	},
	"OF": {
	'orderStart': 1,
	'order': 2,
	'pickupAndLoad': 3,
	'unloadAndDeliver': 4,
	'moveToPallet': 5,
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


domain = None

def AddToRecordsAllTogether(l, new):
	if len(l) % 100 == 0:
		print(len(l))
	for i in range(len(l)):
		item = l[i]
		if new[0:-1] == item[0:-1]:
			n = AddToRecordsAllTogether.Counts[i]
			eff = (float(new[-1]) + n * float(item[-1]))/(n+1)
			item[-1] = str(eff)
			#print("Updated ", i)
			AddToRecordsAllTogether.Counts[i] += 1
			return
	l.append(new)
	AddToRecordsAllTogether.Counts.append(1)
AddToRecordsAllTogether.Counts = []

def AddToRecordsTaskBased(l, new, task):
	if task not in l:
		l[task] = []
		AddToRecordsTaskBased.Counts[task] = []
	for i in range(len(l[task])):
		item = l[task][i]
		if item[0:-1] == new[0:-1]:
			n = AddToRecordsTaskBased.Counts[task][i]
			item[-1] = str((float(new[-1]) + n * float(item[-1]))/(n+1))
			print(" item found in records for ", task)
			AddToRecordsTaskBased.Counts[task][i] += 1
			return
	l[task].append(new)
	AddToRecordsTaskBased.Counts[task].append(1)
AddToRecordsTaskBased.Counts = {}

import argparse

def ConvertToInt(a):
	x = a.split(" ")
	return [float(i) for i in x]

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

def EncodeForHeuristic(domain, state, method, taskAndArgs):
	if domain == "CR":
		x = EncodeState_CR(state)
	elif domain == "SR":
		x = EncodeState_SR(state)
		x += ReadTaskAndArgs_SR(taskAndArgs)
	elif domain == "SD":
		x = EncodeState_SD(state)
		x += ReadTaskAndArgs_SD(taskAndArgs)
	elif domain == "EE":
		x = EncodeState_EE(state)
		x += ReadTaskAndArgs_EE(taskAndArgs)
	elif domain == "OF":
		x = EncodeState_OF(state)

	methodCode = ConvertToOneHotHelper(methodCodes[domain][method], numMethods[domain])
	x += methodCode
	return x

def DecodeForHeuristic(domain, interval):
	num = GetLabel(interval)
	return (intervals[domain][num] + intervals[domain][num + 1])/2

	#num = GetLabel(interval)
	#return (num +0.5)*0.0010419 

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

eL = []
maxE = 0
def AddToeL(e):
	e1 = float(e) * 10000
	e2 = round(e1)/10000
	if e2 not in eL:
		global maxE
		if e2 > maxE:
			print(e2)
			maxE = e2
		eL.append(e2)

def DivideIntoIntervalsEqual(l):
	maxE = 0
	for item in l:
		e = float(item[-1])
		if e > maxE:
			maxE = e

	step = maxE/100

	print("step = ", step, " maxE = ", maxE)

	for item in l:
		e = float(item[-1])
		i = math.floor(e/step)
		item[-1] = str(i)
	return l

def DivideIntoIntervals(l, domain):
	eMax = 0
	for item in l:
		e = float(item[-1])
		if e > eMax:
			eMax = e

	numIntervals = {
		"CR": 100,
		"SR": 10,
		"SD": 75,
		"EE": 200,
	}

	factor = {
		"CR": 1.05,
		"SR": 1.75,
		"SD": 1.12,
		"EE": 1.05,
	}

	widths = []
	sum = 0
	for i in range(numIntervals[domain]):
		x = pow(factor[domain], i) 
		widths.append(x)
		sum += x

	intervalLimits = [0]*numIntervals[domain]

	num = 0
	for i in range(numIntervals[domain]):
		intervalLimits[i] = num
		widths[i] *= eMax/sum
		num += widths[i]

	print(intervalLimits)

	for item in l:
		e = float(item[-1])
		item[-1] = numIntervals[domain] - 1
		for i in range(numIntervals[domain]):
			if e < intervalLimits[i]:
				item[-1] = str(i-1)
				break
	return l

def ReadTaskAndArgs(taskAndArgs, domain):
	if domain == "CR":
		return []
	elif domain == "SR":
		return ReadTaskAndArgs_SR(taskAndArgs)
	elif domain == "SD":
		return ReadTaskAndArgs_SD(taskAndArgs)
	elif domain == "EE":
		return ReadTaskAndArgs_EE(taskAndArgs)

if __name__ == "__main__":

	argparser = argparse.ArgumentParser()
	argparser.add_argument("--domain", help="domain in ['CR', 'SD', SR', EE']",
                           type=str, required=True)
	argparser.add_argument("--dataFrom", help="actor (a) or planner (p) ?",
                           type=str, required=True)
	argparser.add_argument("--learnWhat", help="method (m) or efficiency(e)",
						   type=str, required=True)
	argparser.add_argument("--taskBased", help="divide based on tasks (y) or not(n)?",
						   type=str, required=True)
	argparser.add_argument("--howMany", help="how many training data records to read?",
						   type=int, required=True)
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
		assert(args.taskBased == "n")
		fname = "../../raeResults/learning/{}/{}_data_{}.txt".format(domain, domain, suffix)
		fwrite = open("../../raeResults/learning/{}/numericData_{}_{}.txt".format(domain, domain, suffix), "w")
		recordL = []
	elif learnWhat == "e":
		fname = "../../raeResults/learning/{}/{}_data_eff_{}_without_dup.txt".format(domain, domain, suffix)
		taskBased = args.taskBased
		if taskBased == 'n':
			fwrite = open("../../raeResults/learning/{}/numericData_eff_{}_{}.txt".format(domain, domain, suffix), "w")
			recordL = []
		else:
			fwrite = {}
			recordL = {}
			for task in taskCodes[domain]:
				pass
				fwrite[task] = open("../../raeResults/learning/{}/numericData_eff_{}_{}_task_{}.txt".format(domain, domain, suffix, task), "w")
	f = open(fname)
	
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

		taskAndArgs = f.readline()[0:-1]
		mainTask = f.readline()[0:-1]
		method = f.readline()[0:-1]

		#taskCode = taskCodes[domain][taskAndArgs]
		mainTaskCode = taskCodes[domain][mainTask]
		methodCode = methodCodes[domain][method]
		
		methodCode = ConvertToOneHotHelper(methodCode, numMethods[domain])

		methodCode = [str(i) for i in methodCode]

		record += ReadTaskAndArgs(taskAndArgs, domain)
		#record.append(str(mainTaskCode))

		eff = f.readline()[0:-1]

		if learnWhat == "m":
			record.append(str(methodCode))
		else:
			record += methodCode
			if eff == "inf":
				eff = 1
			record.append(str(eff))
		if taskBased == "y":
			AddToRecordsTaskBased(recordL, record, task)
		else:
			AddToRecordsAllTogether(recordL, record)
			if len(recordL) % 100 == 0:
				print(len(recordL))
			if len(recordL) > args.howMany:
				break

		line = f.readline()
	f.close()

	if learnWhat == "e":
		if taskBased == "y":
			for task in recordL:
				for item in recordL[task]:
					pass
					fwrite[task].write(" ".join([str(i) for i in item]) + "\n")
		else:
			recordN = DivideIntoIntervals(recordL, domain)
			for item in recordN:
				pass
				fwrite.write(" ".join([str(i) for i in item]) + "\n")
	else:
		for item in recordL:
			pass
			fwrite.write(" ".join(item) + "\n")
	print(len(recordN[0]))

