import time
import os



def log(e):
	path = os.path.join(os.getcwd(), 'Docs/errors.txt')
	print(os.getcwd())
	f = open(path, 'a')
	f.write(str(e) + "\n")
	f.close()