import discord
import time

from discord.ext import commands

from watchsama.tools.WatchSamaEmbed import WatchSamaEmbed


def __init__(bot):
    ping(bot)
    stop(bot)
    info(bot)

def stop(bot: discord.Client):
    @bot.command()
    async def stop(ctx: commands.Context) -> discord.Message:
        #Need to add check so that this cant be called outside of test guild
        await ctx.send(f'Goodbye {ctx.author.name}!')
        await bot.close()

def info(bot: discord.Client):
    @bot.command()
    async def info(ctx: commands.Context) -> discord.Message:
        embed = WatchSamaEmbed(title="WatchSama", url = 'https://github.com/moreno-m2698/Watchsama-Discord-Bot', description='Developers: keopi.')
        await ctx.send(embed=embed)


def ping(bot:discord.Client):
    @bot.command()
    async def ping(ctx:commands.Context) -> discord.Message:
        await ctx.send(f'Pong! {round(bot.latency * 1000)} ms')

