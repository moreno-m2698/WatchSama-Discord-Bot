import json
import random


import discord
from discord.ext import commands

from .view.WatchingView import WatchingView
from .API.MALSeleniumWrapper import cache_anime_embeds

#TODO: Access different lists using different jsons by adjusting url path
# Currently Watching: ?status=1 ,Completed =2, On Hold =3, Dropped =4, Plan To Watch =5



class MAL(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    #TODO: convert watchsama command into cog
    @commands.command()
    async def watch(self, ctx: commands.Context) -> discord.Message: #Look into making this a singleton instance so that it cant be cheesed
    #TODO: persist datetime into text

        with open('anime_embed.json', 'r') as openfile:
            embed_jsons: list[dict] = json.load(openfile)['embeds']
            anime_range: list[int] = json.load(openfile)['plan_to_watch_range']
        
        embeds: list[discord.Embed] = list(map(discord.Embed.from_dict, embed_jsons))
        view = WatchingView()
        index = random.randint(anime_range[0], anime_range[1])
        print(index)
        message: discord.Message = ctx.send(embed=embeds[index], view = view)
        view.message_awareness(message)
        view.embeds_awareness(embeds)
        view.embed_index_awareness(index)
        view.embed_range_awareness(anime_range)
        await message

    @commands.command()
    async def refresh(self, ctx: commands.Context) -> discord.Message: #Allows user to refresh embed list if there was a manual updte to MAL after startup
        cache_anime_embeds()
        await ctx.send("Anime List has been updated")


async def setup(bot):
    await bot.add_cog(MAL(bot))