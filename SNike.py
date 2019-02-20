from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from bs4 import BeautifulSoup
import time
import random
import os
import sys

import threading
import queue
import asyncio

import ThreadingBalancer

import database.DBCheck as DBCheck
import database.DBConnector as DBConnector

import errorLog
import sanetizeInput
import seleniumProxy

numOfQueues = 2

def Scrape(content, brand):

	def openHTMLfile(readOrWrite):
		if(readOrWrite == "r"):
			try:		
				return open("Docs/{}.html".format(brand), "r")
			except IOError:
				openHTMLfile("w")
		else:
			return open("Docs/{}.html".format(brand), "w")

	def openSoup(content):
		return BeautifulSoup(content, 'html.parser')

	try:
		if(content.lower() != "none"): 
			soup = openSoup(content)
		else:
			soup = openSoup(openHTMLfile("r"))

		try:	
			if(sys.argv[1].lower() == "save"):
				openHTMLfile("w").write(str(content.encode("utf-8")))
				print("HTML page saved!")
				exit()
		except:
			pass

	except Exception as e:
		print("SAVING AND LOADING ERROR: {}".format(e))
		errorLog.log("SAVING AND LOADING ERROR: {}".format(e))

	def scrapeSoup(soup):
		scrapeResult, scrapeResultFailed = [],[]
		for item in soup.find_all("div", {"class": "grid-item-box"}):
			currentItem = {}
			for productname in item.find_all("p", {"class": "product-display-name nsg-font-family--base edf-font-size--regular nsg-text--dark-grey"}):
				currentItem['name'] = sanetizeInput.clean(productname.get_text().strip())
			for price in item.find_all("span", {"class": "local nsg-font-family--base"}):
				currentItem['price'] = price.get_text().strip() 
			for div in item.find_all("div", {"class": "grid-item-image-wrapper sprite-sheet sprite-index-0"}):			
				currentItem['link'] = div.find('a')['href']

			if(" iD" in currentItem['name']):
				scrapeResultFailed.append(currentItem)
			else:
				scrapeResult.append(currentItem)

		print("{} found {} items and skipped {} ".format(brand.upper(), len(scrapeResult), len(scrapeResultFailed)))
		print(scrapeResultFailed)
		return scrapeResult

	try:
		scrapeResult = scrapeSoup(soup)
	except Exception as e:
		print(e)
		errorLog.log(e)


	def makeQueueObjects(numOfQueues):
		queueObj = []
		for x in range(numOfQueues):
			queueObj.append(queue.Queue())
		return queueObj

	def divideQueues(scrapeResult, queueObj):
		random.shuffle(scrapeResult)

		count = 1
		scrapeLen = len(scrapeResult)
		for x in range(scrapeLen):
			queueObj[count-1].put(scrapeResult.pop())
			if(count == len(queueObj)):
				count = 1
			else:
				count += 1

		random.shuffle(queueObj)
		q = queue.Queue()
		for obj in queueObj:
			q.put(obj)

		print("{} mainQueue has {} sub-queues, each containing: {} objects!".format(brand.upper(), q.qsize(), round(scrapeLen/ q.qsize())))


		return q

	try:
		queueObj = makeQueueObjects(numOfQueues)
		q = divideQueues(scrapeResult, queueObj)
	except Exception as e:
		print("MAKING QUEUES AND DIVIDIG THEM ERROR: {}".format(e))
		errorLog.log("MAKING QUEUES AND DIVIDIG THEM ERROR: {}".format(e))

	while(q.qsize() != 0):
		try:
			ThreadingBalancer.queueThread(brand, [q.get(), DBConnector.connect("nike")])
		except Exception as e:
			print("THREAD PLACEMENT ERROR: {}".format(e))
			errorLog.log("THREAD PLACEMENT ERROR: {}".format(e))
	exit()

def getCurrentItem(queueObj, connector):
	try:	
		while not queueObj.empty():

			def getContent(currentItem, driver):
				for i in range(10):

					driver.get(currentItem['link'])
					currentItemSoup = BeautifulSoup(driver.page_source, 'html.parser') 
					
					availableSizes, unavailableSizes = [], []
					for size in currentItemSoup.find_all("input", {"name": "skuAndSize"}):
						if('disabled' in str(size)):
							tempSizeArray = str(size).split('"')
							unavailableSizes.append(tempSizeArray[3])
						else:
							tempSizeArray = str(size).split('"')
							availableSizes.append(tempSizeArray[3])

					currentItem['available'] = str(availableSizes)
					currentItem['unavailable'] = str(unavailableSizes)

					if(len(availableSizes)==0 and len(unavailableSizes) == 0):
						DBCheck.emptyItem("Nike", currentItem, connector)
					else:	
						DBCheck.check("Nike", currentItem, connector)
				driver.close()
			
			print(queueObj.get())
			getContent(queueObj.get(), seleniumProxy.getDriver())

	except Exception as e:
		print("GETCURRENTITEM ERROR: {}".format(e))
		errorLog.log("TGETCURRENTITEM ERROR: {}".format(e))