import discord_config as dc   #contains the discord bot token

# Import discord and asynico libraries
#import discord     #API wrapper for Discord - https://github.com/Rapptz/discord.py
#import asyncio     #Asynchronous library for executing code when a message is recieved from discord
import time
import datetime
import random
import json
import requests
import ast

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
				"url": "https://www.linkToPicture.com/pic.jpeg"
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
			print("Sending notification")
			shoe = notification[0]
			s['embed']['timestamp'] = str(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f"))
			s['embed']['title'] = shoe['name']
			s['embed']['url'] = shoe['link']
			pics = ast.literal_eval(shoe['pictures'])
			s['embed']['thumbnail']['url'] = pics[random.randint(0,len(pics))]
			s['embed']['fields'][0]['value'] = shoe['price']
			s['embed']['fields'][1]['value'] = shoe['available']
			if(shoe['type'] == "new"):

				s['embed']['author']['name'] = "Rocket.io 	NEW DROP!"
				
				pass
			elif(shoe['type'] == "price"):

				s['embed']['author']['name'] = "Rocket.io 	PRICE CHANGE!"
			elif(shoe['type'] == "available"):
				s['embed']['author']['name'] = "Rocket.io 	NEW SIZES AVAILABLE!"

			POSTedJSON =  json.dumps(s)

			headers = { "Authorization":"Bot {}".format(dc.discord_token),
									"User-Agent":"CloutWatch (v1.0.0)",
									"Content-Type":"application/json", }

			r = requests.post(baseURL, headers = headers, data = POSTedJSON)

			lastnotification = notification

		time.sleep(1)

main("boop")