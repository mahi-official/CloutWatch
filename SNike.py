from selenium import webdriver
from bs4 import BeautifulSoup
import time
import random
import os

import threading
import queue

import database.DBCheck as DBCheck
import database.DBConnector as DBConnector

def Scrape(content):

	#Choose in parent file weither you wanna download the file or use a pre existing version
	if(content != "None"): 
		soup = BeautifulSoup(content, 'html.parser')
	else:
		f = open("Docs/nike.html", "r")
		soup = BeautifulSoup(f, 'html.parser')  
		f.close()

	if False:
		#to download the whole page for testing, so you dont have to redownload it every time
		f = open("Docs/nike.html", "w")
		f.write(str(content.encode("utf-8")))
		f.close()
		exit()

	nikeresult, threads = [], [] #define nikeresult list and threadlist
	q,q1,q2 = queue.Queue(),queue.Queue(),queue.Queue() #define all queue's q1 and q2 are for the threads
	count = 1 #counter for queue division
	queueObj = [q1, q2] #queue object containing all secondary queues

	print("Total amount of shoes found on page: ", len(soup.find_all("div", {"class": "grid-item-box"})))


	for item in soup.find_all("div", {"class": "grid-item-box"}): #for every shoe on the front page:
		shoe = {'name': "shoeName",
				'price': "$000",
				'link': "https://nike.com/shoe",
				'available': [1,2,3],
				'unavailable': [-1,-2,-3]}

		#shoe structure = {"name of shoe", "price of shoe in $", "https://linkToShoe.com", ["available sizes", "14","15"],["unavailable sizes", "12", "13"]}
		for productname in item.find_all("p", {"class": "product-display-name nsg-font-family--base edf-font-size--regular nsg-text--dark-grey"}):
			shoe['name'] = productname.get_text().strip() #get the name of she shoe ie: Air Jordan 12, Kyrie 5 
		for price in item.find_all("span", {"class": "local nsg-font-family--base"}):
			shoe['price'] = price.get_text().strip() #get the price for the individual shoe ie: $150, $100


		for div in item.find_all("div", {"class": "grid-item-image-wrapper sprite-sheet sprite-index-0"}):			
			shoe['link'] = div.find('a')['href'] #get the link for every individual shoe

			#print(shoe)
			obj = [div, shoe] #add the shoe[name, price, link] and the div element (containing the html5 for the item)
			q.put(obj) #put that object into the master queue
			if(q.qsize() % 100 == 0): #if queuesize is divisible by 10 show qsize (to clear clutter)
				print("Qsize: ", q.qsize())

	print("Final Qsize: ", q.qsize())
	

	def getShoeInfo(queueObj, connector):

		qX = queueObj
		driver = webdriver.Chrome()

		while not qX.empty():

			obj = qX.get() 
			div, shoe = obj[0], obj[1]
			time.sleep(3) 
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
			shoe['available'] = availableSizes
			shoe['unavailable'] = unavailableSizes
			print("Thread: " ,threading.current_thread(), " CurrentQueue: ", qX.qsize())
			#print(shoe[0:2],shoe[-2:])
			DBCheck.check("Nike", shoe, connector)
		driver.close()

	while not q.empty(): #splitting up the queues in multiple secondary queues that are given to each individual thread
		queueObj[count-1].put(q.get())
		if(count == 2):
			count = 1
		else:
			count += 1
		
	for qObj in queueObj:
		print(qObj, "Contains: ", qObj.qsize(), " Items")
	
	for i in range(len(queueObj)): #repurpose queue
		q.put(queueObj[i]) #put secondary queue's in main queue

	while not q.empty():
		if(threading.active_count() <=2): #change this if more threads required
			t = threading.Thread(target=getShoeInfo, args=(q.get(),DBConnector.connect("nike"),))
			threads.append(t)
			t.start()
			print("Thread {} launched!".format(threading.current_thread()))
			time.sleep(2)

	while not q1.empty() and not q2.empty(): #sleep till secondary queue's are done
		time.sleep(1)

	exit()
