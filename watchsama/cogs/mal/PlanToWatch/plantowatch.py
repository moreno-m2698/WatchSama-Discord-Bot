import discord
from discord.ext import commands
import discord
from discord.ext import commands
import random
from selenium.webdriver.remote.webdriver import WebDriver
from watchsama.cogs.mal.view.WatchingView import WatchingView
from watchsama.cogs.mal.API.MALSeleniumWrapper import MALSeleniumWrapper, AnimeEntry
import json
import os



def get_to_anime_list() -> WebDriver:
    url: str ='https://myanimelist.net/login.php?from=%2F&'
    wrapper = MALSeleniumWrapper
    driver: WebDriver = wrapper.get_WebDriver()
    wrapper.account_Login(driver=driver, url=url, username=mal_username, password=mal_password)
    return driver

def cache_anime_embeds()-> None:
    wrapper = MALSeleniumWrapper
    driver = get_to_anime_list()
    data: list[AnimeEntry] = wrapper.get_Data(driver)
    embeds: list[discord.Embed] = list(map(create_embed, data))
    embeds_dict: list[dict] = list(map(discord.Embed.to_dict, embeds))
    embeds_json = json.dumps(embeds_dict, indent=4)
    with open("anime_embed.json", "w") as outfile:
        outfile.write(embeds_json)
    driver.close()
    watchsama.plantowatch_range = wrapper.getRandomizerRange(data)

def create_embed(data: AnimeEntry):
    color = discord.Colour.from_str('#FFB7C5')
    title: str = data.title
    result = discord.Embed(title=title,color=color)
    result.set_image(url=data.image)
    return result


class MAL(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    #TODO: convert watchsama command into cog