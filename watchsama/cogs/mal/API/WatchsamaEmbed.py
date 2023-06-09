import datetime
import json
import time

import discord
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import ChromeOptions

import watchsama.cogs.mal.API.MALSelenium as SeleniumWrapper


def get_Description(driver: WebDriver, url: str) -> str: #This uses the webdriver to connect and get the url
    driver.get(url)
    table_element = driver.find_element(By.TAG_NAME, 'table')
    p_tag = table_element.find_element(By.TAG_NAME, 'p')
    result = p_tag.text
    
    return result

def general_embed_from_dict(data: dict, driver: WebDriver) -> discord.Embed:  # This converts the data from the JSON into a general Embed foir discord 
    description:str = get_Description(driver=driver, url=data['reference'])
    embed = discord.Embed(title=data['name'],
                          url=data['reference'],
                          description=description,
                          colour = discord.Colour.from_str('#FFB7C5'))
    embed.set_author(name="Watch-sama")
    embed.set_image(url=data['image'])
    return embed
    

def make_general_embeds(key: str) -> list[discord.Embed]: # Take a list from the json and create the general embeds

    #TODO: Make this into a generator so that we can get 10 everytime!

    driver: WebDriver = SeleniumWrapper.MALSeleniumWrapper.get_WebDriver()    
    with open('watchsama/cogs/mal/JSON/anime_data.json', 'r') as openfile:
        anime_json = json.load(openfile)
    anime_list: list[dict] = anime_json[key]
    embeds =[]
    for entry in anime_list:
        embed = general_embed_from_dict(data=entry, driver=driver)
        embeds.append(embed)
    driver.close()
    return embeds

# What if we make them in batches and then load more when the user gets to that point?







#TODO: WORk on these later

# def make_watching_embeds() -> list[discord.Embed]:
#     driver: WebDriver = SeleniumWrapper.MALSeleniumWrapper.get_WebDriver()
#     with open('watchsama/cogs/mal/JSON/anime_data.json', 'r') as openfile:
#         anime_json = json.load(openfile)
#     anime_list: list[dict] = anime_json["Watching"]
#     embeds = []
#     for entry in anime_list:
#         pass


# def progress_bar(current:int, end: int):
#     emojis = get_emotes()
#     hs = emojis[0]
#     hm = emojis[1]
#     he = emojis[2]
#     em = emojis[3]
#     ee = emojis[4]
#     fs = emojis[5]
#     fm = emojis[6]
#     #10 length 
#     percent = (current/end *10) // 1 + 1
#     if percent == 0:
#         pass