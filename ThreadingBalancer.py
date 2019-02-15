import threading
import SNike
import queue

threads = []
q = queue.Queue()

def startThread(origin, args):
	while not q.empty():
		if(threading.active_count() <=6):
			if(origin == "SNike"):
				t = threading.Thread(target=SNikegetShoeInfo, args=(args[0],args[1],))
			threads.append(t)
			t.start()
			print("Thread {} launched!".format(threading.current_thread()))


def queueThread(origin, args):
	q.put(origin, args)