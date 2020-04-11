import argparse
from paramInfo import params

def Process_LearnH(domain):
	f = open("../../raeResults/learning/{}/{}_data_eff_planner.txt".format(domain, domain), "r")
	fw = open("../../raeResults/learning/{}/{}_data_eff_planner_without_dup.txt".format(domain, domain), "w")

	line = f.readline()
	records = []
	count = 0

	blockSize  = { # num of stat vars + 3
		"CR": 10,
		"SR": 13, 
		"SD": 9,
		"EE": 9,
		"OF": 12,
	}
	nLine = 0
	while(line != ""):
		s = line
		for i in range(blockSize[domain] - 1):
			s += f.readline()
			nLine += 1
		e = f.readline()
		unk = True if e == "UNK\n" else False
		if not unk:
			e = float(e)
			s += str(e) + "\n"
		nLine += 1
		#print(s)
		#count += 1
		#if count > 5:
		#	break
		if s not in records and not unk:
			records.append(s)
			fw.write(s)
			if len(records) % 1000 == 0:
				print(len(records))
		else:
			count += 1
			if count % 1000 == 0:
				print("dup = ", count)
		line = f.readline()
		nLine += 1

	f.close()
	fw.close()

def Process_LearnMI(domain):
	f = open("../../raeResults/AIJ2020/learning/{}/{}_data_planner_mi.txt".format(domain, domain), "r")
	fw = open("../../raeResults/AIJ2020/learning/{}/{}_data_planner_mi_without_dups.txt".format(domain, domain), "w")

	line = f.readline()
	records = []
	nDup = 0

	blockSize  = { # num of stat vars + 3
		"SD": 9,
		"OF": 12,
	}

	nLine = 0
	while(line != ""):
		s = line
		for i in range(blockSize[domain] - 2):
			s += f.readline()
			nLine += 1
		
		mLine = f.readline()
		s += mLine
		mParts = mLine.split(' ')
		mName = mParts[0]

		e = f.readline() # the efficiency
		nLine += 1
		
		if s not in records and mName in params[domain]:
			records.append(s)
			fw.write(s+e)
			if len(records) % 1000 == 0:
				print(len(records))
		else:
			nDup += 1
			if nDup % 1000 == 0:
				print("dup = ", nDup)

		line = f.readline()
		nLine += 1

	f.close()
	fw.close()

if __name__=="__main__":
	argparser = argparse.ArgumentParser()
	argparser.add_argument("--domain", help="domain in ['CR', 'SD', SR', 'EE', 'OF']",
                           type=str, required=True)
	argparser.add_argument("--lMode", help="['learnH', 'learnMI']",
                           type=str, required=True)

	args = argparser.parse_args()
	domain, lMode = args.domain, args.lMode

	if lMode == "learnH":
		Process_LearnH(domain)
	elif lMode == "learnMI":
		Process_LearnMI(domain)
	else:
		print("Incorrect learning mode: must be learnH or learnMI")
	