import threading
import SNike

threads = []
def startThread(origin, args):
	if(threading.active_count() <=6):
		if(origin == "SNike"):
			t = threading.Thread(target=SNikegetShoeInfo, args=(args[0],args[1],))
		threads.append(t)
		t.start()
		print("Thread {} launched!".format(threading.current_thread()))