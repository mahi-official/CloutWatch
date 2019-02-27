from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import ChromeDriverVersion
import errorLog
import random

import time


try:
	if(sys.argv[1] == "-v" or sys.argv[2] == "-v"):
		verbose = True
	else:
		verbose = False
except:
	verbose = False

def requestProx():

	try:
		usableProxies = []
		
		proxySite = "https://www.us-proxy.org/"

		
		if(verbose == False):
			chrome_options = webdriver.ChromeOptions()
			chrome_options.add_argument('--headless')
			chrome_options.add_argument('--disable-gpu')

		driver = webdriver.Chrome(str(ChromeDriverVersion.getPath()), options=chrome_options)
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

		chrome_options = webdriver.ChromeOptions()
		chrome_options.add_argument('--proxy-server=http={}'.format(currentProxy))
		if(verbose == False):
			chrome_options.add_argument('--headless')
			chrome_options.add_argument('--disable-gpu')

		return webdriver.Chrome(str(ChromeDriverVersion.getPath()),options=chrome_options)


	except Exception as e:
		print(e)
		errorLog.log(e)

