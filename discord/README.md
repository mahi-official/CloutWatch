# Discord Interface for CloutWatch

This directory contains the scripts necessary to interface with the Discord API.

### discord_config.py

This file currently only contains the API token for the discord bot.
A token can be acquired by creating an application at: https://discordapp.com/developers/applications/

*Note: The Discord Bot must be a member of the server and have permissions in the channels it's used in.*

### discord_async.py

This script contains the asynchronous functions for receiving messages from Discord.

Example Usage:
```py
if message.content.startswith('!CloutWatch'):
        # Execute this code
        response = '!CloutWatch Command Recieved.'

        # Send message back to the Discord channel
        await client.send_message(message.channel, response)
```

### discord_message_send.py

This script uses the Requests library to post a message to a discord channel.

variables required:
  -discord_channel_ID = The channel ID defined by Discord.
  -message            = The message you wish to send.

Example usage:
```py
import discord_message_send as discord

discord.send_message('503666100345765900', 'test')
```
