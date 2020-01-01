import discord
from discord.ext import commands

from data_transfer import DataHandler

bot = commands.Bot(command_prefix='!')

class BotBehaviour:
    def __init__(self):
        pass
        # self.bot = bot
    
    def bot_init(self):
        return bot

    @bot.command()
    async def link(ctx):
        await ctx.send('https://drive.google.com/drive/folders/1agXJUagpMYhwHSRTf0MpjvSlGcFwfIGt?usp=sharing')
        # pass

    @bot.command(pass_context=True)
    # @log_function
    async def ping(ctx, nums: int):
        # await asyncio.sleep(2)
        await ctx.send('pong')
        channel = ctx.message.channel
        messages = await channel.history(limit=20).flatten()
        for elem in messages:
            if elem.attachments:
                print(elem.attachments[0].url)
            else:
                pass
                # print(elem.content)

    @bot.command(pass_context=True)
    # @log_function
    async def upload(ctx, mAmount: int):
        if (not mAmount):
            mAmount = 1
        dhandler = DataHandler()
        channel = ctx.message.channel
        messages = await channel.history(limit=mAmount).flatten()
        await ctx.send("BOT STATUS: 'Started uploading...'")
        for i, elem in enumerate(messages):
            if elem.attachments:
                data = []
                data.append(elem)
                dhandler.upload(data)
            else:
                pass
                # data = None
                # print(elem.content)
        await ctx.send("BOT STATUS: 'Upload complete'")