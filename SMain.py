from selenium import webdriver
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
import seleniumProxy

from scrapers import SNike
numOfQueues = 5

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

		scrapeResult, scrapeResultFailed = SNike.frontPageScrape(soup)		
		print("{} found {} items and skipped {} ".format(brand.upper(), len(scrapeResult), len(scrapeResultFailed)))
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
		for x in range(len(scrapeResult)):
			queueObj[count-1].put(scrapeResult[x])
			if(count == len(queueObj)):
				count = 1
			else:
				count += 1

		random.shuffle(queueObj)
		q = queue.Queue()
		for obj in queueObj:
			q.put(obj)

		print("{} mainQueue has {} sub-queues, each containing: {} objects!".format(brand.upper(), q.qsize(), round(len(scrapeResult)/ q.qsize())))


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

def getCurrentItem(brand, queueObj, connector):
	try:	
		while not queueObj.empty():

			def getContent(queueObj, driver):
				
				for i in range(10):

					currentItem = queueObj.get()
					driver.get(currentItem['link'])
					currentItemSoup = BeautifulSoup(driver.page_source, 'html.parser') 
				
					if(brand == "nike"):
						currentItem, availableSizes, unavailableSizes = SNike.itemScrape(currentItemSoup, currentItem)

					if(len(availableSizes)== 0 and len(unavailableSizes) == 0):
						DBCheck.emptyItem(brand, currentItem, connector)
					else:	
						DBCheck.check(brand, currentItem, connector)

				driver.close()

			getContent(queueObj, seleniumProxy.getDriver())

	except Exception as e:
		print("GETCURRENTITEM ERROR: {}".format(e))
		errorLog.log("TGETCURRENTITEM ERROR: {}".format(e))