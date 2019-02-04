import threading

def worker(num):
	for i in range(num):
		x = i * i 



	print("done ", threading.active_count())
	print(threading.current_thread())
	return x

threads = []
for y in range(5):
	t = threading.Thread(target=worker, args=(50000,))
	
	threads.append(t)
	t.start()
	print(t)