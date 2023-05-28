import time

import discord
from discord.ext import commands

def __init__(bot):
    stop(bot)
    

def stop(bot):
    @bot.command()
    async def stop(ctx: commands.Context) -> discord.Message:
        await ctx.send(f'Goodbye {ctx.author.name}!')
        await bot.close()

