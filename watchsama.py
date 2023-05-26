import discord
from discord.ext import commands
import random
from selenium.webdriver.remote.webdriver import WebDriver

from watchsama.cogs.mal.PlanToWatch.plantowatch import cache_anime_embeds
import json
import os

#---------------------------------------------------------------------------

mal_username: str = "gabslittlepogger"
mal_password: str = 'qaz890poimnb'
intents = discord.Intents.default()
intents.message_content = True
watchsama = commands.Bot(command_prefix="!", intents=intents)
watchsama.plantowatch_range: range | None = None
#-------------------------------------------------------------------------

#TODO: Choicing random anime feature
#Add timeout
#Add description to first <br>

#Create a view to interact with embed
#Needs to have a single track reroll thats tracked with date
#Should I synthesize or make from a cached list



#----------------------------------------------------------------------------------

@watchsama.event
async def on_ready() -> None:
    print('Watchsama is watching')
    # cache_anime_embeds()

    #TODO: find a way to cache the range so u dont wanna die

    check_file = os.stat('anime_embed.json').st_size
    if check_file == 0 or check_file == 2:
        cache_anime_embeds()
        print("populating json")
    await watchsama.guilds[0].text_channels[0].send('Watch-sama is running') #Find out how to get her to talk properly

@watchsama.command()
async def stop(ctx: commands.Context) -> discord.Message:
    await ctx.send(f'Goodbye {ctx.author.name}!')
    await watchsama.close()
  
@watchsama.command()
async def refresh(ctx: commands.Context) -> discord.Message: #Allows user to refresh embed list if there was a manual updte to MAL after startup
    cache_anime_embeds()
    await ctx.send("Anime List has been updated")

@watchsama.command()
async def watch(ctx: commands.Context) -> discord.Message: #Look into making this a singleton instance so that it cant be cheesed
    #TODO: persist datetime into text

    anime_range: range = watchsama.plantowatch_range
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



#TODO: ADD TO ENV VARIABLE
watchsama.run('MTEwMzM5NDU4OTQ3NTM0ODU2Nw.G2x86i.U4d9iaNSjTC93aMEA10hHiK1k_7C-w4baw4C3A')