import torch
import math
import ast
import numpy as np
import pdb

def ReadStateVars(line, f, count):
	for i in range(count):
		f.readline()

domain = None

import argparse


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

def PrintEffIntervals(eMax, l):
	
	widths = []
	sum = 0

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

	counts = [0]*numIntervals[domain]

	for item in l:
		for i in range(numIntervals[domain]):
			if item < intervalLimits[i]:
				counts[i-1] += 1
				break

	sanitySum = 0
	for i in counts:
		sanitySum += i
	print(counts, sanitySum)

if __name__ == "__main__":

	argparser = argparse.ArgumentParser()
	argparser.add_argument("--domain", help="domain in ['CR', 'SD', SR', EE']",
                           type=str, required=True)
	argparser.add_argument("--dataFrom", help="actor (a) or planner (p) ?",
                           type=str, required=True)
	argparser.add_argument("--howMany", help="Number of training data items to read?",
                           type=int, required=True)

	args = argparser.parse_args()
	domain = args.domain
	howMany = args.howMany

	if args.dataFrom == 'a':
		suffix = 'actor'
	elif args.dataFrom == 'p':
		suffix = 'planner'
	else:
		print("Invalid value for --dataFrom")
		exit()

	fname = "../../raeResults/learning/{}/{}_data_eff_{}_without_dup.txt".format(domain, domain, suffix)
	recordL = []
	countL = []

	f = open(fname)
	
	line = f.readline()
	eMax = 0

	while(line != ""):
		if domain == "CR":
			ReadStateVars(line, f, 6)
		elif domain == "SR":
			ReadStateVars(line, f, 9)
		elif domain == "SD":
			ReadStateVars(line, f, 5)
		elif domain == "EE":
			ReadStateVars(line, f, 5)

		task = f.readline()[0:-1]
		mainTask = f.readline()[0:-1]
		method = f.readline()[0:-1]

		eff = float(f.readline()[0:-1])

		if eff == float("inf"):
			eff = 1

		if eff > eMax:
			eMax = eff

		found = False
		for item in recordL:
			if item != 0 and abs(item - eff)/abs(item) < 0.0001:
				found = True
			elif item == 0:
				if eff == 0:
					found = True
		if found == False:
			recordL.append(eff)

		if len(recordL) % 100 == 0:
			print(len(recordL))
		
		if len(recordL) > howMany:
			break
		line = f.readline()
	f.close()

	PrintEffIntervals(eMax, recordL)
