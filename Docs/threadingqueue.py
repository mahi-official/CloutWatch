import queue
import random
import threading

def calculation(array):
	num = 1
	for i in array:
		num =+ num*i
	print(threading.current_thread(), " is finished! Q: ", q.qsize())


q = queue.Queue()

for x in range(50):
	templist = []
	for z in range(99999):
		templist.append(random.randint(1,99))
	q.put(templist)
	print("Making queue: ", q.qsize())

threads = []
while not q.empty():
	if(threading.active_count() <= 5):
		print(threading.active_count())
		t = threading.Thread(target=calculation, args=(q.get(),))
		threads.append(t)
		t.start()


