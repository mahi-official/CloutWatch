import pymysql

def connect(brand):
	DB_URL = "cloutwatchdb.c5med6d4kthk.us-east-1.rds.amazonaws.com"
	DB_USER = "cloutwatch"
	DB_PASS = "psswd"
	DB_NAME = brand.lower()

	connection = pymysql.connect(host=DB_URL,
							 user=DB_USER,
							 password=DB_PASS,
							 database=DB_NAME,
							 charset='utf8mb4',
							 cursorclass=pymysql.cursors.DictCursor)

	return connection