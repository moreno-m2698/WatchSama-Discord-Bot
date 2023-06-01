import json
import random


import discord
from discord.ext import commands

from .view.WatchingView import WatchingView
from .API.MALSelenium import cache_anime_meta

#TODO: Access different lists using different jsons by adjusting url path
# Currently Watching: ?status=1 ,Completed =2, On Hold =3, Dropped =4, Plan To Watch =5



class MALCog(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    #TODO: convert watchsama command into cog
    @commands.command()
    async def watch(self, ctx: commands.Context) -> discord.Message: #Look into making this a singleton instance so that it cant be cheesed
    #TODO: persist datetime into text

        with open('watchsama/cogs/mal/JSON/anime_embed.json', 'r') as openfile:
            cache_json = json.load(openfile)


        embed_dict = cache_json['embeds']
        anime_range = cache_json["plan_to_watch_range"]
        
        embeds: list[discord.Embed] = list(map(discord.Embed.from_dict, embed_dict))
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
        cache_anime_meta()
        await ctx.send("Anime List has been updated")


async def cog_setup(bot: commands.Bot):
    await bot.add_cog(MALCog(bot))