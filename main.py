import discord
from discord.ext import commands
import os
import asyncio
from decouple import config

#import all of the cogs
from help_cog import help_cog
from music_cog import music_cog

# intents = discord.Intents.default()
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

#remove the default help command so that we can write out own
bot.remove_command('help')


async def main():
    token = config("TOKEN")
    # print(token)
    async with bot:
        await bot.add_cog(help_cog(bot))
        await bot.add_cog(music_cog(bot))
        await bot.start(token)
        # print('bot started')

asyncio.run(main())

