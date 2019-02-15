from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from bs4 import BeautifulSoup
import time
import random
import os
import sys

import threading
import queue

import ThreadingBalancer

import database.DBCheck as DBCheck
import database.DBConnector as DBConnector

import errorLog
import sanetizeInput
import seleniumProxy

global sleeptime

def getShoeInfo(queueObj, connector):
	try:
		qX = queueObj #get thread specific queue object
		
		while not qX.empty():

			driver = seleniumProxy.getDriver() #get seleniumdriver with proxy

			for i in range(20): #do this X amount of time, then get another proxy driver
				obj = qX.get() #get object out of thread specific queue
				div, shoe = obj[0], obj[1] #get div and shoe out of the object
				print("Thread: " ,threading.current_thread(), " CurrentQueue: ", qX.qsize())
				time.sleep(1)

				pageContent = driver.get(div.find('a')['href'])#get specific shoe page from div and opens it
				shoeInfo = BeautifulSoup(driver.page_source, 'html.parser') #BS4 Parser
				availableSizes, unavailableSizes = [], []

				for size in shoeInfo.find_all("input", {"name": "skuAndSize"}):#get sizes
					if('disabled' in str(size)):#get all disabled (or unavailable sizes)
						tempSizeArray = str(size).split('"')
						unavailableSizes.append(tempSizeArray[1])
					else:#get all available sizes
						tempSizeArray = str(size).split('"')
						availableSizes.append(tempSizeArray[1])

				#append them to the shoe object
				shoe['available'] = str(availableSizes)
				shoe['unavailable'] = str(unavailableSizes)

				#if both size arrays are empty, theres something wrong so we add them to the emptyItem database to check out later! 
				#This catches broken links, new drops that you cant buy yet and iD shoes that dont have " iD " in their name!
				if(len(availableSizes)==0 and len(unavailableSizes) == 0):
					if(" iD" in shoe['name']):
						pass
					else:
						DBCheck.emptyItem("Nike", shoe, connector)
				else:	
					DBCheck.check("Nike", shoe, connector)

					
				#time.sleep(.5) 
			driver.close()
	except Exception as e:
		print(e)
		errorLog.log(e)

def Scrape(content):

	try:
		#Choose in parent file weither you wanna download the file or use a pre existing version
		if(content.lower() != "none"): 
			soup = BeautifulSoup(content, 'html.parser')
		else:
			f = open("Docs/nike.html", "r")
			soup = BeautifulSoup(f, 'html.parser')  
			f.close()

		if(sys.argv[1].lower() == "save"):
			#to download the whole page for testing, so you dont have to redownload it every time
			f = open("Docs/nike.html", "w")
			f.write(str(content.encode("utf-8")))
			f.close()
			exit()
		else:
			pass

	except Exception as e:
		print(e)
		errorLog.log(e)

	nikeresult = [] #define nikeresult list and threadlist
	q,q1,q2 = queue.Queue(),queue.Queue(),queue.Queue() #define all queue's q1 and q2 are for the threads
	count = 1 #counter for queue division
	queueObj = [q1, q2] #queue object containing all secondary queues

	print("Total amount of shoes found on page: ", len(soup.find_all("div", {"class": "grid-item-box"})))

	iDCount = 0 #count of shoes that use Nike iD
	normalCount = 0	#count of shoes that dont use Nike iD

	try:
		for item in soup.find_all("div", {"class": "grid-item-box"}): #for every shoe on the front page:
			shoe = {'name': "shoeName",
					'price': "$000",
					'link': "https://nike.com/shoe",
					'available': [1,2,3],
					'unavailable': [-1,-2,-3]}

			#shoe structure = {"name of shoe", "price of shoe in $", "https://linkToShoe.com", ["available sizes", "14","15"],["unavailable sizes", "12", "13"]}
			for productname in item.find_all("p", {"class": "product-display-name nsg-font-family--base edf-font-size--regular nsg-text--dark-grey"}):
				shoe['name'] = sanetizeInput.clean(productname.get_text().strip()) #get the name of she shoe ie: Air Jordan 12, Kyrie 5 
			for price in item.find_all("span", {"class": "local nsg-font-family--base"}):
				shoe['price'] = price.get_text().strip() #get the price for the individual shoe ie: $150, $100


			for div in item.find_all("div", {"class": "grid-item-image-wrapper sprite-sheet sprite-index-0"}):			
				shoe['link'] = div.find('a')['href'] #get the link for every individual shoe

			
			if(" iD" in shoe['name']):#add up all the shoes that use Nike iD
				iDCount += 1
				#print("Skipped Nike iD: {}".format(shoe['name']))
			else:
				obj = [div, shoe] #add the shoe[name, price, link] and the div element (containing the html5 for the item)
				nikeresult.append(obj) #put that object into the master queue
				if(len(nikeresult) % 100 == 0): #if queuesize is divisible by 10 show qsize (to clear clutter)
					print("Qsize: ", len(nikeresult))
				normalCount += 1

		print("Added {} items to queue, skipped {} iD shoes".format(normalCount, iDCount))
	except Exception as e:
		print(e)
		errorLog.log(e)

	print("Final Qsize: ", len(nikeresult))
	

	try:

		random.shuffle(nikeresult)
		while len(nikeresult) != 0: #splitting up the queues in multiple secondary queues that are given to each individual thread
			#queueObj[count-1].put(nikeresult.pop(0))
			#if(count == 2):
			#	count = 1
			#else:
			#	count += 1
			queueObj[0].put(nikeresult.pop(0))
			
		for qObj in queueObj:
			print(qObj, "Contains: ", qObj.qsize(), " Items")

		for i in range(len(queueObj)): #repurpose queue
			q.put(queueObj[i]) #put secondary queue's in main queue

	except Exception as e:
		print(e)
		errorLog.log(e)

	while not q.empty():
		try:
			threadArgs = [q.get(), DBConnector.connect("nike")]
			ThreadingBalancer.startThread("SNike", threadArgs)
		except Exception as e:
			print(e)
			errorLog.log(e)

	while not q1.empty() and not q2.empty(): #sleep till secondary queue's are done
		time.sleep(1)

	exit()
