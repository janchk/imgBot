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
    # @log_function
    async def ping(ctx):
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

    @bot.command()
    # @log_function
    async def download(ctx):
        # await asyncio.sleep(2)
        # await ctx.send('pong')
        dhandler = DataHandler()
        channel = ctx.message.channel
        messages = await channel.history(limit=100).flatten()
        await ctx.send("BOT STATUS: 'Started downloading...'")
        for i, elem in enumerate(messages):
            # await ctx.message.delete()
            # await client.delete_message("{} from {} are downloaded".format(i, 100))
            if elem.attachments:
                data = []
                data.append(elem)
                dhandler.upload(data)
            else:
                pass
                # data = None
                # print(elem.content)
        await ctx.send("BOT STATUS: 'Download complete'")