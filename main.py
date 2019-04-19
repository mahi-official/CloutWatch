import os
import ThreadingBalancer
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import random
import os
import sys

import SMain
import ChromeDriverVersion
import errorLog

def getWebsites():
	websites = []
	file = os.path.join(os.getcwd(), "Docs", "websites.txt")
	with open(file, 'r') as file:
		for line in file:
			if(line[-1:] == "/n"):
				websites.append(line[:-1])
			else:
				websites.append(line[:-1])

	return websites

def requestWebsite(website):

	print("Scraping: {}".format(website))
	try:
		
		driver = webdriver.Chrome(ChromeDriverVersion.getPath())
		page = driver.get(website)

		last_height = driver.execute_script("return document.body.scrollHeight")
		while True:
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			print("!!Scrolling!!")
			time.sleep(1.5)
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
		errorLog.log(e)

def LoadOrSave(website):
	try:
		if False or sys.argv[1].lower() == "save":
			content = requestWebsite(website)
		else:
			content = "none"
	except Exception as e:
		errorLog.log(e)
		content = "none"

	return content

def websiteFilter(website):

	if(website == "https://store.nike.com/us/en_us/pw/mens-shoes/7puZoi3"):
		SMain.Scrape(LoadOrSave(website), "nike")


def main():
	ThreadingBalancer.startThreading()
	for website in getWebsites():
		websiteFilter(website)

if __name__ == '__main__':
	main()
