import sys
import os

sys.path.insert(0, str(os.path.join("/",*list(os.getcwd().split("/"))[:-1], "database/")))
import DBConnector

def get(brand):
	try:
		with DBConnector.connect(brand).cursor() as cursor:
			cursor.execute("SELECT * FROM notification ORDER BY id DESC LIMIT 1;")
			return cursor.fetchall()
	except Exception as e:
		return "Something went wrong! Try again later!" + str(e)

def get10(brand):
	try:
		with DBConnector.connect(brand).cursor() as cursor:
			cursor.execute("SELECT * FROM notification ORDER BY id DESC LIMIT 10;")
			return cursor.fetchall()
	except Exception as e:
		return "Something went wrong! Try again later!" + str(e)