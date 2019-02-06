import pymysql

DB_URL = "localhost"
DB_USER = "cloutwatch"
DB_PASS = "psswd"
database_name = "nike"

connection = pymysql.connect(host=DB_URL,
							 user=DB_USER,
							 password=DB_PASS,
							 database=database_name,
							 charset='utf8mb4',
							 cursorclass=pymysql.cursors.DictCursor)


def check(brand, item):
	#check in db if item exists
	#if it does -> do nothign
	#if it doesnt -> replace the item
	
	