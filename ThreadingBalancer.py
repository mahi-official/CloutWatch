import threading
import SNike
import queue
import time
import errorLog

threads = []
q = queue.Queue()



def addThread():
	while True:
		while not q.empty():
			if(threading.active_count() <= 6):
				qItem = q.get()
				origin, args = qItem[0], qItem[1]
				if(origin == "SNike"):
					t = threading.Thread(target=SNike.getShoeInfo, args=(args[0],args[1],))
					threads.append(t)
					t.start()
					print("Thread {} launched!".format(threading.current_thread()))
				else:
					error = "Unable to launch thread! origin invalid: {}".format(origin)
					print(error)
					errorLog.log(error)
		print("!!! THREADING BALANCER HAS NOTHING TO DO!")
		time.sleep(2)

def queueThread(origin, args):
	qItem = [origin, args]
	q.put(qItem)

def startThreading():
	print("Starting master thread")
	t = threading.Thread(target=addThread,)
	threads.append(t)
	t.start()