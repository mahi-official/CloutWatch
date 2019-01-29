# Author: Travis-Owens
# Date: 2018-1-29
# Project: CloutWatch
# File-Discription: This file will post a message to the defined discord channel

# Import discord_config file
import discord_config as dc   #contains the discord bot token

# Import requests and json libraries
import requests
import json


# Input:
#   discord_channel_ID =  The ID of the disocrd channel you're sending the message to.
#   message            =  A String with the desired message
def send_message(discord_channel_ID, message):
    # The message is POSTed to Discord via the Requests library in a JSON format

    try:
        # BaseURL is where the message needs to be posted
        baseURL = baseURL = "https://discordapp.com/api/channels/{}/messages".format(discord_channel_ID)

        # POSTedJSON is the message formated into a json dump
        POSTedJSON =  json.dumps({"content":message})

        # Headers for the POST request
        headers = { "Authorization":"Bot {}".format(dc.discord_token),
                    "User-Agent":"CloutWatch (v1.0.0)",
                    "Content-Type":"application/json", }

        #Submit the request to Discord
        r = requests.post(baseURL, headers = headers, data = POSTedJSON)

    except Exception as e:
        # @Mathisco-01 : Add in error loggin function here
        print("Exception in discord_message_send.py: " + e)
