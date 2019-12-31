# Work with Python 3.6
import discord
import asyncio
# import urllib3
import requests
from discord.ext import commands
from functools import wraps

import os

from bot import bot_commands
# from data_transfer import DataHandler

if os.path.exists('credentials/discord_credentials.txt'):
            with open('credentials/discord_credentials.txt', 'r') as token:
                TOKEN = token.read()

SCOPES = ['https://www.googleapis.com/auth/drive']

client = discord.Client()
# http = urllib3.PoolManager()
# bot = commands.Bot(command_prefix='$', description='A bot that greets the user back.')
# def log_function(func):
#     @wraps(func)
#     async def wrapped_func(ctx):
#         print("\nexecuting %s" %func.__name__)
#         print("\nargs is %s" %ctx)
#         await asyncio.sleep(1)
#         func(ctx)
#     return wrapped_func

# bot = commands.Bot(command_prefix='!')

bot_behaviour = bot_commands.BotBehaviour()
bot = bot_behaviour.bot_init()

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.run(TOKEN)
