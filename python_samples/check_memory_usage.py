import os
import psutil
import multiprocessing
import time

def Test1():
	process = psutil.Process(os.getpid())
	print("Inside test1 1st", process.memory_info().rss/1024/1024)
	s = 5
	print(s)
	print("Inside test1 2nd ", process.memory_info().rss/1024/1024)

	Test2()
	#y = 1
	y = 4
	y2= 5
	y4=10
	y7='sdkfjnsf'
	print("Inside test1 3rd ", process.memory_info().rss/1024/1024)

	
def Test2():
	x = 2
	print("here x ", x)
	process = psutil.Process(os.getpid())
	print("Inside test 2 ", process.memory_info().rss/1024/1024)

def p2Main():
	time.sleep(10)
	print("p2 is ending")

def p1Main():
	p2 = multiprocessing.Process(target=p2Main)
	p2.start()

if __name__=="__main__":

	#p = multiprocessing.Process(target=Test1)
	#p.start()
	#p.join()
	#process = psutil.Process(os.getpid())
	#print("In main", process.memory_info().rss/1024)

	p1 = multiprocessing.Process(target=p1Main)
	p1.start()
	p1.join(5)
	print(p1.is_alive())
	p1.terminate()
