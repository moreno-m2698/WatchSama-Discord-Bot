import json
import random

import discord
from discord.ext import commands


from .view.MALView import MALView
from .API.MALController import cache_anime_meta
from .API.WatchsamaEmbed import make_general_embeds
from .view.HoldView import HoldView


class MALCog(commands.Cog):

    ''' Honestly makes more sense for this cog to validate whether or not there is anything in cache'''
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def watching(self, ctx: commands.Context) -> discord.Message:
        ''' This command will give the user back a discord message that shows some of the shows they are watching'''
        pass

    @commands.command()
    async def complete(self, ctx: commands.Context) -> discord.Message:
        ''' This command will give the user back a discord message that shows what shows they have completed'''
        pass

    @commands.command()
    async def refresh(self, ctx: commands.Context) -> discord.Message:
        ''' This command will give refresh the anime that is currently being cached if caching is implemented and the give user feedback'''
        pass

    @commands.command()
    async def search(self, ctx: commands.Context) -> discord.Message:
        ''' This command will allow user to make a search on MAL and return a list of 5 shows that meet the description'''
        pass

    


    @commands.command()
    async def hold(self, ctx: commands.Context) -> discord.Message:
        embeds: list[discord.Embed] = make_general_embeds(3)
        embed_index: int = 0
        view = HoldView()
        message: discord.Message = ctx.send(content = 'Here are the series that you have on hold.', embed=embeds[embed_index], view = view)
        view.message_awareness(message)
        view.embeds_awareness(embeds)
        view.embed_index_awareness(embed_index)
        await message


    @commands.command()
    async def refresh(self, ctx: commands.Context) -> discord.Message: #Allows user to refresh embed list if there was a manual update to MAL after startup
        keys = ['1', '2', '3', '4', '6']
        for key in keys:
            cache_anime_meta(key)
        await ctx.send("Anime List has been updated")


async def cog_setup(bot: commands.Bot):
    await bot.add_cog(MALCog(bot))