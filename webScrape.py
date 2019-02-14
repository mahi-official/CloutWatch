from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request
from urllib.request import Request, urlopen
import time
import random
import os
import sys

import threading
import queue

import SNike
import ChromeDriverVersion
import errorLog


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

def bapeScrape(website):        
	page = requestWebsite(website)

	return soup

def nikeScrape(website):

	try:
		if False or sys.argv[1].lower() == "save":
			content = requestWebsite(website)
		else:
			content = "none"
	except Exception as e:
		errorLog.log(e)
		content = "none"

	SNike.Scrape(content)


def adidasScrape(website):
	page = requestWebsite(website)


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

