from selenium import webdriver

def requestWebsite(website):

	print("Scraping: {}".format(website))
	try:
		driver = webdriver.Chrome()
		page = driver.get(website)
		content = driver.page_source
		driver.close()

		print(content)
		return content
	except Exception as e:
		print(e)

def bapeScrape(website):		
	data = requestWebsite(website)

	return data

def nikeScrape(website):
	data = requestWebsite(website)

	return data

def adidasScrape(website):
	data = requestWebsite(website)

	return data

def yeezyScrape(website):
	data = requestWebsite(website)

	return data

def kithScrape(website):
	data = requestWebsite(website)

	return data

def undefeatedScrape(website):
	data = requestWebsite(website)

	return data

def palaceskateboardsScrape(website):
	data = requestWebsite(website)

	return data

def doverstreetmarketScrape(website):
	data = requestWebsite(website)

	return data

def vloneScrape(website):
	data = requestWebsite(website)

	return data

