from typing import Optional, Union
import discord
from discord.emoji import Emoji
from discord.enums import ButtonStyle
from discord.ext import commands
from discord.partial_emoji import PartialEmoji
from discord.ui import View, Button
import random
import time



from selenium.webdriver.remote.webdriver import WebDriver


from view.WatchingView import WatchingView
from API.MALSeleniumWrapper import MALSeleniumWrapper, AnimeEntry

#---------------------------------------------------------------------------

mal_username: str = "gabslittlepogger"
mal_password: str = 'qaz890poimnb'
intents = discord.Intents.default()
intents.message_content = True
watchsama = commands.Bot(command_prefix="!", intents=intents)
watchsama.watchinganime: list[discord.Embed] = []
#-------------------------------------------------------------------------



        

#----------------------------------------------------------------------------------------------------

#TODO: Choicing random anime feature
#Create reroll button
#Create url to gabslittlepogger button
#Add timeout

#Create a view to interact with embed
#Needs to have a single track reroll thats tracked with date
#Should I synthesize or make from a cached list

def create_embed(data: AnimeEntry):
    color = discord.Colour.from_str('#FFB7C5')
    title: str = data.title
    result = discord.Embed(title=title,color=color)
    result.set_image(url=data.image)
    return result

#----------------------------------------------------------------------------------

@watchsama.event
async def on_ready() -> None:
    print('Watchsama is watching')
    url: str ='https://myanimelist.net/login.php?from=%2F&'
    wrapper = MALSeleniumWrapper
    driver: WebDriver = wrapper.get_WebDriver()
    wrapper.account_Login(driver=driver, url=url, username=mal_username, password=mal_password)
    data: list[AnimeEntry] = wrapper.get_Data(driver)
    embeds: list[discord.Embed] = list(map(create_embed, data))
    watchsama.watchinganime = embeds
    driver.close()
    await watchsama.guilds[0].text_channels[0].send('Watch-sama is running')

@watchsama.command()
async def stop(ctx: commands.Context) -> discord.Message:
    await ctx.send(f'Goodbye {ctx.author.name}!')
    await watchsama.close()
  
@watchsama.command()
async def refresh(ctx: commands.Context) -> discord.Message: #Allows user to refresh embed list if there was a manual updte to MAL after startup
    url: str ='https://myanimelist.net/login.php?from=%2F&'
    wrapper = MALSeleniumWrapper
    driver: WebDriver = wrapper.get_WebDriver()
    wrapper.account_Login(driver=driver, url=url, username=mal_username, password=mal_password)
    data: list[AnimeEntry] = wrapper.get_Data(driver)
    await ctx.send(f"Successful MAL login: Check Log")
    embeds: list[discord.Embed] = list(map(create_embed, data))
    watchsama.watchinganime = embeds
    driver.close()

@watchsama.command()
async def view_test(ctx: commands.Context) -> discord.Message:
    
    embeds: list[discord.Embed] = watchsama.watchinganime
    view = WatchingView()
    index = 0
    message: discord.Message = ctx.send(embed=embeds[index], view = view)
    view.message_awareness(message)
    view.embeds_awareness(embeds)
    view.embed_index_awareness(index)
    await message
    
@watchsama.command()
async def watch(ctx: commands.Context) -> discord.Message:
    pass



#TODO: ADD TO ENV VARIABLE
watchsama.run('MTEwMzM5NDU4OTQ3NTM0ODU2Nw.G2x86i.U4d9iaNSjTC93aMEA10hHiK1k_7C-w4baw4C3A')