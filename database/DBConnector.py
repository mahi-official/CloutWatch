import pymysql

def connect(brand)
	DB_URL = "localhost"
	DB_USER = "cloutwatch"
	DB_PASS = "psswd"
	database_name = brand

	connection = pymysql.connect(host=DB_URL,
							 user=DB_USER,
							 password=DB_PASS,
							 database=database_name,
							 charset='utf8mb4',
							 cursorclass=pymysql.cursors.DictCursor)

	return connection