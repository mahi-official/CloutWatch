discord_token = 'NTQyMDQ3NDAwNDE2NTA5OTcz.D0odww.Z6RMtOrI4SWY_Ke9DhDEQbdz8fI'

import discord
import json
import requests


print("Logging in")
client = discord.Client()
client.run(discord_token) 
print("login completed")

baseURL = "https://discordapp.com/api/channels/{}/messages".format('546528282284392448')

while True:
	string = input("Say smthn: ")
	POSTedJSON =  json.dumps({"content":string})

	headers = { "Authorization":"Bot {}".format(discord_token),
				"User-Agent":"CloutWatch (v1.0.0)",
				"Content-Type":"application/json", }

	r = requests.post(baseURL, headers = headers, data = POSTedJSON)