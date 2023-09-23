import json
import random

import discord
from discord.ext import commands


from .view.MALView import MALView

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
        # rawData = SeleniumRawData.create_Anime_List(status=status)
        rawData = [
            {
                "name": "Cells at Work!",
                "reference": "https://myanimelist.net/anime/37141/Hataraku_Saibou",
                "status": "completed",
                "image": "https://cdn.myanimelist.net/r/192x272/images/anime/1141/117446.webp?s=507f46109160673787d31ab1ca40227d",
                "media": "TV"
            },
            {
                "name": "Death Parade",
                "reference": "https://myanimelist.net/anime/28223/Death_Parade",
                "status": "completed",
                "image": "https://cdn.myanimelist.net/r/192x272/images/anime/5/71553.webp?s=9ff22a629b680f6051e9aceb312e88d6",
                "media": "TV"
            }
        ]

        embeds = []
        for anime in rawData:
            url = anime['reference']
            print(url)
            title= anime['name']
            print(title)
            media =  anime['media']
            status = anime['status']
            image = anime['image']
            embed = BasicEmbed(url = url, title = title, media = media, status = status, description = None, image = image)
            embeds.append(embed)
    

        index = 1
        view = MALViewBuilder.create_View(embed_index=index)
        print(view.embed_index)
       

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
