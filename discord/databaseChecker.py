import discord_config as dc   #contains the discord bot token

# Import discord and asynico libraries
import discord     #API wrapper for Discord - https://github.com/Rapptz/discord.py
import asyncio     #Asynchronous library for executing code when a message is recieved from discord
import time
import json
import requests

import getNotification

def main(client):
	lastnotification = ''
	shoe = {}

	baseURL = "https://discordapp.com/api/channels/{}/messages".format('546839466569105420')

	while True:


		notification = getNotification.get('nike')
		if(lastnotification != notification):
			shoe = notification[0]
			if(shoe['type'] == "new"):
				string = "@everyone NEW DROP! {} is now available for {} at {}".format(shoe['name'], shoe['price'], shoe['link'])
			elif(shoe['type'] == "price"):
				string = "@everyone PRICE CHANGE! {} is now available for {} at {}".format(shoe['name'], shoe['price'], shoe['link'])
			elif(shoe['type'] == "available"):
				string = "@everyone NEW SIZES AVAILABLE! {} now has {} sizes available for {} at {}".format(shoe['name'], shoe['available'], shoe['price'], shoe['link'])
			

			print(string)
			
			POSTedJSON =  json.dumps({"content":string})

			headers = { "Authorization":"Bot {}".format(dc.discord_token),
						"User-Agent":"CloutWatch (v1.0.0)",
						"Content-Type":"application/json", }

			r = requests.post(baseURL, headers = headers, data = POSTedJSON)

			lastnotification = notification

		time.sleep(1)


