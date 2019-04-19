import pymysql
import base64

def connect(brand):
	DB_URL = "##REDACTED##"
	DB_USER = "cloutwatch"
	DB_PASS =  base64.b64decode("##REDACTED##").decode()
	DB_NAME = brand.lower()

	connection = pymysql.connect(host=DB_URL,
							 user=DB_USER,
							 password=DB_PASS,
							 database=DB_NAME,
							 charset='utf8mb4',
							 cursorclass=pymysql.cursors.DictCursor)

	return connection

def connectVerify():
	DB_URL = "##REDACTED##"
	DB_USER = "cloutwatch"
	DB_PASS =  base64.b64decode("##REDACTED##".decode())
	DB_NAME = brand.lower()

	connection = pymysql.connect(host=DB_URL,
							 user=DB_USER,
							 password=DB_PASS,
							 database=DB_NAME,
							 charset='utf8mb4',
							 cursorclass=pymysql.cursors.DictCursor)

	return connection