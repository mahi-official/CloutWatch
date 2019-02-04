from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request
from urllib.request import Request, urlopen
import time
import random
import os
import mechanize

import threading
import queue

def requestWebsite(website):

	print("Scraping: {}".format(website))
	try:
		
		driver = webdriver.Chrome()
		page = driver.get(website)

		last_height = driver.execute_script("return document.body.scrollHeight")
		while True:
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(1)
			new_height = driver.execute_script("return document.body.scrollHeight")
			if(new_height == last_height):
				break
			last_height = new_height

		content = driver.page_source
		content.replace("\\n", "")
		driver.close()

		return content
	except Exception as e:
		print(e)

def bapeScrape(website):        
	soup = requestWebsite(website)

	return  soup

def nikeScrape(website):
	
	if True: 
		soup = BeautifulSoup(requestWebsite(website), 'html.parser')
	else:
		f = open("Docs/nike.html", "r")
		soup = BeautifulSoup(f, 'html.parser')  
		f.close()

	if False:
		#to download the whole page for testing, so you dont have to redownload it every time
		f = open("Docs/nike.html", "w")
		f.write(str(soup.prettify().encode("utf-8")))
		f.close()
		exit()


	nikeresult, threads = [], []
	q,q1,q2 = queue.Queue(),queue.Queue(),queue.Queue()



	def getShoeInfo(queueObj):

		qX = queueObj
		driver = webdriver.Chrome()
		while not qX.empty():

			obj = qX.get()
			div, shoe = obj[0], obj[1]
			time.sleep(2)
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
			print("Thread: " ,threading.current_thread(), " CurrentQueue: ", qX.qsize())
			print(shoe[0:2],shoe[-2:])
			nikeresult.append(shoe)
		driver.close()

	
	print(len(soup.find_all("div", {"class": "grid-item-box"})))
	for item in soup.find_all("div", {"class": "grid-item-box"}):
		shoe = []
		for productname in item.find_all("p", {"class": "product-display-name nsg-font-family--base edf-font-size--regular nsg-text--dark-grey"}):
			shoe.append(productname.get_text().strip())
		for price in item.find_all("span", {"class": "local nsg-font-family--base"}):
			shoe.append(price.get_text().strip())


	
		for div in item.find_all("div", {"class": "grid-item-image-wrapper sprite-sheet sprite-index-0"}):			
			shoe.append(div.find('a')['href'])

			#print(shoe)
			obj = [div, shoe]
			q.put(obj)
			print("Qsize: ", q.qsize())

	count = 1	
	queueObj = [q1, q2]
	while not q.empty():
		queueObj[count-1].put(q.get())
		if(count == 2):
			count = 1
		else:
			count += 1
		
	for qObj in queueObj:
		print(qObj.qsize())
	
	for i in range(len(queueObj)):
		q.put(queueObj[i])

	while not q.empty():
		if(threading.active_count() <=2):
			print("Qsize: ", q.qsize())
			t = threading.Thread(target=getShoeInfo, args=(q.get(),))
			threads.append(t)
			t.start()
			time.sleep(4)

	while not q1.empty():
		time.sleep(1)

	print(len(nikeresult))
	for shoe in nikeresult:
		print("name: {} price: {} \nlink: {} \navailableSizes: {} \nunavailableSizes: {}". format(shoe[0], shoe[1], shoe[2], shoe[3], shoe[4]))
	
	
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

