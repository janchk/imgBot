# Work with Python 3.6
import discord
import asyncio
# import urllib3
import requests
from discord.ext import commands
from functools import wraps

import os

from bot import bot_commands
from data_transfer import DataHandler

if os.path.exists('credentials/discord_credentials.txt'):
            with open('credentials/discord_credentials.txt', 'r') as token:
                TOKEN = token.read()

SCOPES = ['https://www.googleapis.com/auth/drive']

client = discord.Client()

dhandler = DataHandler()

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
    if message.attachments:
        dhandler.upload([message])

bot.run(TOKEN)
