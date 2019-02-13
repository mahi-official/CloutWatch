import queue
import random

q = queue.Queue()

for x in range(50):
	templist = []
	for z in range(99999):
		templist.append(random.randint(1,99))
	q.put(templist)

while not q.empty():
	print(q.get())