import discord
from discord.ext import commands
import random
import datetime
import json
import time


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import requests

mal_username = "gabslittlepogger"
mal_password = 'qaz890poimnb'
intents = discord.Intents.default()
intents.message_content = True
watchsama = commands.Bot(command_prefix="!", intents=intents)


@watchsama.event
async def on_ready():
    print('Watchsama is watching')

@watchsama.command()
async def stop(ctx):
    await ctx.send(f'Goodbye {ctx.author.name}!')
    await watchsama.close()

class MALSeleniumWrapper():
    def __init__(self):
        self.url = 'https://myanimelist.net/'
    
    def createConnection():
        driver = webdriver.Chrome()
        return driver
    
    def accountLogin(driver,url, username, password):
        driver.get(url)
        loginElement = driver.find_element(By.ID, 'loginUserName')
        passwordElement = driver.find_element(By.ID, 'login-password')
        loginButton = driver.find_element(By.CLASS_NAME, "btn-recaptcha-submit")
        loginElement.send_keys(username)
        passwordElement.send_keys(password)
        loginButton.click()
        time.sleep(2)
        driver.get('https://myanimelist.net/animelist/gabslittlepogger')
        
    
    def titlesArray(driver):
        animeList = driver.find_elements(By.CLASS_NAME, 'list-item') #These are tbody
        # tbodyTotr = lambda tbody: tbody.find_element(By.CLASS_NAME, 'list-table-data')
        # trList = list(map(tbodyTotr,animeList))
        getTdClassTitle = lambda data: data.find_element(By.CLASS_NAME, 'title')
        rawTitleList = list(map(getTdClassTitle,animeList))
        getTitle = lambda data: data.find_element(By.TAG_NAME, 'a').text
        titleList = list(map(getTitle, rawTitleList))
        print(titleList)
        time.sleep(2)
        return titleList
    
    def findRange(driver): #Assume we are not finding a new webpage
        animeTable = driver.find_elements(By.CLASS_NAME, 'completed')
        parentTest = lambda data: data.parent #This returns the driver

        #Need to combine into tuple or list to process
        testArray = list(map(parentTest, animeTable[1:]))
        parentTagTest = lambda data: type(data)
        testArray2 = list(map(parentTagTest, testArray))
        time.sleep(1)
        print(animeTable)
        print(testArray)
        print(testArray2)
        return testArray

        



    
@watchsama.command()

async def test(ctx):
    url ='https://myanimelist.net/login.php?from=%2F&'
    driver = MALSeleniumWrapper.createConnection()
    MALSeleniumWrapper.accountLogin(driver=driver, url=url, username=mal_username, password=mal_password)
    #titles = MALSeleniumWrapper.titlesArray(driver=driver) 
    noWatch = MALSeleniumWrapper.findRange(driver=driver)
    await ctx.send(f"Successful MAL login: Check Log")
    #await ctx.send(f"Here is the list: {titles}")
    #await ctx.send(f"Here are the no Wathc {noWatch}")
    driver.close()

watchsama.run('MTEwMzM5NDU4OTQ3NTM0ODU2Nw.G2x86i.U4d9iaNSjTC93aMEA10hHiK1k_7C-w4baw4C3A')