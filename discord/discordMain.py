# Author: Travis-Owens & ya boy Mathis
# Date: 2018-1-29
# Project: CloutWatch
# File-Discription: This file uses the async library to provide real-time response to messages posted on discord

# Import discord_config file
import discord_config as dc   #contains the discord bot token

# Import discord and asynico libraries
import discord     #API wrapper for Discord - https://github.com/Rapptz/discord.py
import asyncio     #Asynchronous library for executing code when a message is recieved from discord
import threading

import databaseChecker
import getNotification

threads = []

def callDatabaseChecker(client):
	databaseChecker.main(client)

def createThread(client):
	t = threading.Thread(target=callDatabaseChecker, args=(client,))
	threads.append(t)
	t.start()

client = discord.Client()   #Create a disord.Client object for handling messages

# This function will print information when the bot has successfully logged into the Discord API
@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('\n')
	createThread(client)


# this function will execute when a message is sent to a channel that the discord bot has read access
@client.event
async def on_message(message):
	# Common Discord.py Functions
	# - message.content = The content of the received message
	# - message.channel = The discord channel of the received message
	# - message.author.server_permissions.administrator = Returns True if the user has admin permissions in the current discord server

	if (message.author.id != client.user.id):   # Prevent the bot from responding to itself and creating a loop
		# Example conditions
		if message.content.lower().startswith('!Spark'):
			# Execute this code
			response = '!Spark Command Recieved.'

			# Send message back to the Discord channel
			await client.send_message(message.channel, response)

		elif message.content.lower().startswith('!s'):
			# Execute this code

			msgContent = str(message.content[len('!S'):].strip())
			if(msgContent != ""):
				if(msgContent.lower() == "nike"):
					await client.send_message(message.channel, "Got it! Fetching information, hang tight!")
					await client.send_message(message.channel, getNotification.get("nike"))
				elif(msgContent.lower() == "nike10"):
					#await client.send_message(message.channel, "Got it! Fetching information, hang tight!")
					#response = getNotification.get10("nike")
					#for item in response:
					#	await client.send_message(message.channel, item)
					pass	
				else:
					response = "Ayy there, I haven't built that yet!"
					await client.send_message(message.channel, response)
			else:
				response = "You need to actually say something, cuz idk what you want me to do!"
				await client.send_message(message.channel, response)

client.run(dc.discord_token)     #Start the async event listeners, dc.discord_token is located in discord_config.py
