#This script is dedicated to creating tables in a fresh database enviroment
#this has to be run manually!
#also make sure user 'cloutwatch' has all grants

import pymysql

DB_URL = "cloutwatchdb.c5med6d4kthk.us-east-1.rds.amazonaws.com"
DB_USER = "cloutwatch"
DB_PASS = "psswd"
database_name = "nike"

def createNikeTable():


	connection = pymysql.connect(host=DB_URL,
							 user=DB_USER,
							 password=DB_PASS,
							 database=database_name,
							 charset='utf8mb4',
							 cursorclass=pymysql.cursors.DictCursor)

	with connection.cursor() as cursor:
		try:
			cursor.execute("CREATE TABLE IF NOT EXISTS data (ID int NOT NULL AUTO_INCREMENT,ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP , name TEXT, price TEXT, link TEXT, available TEXT, unavailable TEXT, pictures TEXT, PRIMARY KEY (ID))")
			connection.commit()
		except Exception as e:
			print(e)


def createEmptyItem():


	connection = pymysql.connect(host=DB_URL,
							 user=DB_USER,
							 password=DB_PASS,
							 database=database_name,
							 charset='utf8mb4',
							 cursorclass=pymysql.cursors.DictCursor)

	with connection.cursor() as cursor:
		try:
			cursor.execute("CREATE TABLE IF NOT EXISTS emptyItem (ID int NOT NULL AUTO_INCREMENT,ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP , name TEXT, price TEXT, link TEXT, available TEXT, unavailable TEXT, pictures TEXT, PRIMARY KEY (ID))")
			connection.commit()
		except Exception as e:
			print(e)

def createNotification():


	connection = pymysql.connect(host=DB_URL,
							 user=DB_USER,
							 password=DB_PASS,
							 database=database_name,
							 charset='utf8mb4',
							 cursorclass=pymysql.cursors.DictCursor)

	with connection.cursor() as cursor:
		try:
			cursor.execute("CREATE TABLE IF NOT EXISTS notification (ID int NOT NULL AUTO_INCREMENT, type TEXT, ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, name TEXT, price TEXT, link TEXT, available TEXT, unavailable TEXT, pictures TEXT, PRIMARY KEY (ID))")
			connection.commit()
		except Exception as e:
			print(e)

createNotification()
createEmptyItem()
createNikeTable()
