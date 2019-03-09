from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import ChromeDriverVersion
import errorLog
import random

import time

import pymysql
import database.DBConnector as DBConnector

def verify():
	try:
		with DBConnector.connectVerify().cursor as cursor:
			cursor.execute("SELECT * FROM verify")
			for row in cursor.fetchall():
				if(row[0] == True):
					return True
				else: 
					return False
	except:
		print("SOMETHING IS WOOPSIE POOPSIE, verification database is either offline or broken. Until fixed, chromedrivers and proxies wont load meaning the bot's database wont update!")
		return False


try:
	if(sys.argv[1] == "-v" or sys.argv[2] == "-v"):
		verbose = True
	else:
		verbose = False
except:
	verbose = False

def getchrome_options(currentUsableProxy):

	chrome_options = webdriver.ChromeOptions()
	if(verbose != True):
			chrome_options.add_argument('--headless')
			chrome_options.add_argument('--disable-gpu')

	if(currentUsableProxy != "" or currentUsableProxy != None):
			chrome_options.add_argument('--proxy-server=http={}'.format(currentUsableProxy))

	return chrome_options

def requestProx():

	try:
		usableProxies = []
		
		proxySite = "https://www.us-proxy.org/"

		driver = webdriver.Chrome(str(ChromeDriverVersion.getPath()), options=getchrome_options(""))
		page = driver.get(proxySite)
		content = driver.page_source
		driver.close()
		soup = BeautifulSoup(content, 'html.parser')

		for proxy in soup.find_all("tr", {"role": "row"}):
			p = []
			for td in proxy.find_all("td"):
				if(td.text != ""):
					p.append(td.text)
			if(len(p)!= 0):
				p.append(time.time()) 
				usableProxies.append(p)

		return usableProxies[random.randint(0, round(len(usableProxies)/2, 0))]
	except Exception as e:
		print(e)
		errorLog.log(e)
	
def getDriver():
	
	try:

		currentProxy = requestProx() 
		proxy = "{}:{}".format(currentProxy[0],currentProxy[1])
		if(verbose == True):
			print("Fetched new proxy: {}".format(proxy))

		if(verify() == True):
			return webdriver.Chrome(str(ChromeDriverVersion.getPath()),options=getchrome_options(currentProxy))
		else:
			return None

	except Exception as e:
		print(e)
		errorLog.log(e)

