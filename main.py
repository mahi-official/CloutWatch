import os
from webScrape import *

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

def websiteFilter(website):

	if(website == "https://us.bape.com/"):
		bapeScrape(website)
	elif(website == "https://store.nike.com/us/en_us/pw/mens-shoes/7puZoi3"):
		nikeScrape(website)
	elif(website == "https://www.adidas.com/us"):
		adidasScrape(website)
	elif(website == "https://yeezysupply.com/"):
		yeezyScrape(website)
	elif(website == "https://kith.com/"):
		kithScrape(website)
	elif(website == "https://undefeated.com/"):
		undefeatedScrape(website)
	elif(website == "https://www.palaceskateboards.com/"):
		palaceskateboardsScrape(website)
	elif(website == "https://shop.doverstreetmarket.com/us/"):
		doverstreetmarketScrape(website)
	elif(website == "https://vlone.co/"):
		vloneScrape(website)

def main():
	for website in getWebsites():
		websiteFilter(website)

if __name__ == '__main__':
	main()
