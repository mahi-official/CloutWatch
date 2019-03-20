import discord_config as dc   #contains the discord bot token

# Import discord and asynico libraries
#import discord     #API wrapper for Discord - https://github.com/Rapptz/discord.py
#import asyncio     #Asynchronous library for executing code when a message is recieved from discord
import time
import datetime
import json
import requests

import getNotification

def main(client):
	lastnotification = ''
	shoe = {}

	baseURL = "https://discordapp.com/api/channels/{}/messages".format('554609024071499776')
	s = { 
		"embed": {
			"title": "TITLE",
			"url": "https://www.linkToShoe.com",
			"color": 7157618,
			"timestamp": "{}".format(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")),
			"footer": {
				"icon_url": "https://media.discordapp.net/attachments/550708604697706498/554795532908888068/Black.png?width=645&height=645",
				"text": "brought to you by Cloutwatch X Rocket.io"
			},
			"thumbnail": {
				"url": "https://www.linkToPicture.com/pic.jpeg"
			},
			"image": {
				"url": ""
			},
			"author": {
				"name": "Rocket.io",
				"url": "http://rocket.io/",
				"icon_url": "https://media.discordapp.net/attachments/550708604697706498/554795649829437474/Rocket_IO_Logo.png?width=645&height=645"
			},
			"fields": [
				{
					"name": "Price",
					"value": "PRICE",
					"inline": False
				},
				{
					"name": "SIZES",
					"value": "[1,2,3,4,5,6,7]",
					"inline": True
				}
			]
		}
	}

	while True:


		notification = getNotification.get('nike')
		if(lastnotification != notification):
			shoe = notification[0]
			if(shoe['type'] == "new"):
				s['embed']['author']['name'] = "Rocket.io 	NEW DROP!"
				s['embed']['timestamp'] = str(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f"))
				s['embed']['title'] = shoe['name']
				s['embed']['url'] = shoe['link']
				s['embed']['thumbnail']['url'] = shoe['pictures'][0]
				s['embed']['fields'][0]['value'] = shoe['price']
				s['embed']['fields'][1]['value'] = shoe['available']

			elif(shoe['type'] == "price"):
				string = "@everyone PRICE CHANGE! {} is now available for {} at {}".format(shoe['name'], shoe['price'], shoe['link'])
			elif(shoe['type'] == "available"):
				string = "@everyone NEW SIZES AVAILABLE! {} now has {} sizes available for {} at {}".format(shoe['name'], shoe['available'], shoe['price'], shoe['link'])
			

			POSTedJSON =  json.dumps(s)

			print(s)

			headers = { "Authorization":"Bot {}".format(dc.discord_token),
									"User-Agent":"CloutWatch (v1.0.0)",
									"Content-Type":"application/json", }

			r = requests.post(baseURL, headers = headers, data = POSTedJSON)

			lastnotification = notification

		time.sleep(1)

main("boop")
