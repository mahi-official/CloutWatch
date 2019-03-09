from bs4 import BeautifulSoup
import scrapers.sanitizeString


def frontPageScrape(soup):

	scrapeResult, scrapeResultFailed = [],[]
	for item in soup.find_all("div", {"class": "grid-item-box"}):
		currentItem = {}
		for productname in item.find_all("p", {"class": "product-display-name nsg-font-family--base edf-font-size--regular nsg-text--dark-grey"}):
			currentItem['name'] = scrapers.sanitizeString.cleanString(productname.get_text().strip())
		for price in item.find_all("span", {"class": "local nsg-font-family--base"}):
			currentItem['price'] = price.get_text().strip() 
		for div in item.find_all("div", {"class": "grid-item-image-wrapper sprite-sheet sprite-index-0"}):			
			currentItem['link'] = div.find('a')['href']

		if(" iD" in currentItem['name']):
			scrapeResultFailed.append(currentItem)
		else:
			scrapeResult.append(currentItem)

	return scrapeResult, scrapeResultFailed



def itemScrape(currentItemSoup ,currentItem):

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

	return currentItem, availableSizes, unavailableSizes