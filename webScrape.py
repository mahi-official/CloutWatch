from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request
from urllib.request import Request, urlopen
import time
import random
import os

import threading
import queue

import SNike

def requestWebsite(website):

	print("Scraping: {}".format(website))
	try:
		
		driver = webdriver.Chrome('Docs/chromedriver')
		page = driver.get(website)

		last_height = driver.execute_script("return document.body.scrollHeight")
		while True:
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
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

	if False:
		content = requestWebsite(website)
	else:
		content = "None"

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

