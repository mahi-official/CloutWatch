import time
import os

def log(e):
	try:
		path = os.path.join(os.getcwd(), 'Docs/errors.txt')
		f = open(path, 'a')
		f.write(str(e) + " |  " + str(time.ctime(time.time())) + "\n")
		f.close()
	except Exception as e:
		print(e)
		for i in range(5):
			print("LOGGING ERROR!!! CAN'T LOG!")
			time.sleep(1)