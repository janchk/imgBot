# Work with Python 3.6
import discord
import asyncio
import requests
from discord.ext import commands
from functools import wraps

from credentials.get_credentials import get_discord_creds


from bot import bot_commands
from bot.bot_globals import WatchedChannels
from data_transfer import DataHandler

 
TOKEN = get_discord_creds()
SCOPES = ['https://www.googleapis.com/auth/drive']

client = discord.Client()
dhandler = DataHandler()
watched_channels = WatchedChannels()

bot_behaviour = bot_commands.BotBehaviour()
bot = bot_behaviour.bot_init()

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if (message.channel.id in watched_channels.data):
        print(message)
        if message.attachments:
            dhandler.upload([message])

bot.run(TOKEN)
