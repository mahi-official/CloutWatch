import threading
import SMain
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
					brand, args = qItem[0], qItem[1] #qItem[0] = brand.   qItem[1] = [q.get(), DBConnector.connect("nike")]
					if(brand == "nike"):
						t = threading.Thread(target=SMain.getCurrentItem, args=(brand, args[0],args[1],))
						threads.append(t)
						t.start()
						print("Thread {} launched!".format(threading.current_thread()))
					else:
						print("Unable to launch thread! brand invalid: {}".format(brand))
						errorLog.log("Unable to launch thread! brand invalid: {}".format(brand))
			except Exception as e:
				print(e)
				errorLog.log(e)
		time.sleep(1)

def queueThread(brand, args):
	q.put([brand, args])

def startThreading(): 
	print("Starting master thread 1/1!")
	t = threading.Thread(target=addThread,)
	threads.append(t)
	t.start()