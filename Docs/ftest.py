import threading

def worker(num):
	for i in range(num):
		x = i * i 

	print("done ", threading.active_count())
	print(threading.current_thread())
	return x

threads = []
max_num_of_threads = 5
for y in range(max_num_of_threads):
	t = threading.Thread(target=worker, args=(50000,))
	
	threads.append(t)
	t.start()
	print(t)

threads = []

t = threading.Thread(target=function1)
threads.append(t)
t = threading.Thread(target=function2)
threads.append(t)
t = threading.Thread(target=function3)
threads.append(t)