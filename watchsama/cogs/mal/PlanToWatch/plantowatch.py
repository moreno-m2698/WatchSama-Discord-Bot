import discord
from discord.ext import commands
from selenium.webdriver.remote.webdriver import WebDriver
import json
import random

#-----------------------
import discord
from discord.ext import commands

from ..view.WatchingView import WatchingView
from ..API.MALSeleniumWrapper import cache_anime_embeds




class PlanToWatch(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    #TODO: convert watchsama command into cog
    @commands.command()
    async def watch(self, ctx: commands.Context) -> discord.Message: #Look into making this a singleton instance so that it cant be cheesed
    #TODO: persist datetime into text

        anime_range: range = self.bot.plantowatch_range
        with open('anime_embed.json', 'r') as openfile:
            embed_jsons: list[dict] = json.load(openfile)
        
        embeds: list[discord.Embed] = list(map(discord.Embed.from_dict, embed_jsons))
        view = WatchingView()
        index = random.sample(anime_range,1)[0]
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


def setup(bot):
    bot.add_cog(PlanToWatch(bot))