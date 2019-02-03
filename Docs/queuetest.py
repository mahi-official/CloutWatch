import queue
import random

q = queue.Queue()

for i in range(5):
	tempList = []
	for x in range(15):
		tempList.append(random.randint(0,15))

	q.put(tempList)

while not q.empty():
	print(q.get())