import argparse

if __name__=="__main__":
	argparser = argparse.ArgumentParser()
	argparser.add_argument("--domain", help="domain in ['CR', 'SD', SR', 'EE', 'OF']",
                           type=str, required=True)

	args = argparser.parse_args()
	domain = args.domain
	f = open("../../raeResults/AIJ2020/learning/{}/{}_data_eff_planner.txt".format(domain, domain), "r")
	fw = open("../../raeResults/AIJ2020/learning/{}/{}_data_eff_planner_without_dup.txt".format(domain, domain), "w")

	line = f.readline()
	records = []
	count = 0

	lim  = { # num of stat vars + 3
		"CR": 10,
		"SR": 13, 
		"SD": 9,
		"EE": 9,
	}
	nLine = 0
	while(line != ""):
		s = line
		for i in range(lim[domain] - 1):
			s += f.readline()
			nLine += 1
		e = f.readline()
		if e == "UNK\n":
			unk = True
		else:
			unk = False
			e = float(e)
			s += str(e) + "\n"
		nLine += 1
		#print(s)
		#count += 1
		#if count > 5:
		#	break
		if s not in records and unk == False:
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