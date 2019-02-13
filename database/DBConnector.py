import pymysql

def connect(brand):
	DB_URL = "localhost"
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