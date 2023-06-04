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

def get_Description(driver: WebDriver, url: str) -> str:
    driver.get(url)
    table_element = driver.find_element(By.TAG_NAME, 'table')
    p_tag = table_element.find_element(By.TAG_NAME, 'p')
    result = p_tag.text
    
    return result

def embed_from_dict(data: dict, driver: WebDriver) -> discord.Embed:
    description:str = get_Description(driver=driver, url=data['reference'])
    embed = discord.Embed(title=data['name'],
                          url=data['reference'],
                          description=description,
                          colour = discord.Colour.from_str('#FFB7C5'))
    embed.set_author(name="Watch-sama")
    embed.set_image(url=data['image'])
    return embed
    

def make_embeds(key: str) -> list[discord.Embed]: # Take a list from the json and create the embeds
    driver = SeleniumWrapper.MALSeleniumWrapper.get_WebDriver()    
    with open('watchsama/cogs/mal/JSON/anime_data.json', 'r') as openfile:
        anime_json = json.load(openfile)
    anime_list: list[dict] = anime_json[key]
    embeds =[]
    for entry in anime_list:
        embed = embed_from_dict(data=entry, driver=driver)
        embeds.append(embed)
    # embeds = [embed_from_dict(data=entry, driver=driver) for entry in anime_list]
    driver.close()
    return embeds