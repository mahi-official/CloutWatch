from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import ChromeDriverVersion

def requestProx():

	try:
		proxySite = "https://www.us-proxy.org/"

		driver = webdriver.Chrome(str(ChromeDriverVersion.getPath()))
		page = driver.get(proxySite)
		content = driver.page_source
		driver.close()
		soup = BeautifulSoup(content, 'html.parser')

		usableProxies = []
		for proxy in soup.find_all("tr", {"role": "row"}):

			c = 0
			p = []
			for td in proxy.find_all("td"):
				if(c == 0):#get proxy ip
					p.append(td.text)
				if(c == 1):#get proxy port
					p.append(td.text)

				usableProxies.append(p)

		return usableProxies[0]
	except Exception as e:
		print(e)
		errorLog.log(e)
	
def getDriver():
	
	try:
		passProxy = requestProx()
		print("Fetched new proxy: {}".format(passProxy))
		
		currentProxy = requestProx()# ['proxyip', 'proxyport']
		proxy = "{}:{}".format(currentProxy[0],currentProxy[1])
		chrome_options = webdriver.ChromeOptions()
		chrome_options.add_argument('--proxy-server=http={}'.format(currentProxy))
		

		return webdriver.Chrome(str(ChromeDriverVersion.getPath()),options=chrome_options)
	except Exception as e:
		print(e)
		errorLog.log(e)
	

