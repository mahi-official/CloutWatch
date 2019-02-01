from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request
import time
import random
import os

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

	def getShoeInfo(driver, url):
		print(url)
		pageContent = driver.get(url)
		return driver.page_source
	
	
	
	if True: 
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

	driver = webdriver.Chrome()
	print(len(soup.find_all("div", {"class": "grid-item-box"})))
	for item in soup.find_all("div", {"class": "grid-item-box"}):
		shoe = []
		for productname in item.find_all("p", {"class": "product-display-name nsg-font-family--base edf-font-size--regular nsg-text--dark-grey"}):
			shoe.append(productname.string)
			print("Name: ",productname.string)
		for price in item.find_all("span", {"class": "local nsg-font-family--base"}):
			shoe.append(price.string)
			print("Price: ",price.string)
		for div in item.find_all("div", {"class": "grid-item-image-wrapper sprite-sheet sprite-index-0"}):
			shoe.append(div.find('a')['href'])
			print("Link :",div.find('a')['href'])
			shoeInfo = BeautifulSoup(getShoeInfo(driver, div.find('a')['href']))
			availableSizes, unavailableSizes = [], []
			for size in shoeInfo.find_all("input", {"name": "skuAndSize"}):
				if('disabled' in str(size)):
					tempSizeArray = str(size).split('"')
					unavailableSizes.append(tempSizeArray[1])
				else:
					tempSizeArray = str(size).split('"')
					availableSizes.append(tempSizeArray[1])
			print("Y sizes: ",availableSizes)
			print("X sizes: ",unavailableSizes)
			shoe.append(availableSizes)
			shoe.append(unavailableSizes)

			print("\n")
		nikeresult.append(shoe)



	for shoe in nikeresult:
		print("name: {} price: {} \nlink: {} \navailableSizes: {} \nunavailableSizes: {}". format(shoe[0], shoe[1], shoe[2], shoe[3], shoe[4]))


	driver.close()
	print(len(nikeresult))
	print(nikeresult[random.randrange(0,len(nikeresult))])
	exit()

	return  soup

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

