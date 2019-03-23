from bs4 import BeautifulSoup
import scrapers.sanitizeString


def frontPageScrape(soup):

	scrapeResult, scrapeResultFailed = [],[]
	for ul in soup.find_all("ul", {"id": "shop-scroller"}):
		for a in ul.find_all("a", href=True):
			currentItem = {}						
			currentItem['link'] = "https://www.supremenewyork.com" + a['href']
			print(currentItem['link'])

			if(currentItem['link'] != "" or currentItem['link'] != None):
				scrapeResult.append(currentItem)	
			else:
				scrapeResultFailed.append(currentItem)

	return scrapeResult, scrapeResultFailed



def itemScrape(currentItemSoup ,currentItem):

	availableSizes, unavailableSizes, pics = [], [], []
	try:
		for picture in currentItemSoup.find_all("img", {"class": "css-viwop1 u-full-width u-full-height css-147n82m"}):
			
			url = str(picture.get("src"))
			if("LOADING" in url.upper()):
				pass
			else:
				if(url != ""):
					pics.append(url)

		currentItem['pictures'] = pics
	except Exception as e:
		print("pic not found! " + e )
		currentItem['pictures'] = [""]

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