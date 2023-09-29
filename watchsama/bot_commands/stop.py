import discord
from discord.ext import commands

def stop(bot):
    @bot.command()
    async def stop(ctx: commands.Context) -> discord.Message:
        #Need to add check so that this cant be called outside of test guild
        await ctx.send(f'Goodbye {ctx.author.name}!')
        await bot.close()
