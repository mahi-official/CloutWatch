from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request
import time
import random
import os

import threading
import queue

def requestWebsite(website):

	print("Scraping: {}".format(website))
	try:
		
		driver = webdriver.Chrome()
		driver.maximize_window()
		page = driver.get(website)

		last_height = driver.execute_script("return document.body.scrollHeight")
		while True:
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(2)
			new_height = driver.execute_script("return document.body.scrollHeight")
			if(new_height == last_height):
				break
			last_height = new_height

		content = driver.page_source
		#driver.close()

		return content
	except Exception as e:
		print(e)

def bapeScrape(website):        
	soup = requestWebsite(website)

	return  soup

def nikeScrape(website):
	
	if False: 
		soup = BeautifulSoup(requestWebsite(website), 'html.parser')
	else:
		f = open("Docs/nike.html", "r")
		soup = BeautifulSoup(f, 'html.parser')  
		f.close()

	if False:
		#to download the whole page for testing, so you dont have to redownload it every time
		f = open("Docs/nike.html".decode(), "w")
		f.write(str(soup.prettify().encode("utf-8")))
		f.close()
		exit()


	nikeresult = []
	q = queue.Queue()

	def getShoeInfo(div, shoe):

		driver = webdriver.Chrome()
		pageContent = driver.get(div.find('a')['href'])
		shoeInfo = BeautifulSoup(driver.page_source, 'html.parser')
		availableSizes, unavailableSizes = [], []
		for size in shoeInfo.find_all("input", {"name": "skuAndSize"}):
			if('disabled' in str(size)):
				tempSizeArray = str(size).split('"')
				unavailableSizes.append(tempSizeArray[1])
			else:
				tempSizeArray = str(size).split('"')
				availableSizes.append(tempSizeArray[1])
		shoe.append(unavailableSizes)
		shoe.append(availableSizes)
		nikeresult.append(shoe)
		driver.close()

	
	print(len(soup.find_all("div", {"class": "grid-item-box"})))
	for item in soup.find_all("div", {"class": "grid-item-box"}):
		shoe = []
		for productname in item.find_all("p", {"class": "product-display-name nsg-font-family--base edf-font-size--regular nsg-text--dark-grey"}):
			shoe.append(productname.get_text())
		for price in item.find_all("span", {"class": "local nsg-font-family--base"}):
			shoe.append(price.get_text())


	
		for div in item.find_all("div", {"class": "grid-item-image-wrapper sprite-sheet sprite-index-0"}):			
			shoe.append(div.find('a')['href'])

			#print(shoe)
			obj = [div, shoe]
			q.put(obj)
			print("Qsize: ", q.qsize())

	threads = []
	while not q.empty():
		if(threading.active_count() <=3):
			print("Qsize: ", q.qsize())
			obj = q.get()
			div, shoe = obj[0], obj[1]
			t = threading.Thread(target=getShoeInfo, args=(div, shoe,))
			threads.append(t)
			t.start()
			try:
				print(len(nikeresult))
				print(nikeresult[random.randrange(0,len(nikeresult))])
			except:
				pass
		


	for shoe in nikeresult:
		print("name: {} price: {} \nlink: {} \navailableSizes: {} \nunavailableSizes: {}". format(shoe[0], shoe[1], shoe[2], shoe[3], shoe[4]))


	
	print(len(nikeresult))
	print(nikeresult[random.randrange(0,len(nikeresult))])
	exit()

	return  nikeresult

def adidasScrape(website):
	soup = requestWebsite(website)


	return  soup

def yeezyScrape(website):
	soup = requestWebsite(website)

	return  soup

def kithScrape(website):
	soup = requestWebsite(website)

	return  soup

def undefeatedScrape(website):
	soup = requestWebsite(website)

	return  soup

def palaceskateboardsScrape(website):
	soup = requestWebsite(website)

	return  soup

def doverstreetmarketScrape(website):
	soup = requestWebsite(website)

	return  soup

def vloneScrape(website):
	soup = requestWebsite(website)

	return  soup

