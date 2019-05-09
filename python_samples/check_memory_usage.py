import os
import psutil
import multiprocessing

def Test1():
	s = 5
	print(s)
	process = psutil.Process(os.getpid())
	print("Inside test1", process.memory_info().rss/1024)

if __name__=="__main__":
	p = multiprocessing.Process(target=Test1)
	p.start()
	p.join()
	#process = psutil.Process(os.getpid())
	#print("In main", process.memory_info().rss/1024)

