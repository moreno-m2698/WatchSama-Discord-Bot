import discord
from discord.ext import commands

def stop(bot):
    @bot.command()
    async def stop(ctx: commands.Context) -> discord.Message:
        await ctx.send(f'Goodbye {ctx.author.name}!')
        await bot.close()
