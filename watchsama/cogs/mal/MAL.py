import json
import random

import discord
from discord.ext import commands
from selenium import webdriver

from .API.RawAnimeData import SeleniumRawData
from .API.Embeds import BasicEmbed
from .API.ui.ViewBuilder import MALViewBuilder
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

        status = 2
        driver = webdriver.Chrome()
        print("A WebDriver has been initiated")
        rawData = SeleniumRawData.create_Anime_List(driver = driver, status=status)
        chunker = 5
        data_for_view = list(SeleniumRawData.list_chunking(rawData, chunker))
        embeds = []
        for anime in data_for_view[0]:
            url = anime['reference']
            title= anime['name']
            media =  anime['media']
            status = anime['status']
            image = anime['image']
            description = SeleniumRawData.get_Description(driver, url)
            embed = BasicEmbed(url = url, title = title, media = media, status = status, description = description, image = image)
            embeds.append(embed)
        driver.close()
        print("WebDriver is now closed")
        index = 0
        view = MALViewBuilder.create_View(embeds = embeds, data = data_for_view)
        message: discord.Message = ctx.send(content = f"Testing this function:", view = view, embed = embeds[index])
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
