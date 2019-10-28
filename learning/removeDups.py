if __name__=="__main__":
	domain = "SD"
	f = open("../../raeResults/learning/{}/{}_data_eff_planner.txt".format(domain, domain), "r")
	fw = open("../../raeResults/learning/{}/{}_data_eff_planner_without_dup.txt".format(domain, domain), "w")

	line = f.readline()
	records = []
	count = 0

	lim  = {
		"SR": 13,
		"SD": 9,
	}
	lineN = 0
	while(line != ""):
		s = line
		for i in range(lim[domain] - 1):
			s += f.readline()
			lineN += 1
		print(lineN)
		e = f.readline()
		if e == "UNK\n":
			unk = True
		else:
			unk = False
			e = float(e)
			s += str(e) + "\n"
		lineN += 1
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
		lineN += 1

	f.close()
	fw.close()