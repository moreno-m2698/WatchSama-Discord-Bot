import json
import random

import discord
from discord.ext import commands


from .view.MALView import MALView

from .API.RawAnimeData import SeleniumRawData

class MALCog(commands.Cog):

    ''' Honestly makes more sense for this cog to validate whether or not there is anything in cache'''

    #NOTE: currently We shall assume no caching and will pull the data from MAL
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def watching(self, ctx: commands.Context) -> discord.Message:
        ''' This command will give the user back a discord message that shows some of the shows they are watching'''
        pass

    @commands.command()
    async def complete(self, ctx: commands.Context) -> discord.Message:

        ''' This command will give the user back a discord message that shows what shows they have completed'''


        rawData = SeleniumRawData.create_Anime_List()

        message: discord.Message = ctx.send(content = "Testing this function")
        await message
   

    @commands.command()
    async def refresh(self, ctx: commands.Context) -> discord.Message:
        ''' This command will give refresh the anime that is currently being cached if caching is implemented and the give user feedback'''
        pass

    @commands.command()
    async def search(self, ctx: commands.Context) -> discord.Message:
        ''' This command will allow user to make a search on MAL and return a list of 5 shows that meet the description'''
        pass




async def cog_setup(bot: commands.Bot):
    await bot.add_cog(MALCog(bot))