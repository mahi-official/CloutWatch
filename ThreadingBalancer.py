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
			try:
				if(threading.active_count() <= 6):
					qItem = q.get()
					origin, args = qItem[0], qItem[1] #qItem[0] = brand.   qItem[1] = [q.get(), DBConnector.connect("nike")]
					if(origin == "nike"):
						t = threading.Thread(target=SNike.getCurrentItem, args=(args[0],args[1],))
						threads.append(t)
						t.start()
						print("Thread {} launched!".format(threading.current_thread()))
					else:
						error = "Unable to launch thread! origin invalid: {}".format(origin)
						print(error)
						errorLog.log(error)
			except Exception as e:
				print(e)
				errorLog.log(e)
		time.sleep(1)

def queueThread(origin, args):
	qItem = [origin, args]
	q.put(qItem)

def startThreading(): 
	print("Starting master thread 1/1!")
	t = threading.Thread(target=addThread,)
	threads.append(t)
	t.start()