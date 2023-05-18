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

#---------------------------------------------------------------------------

mal_username = "gabslittlepogger"
mal_password = 'qaz890poimnb'
intents = discord.Intents.default()
intents.message_content = True
watchsama = commands.Bot(command_prefix="!", intents=intents)

#-------------------------------------------------------------------------

class MALSeleniumWrapper():
    def __init__(self):
        self.url = 'https://myanimelist.net/'
    
    def createConnection(self):
        driver = webdriver.Chrome()
        return driver
    
    def accountLogin(self, driver, url, username, password):
        driver.get(url)
        loginElement = driver.find_element(By.ID, 'loginUserName')
        passwordElement = driver.find_element(By.ID, 'login-password')
        loginButton = driver.find_element(By.CLASS_NAME, "btn-recaptcha-submit")
        loginElement.send_keys(username)
        passwordElement.send_keys(password)
        loginButton.click()
        time.sleep(2)
        driver.get('https://myanimelist.net/animelist/gabslittlepogger')

    def getEntries(self, driver):
        animeList = driver.find_elements(By.CLASS_NAME, 'list-item')
        return animeList

    def getTitle(self, element):
        rawTitle = element.find_element(By.CLASS_NAME, 'title')
        title = rawTitle.find_element(By.TAG_NAME, 'a').text
        return title
    
    def getStatus(self, element):
        statusElement = element.find_element(By.CLASS_NAME, 'status')
        rawClasses = statusElement.get_attribute('class')
        classList = list(rawClasses.split(" "))
        status = classList[2]

        return status
    
    def getData(self, driver):
        rawData = self.getEntries(driver)
        result = []
        for element in rawData:
            refinement = [self.getTitle(element), self.getStatus(element)]
            result.append(refinement)
        
        return result


    def findRange(driver): #Assume we are not finding a new webpage
        animeTable = driver.find_elements(By.CLASS_NAME, 'completed')
        parentTest = lambda data: data.parent #This returns the driver

        #Need to combine into tuple or list to process
        #Will create big list and then prune:
        # Must cache this list
        #[status,number,image,title]
        # Might want to look at beautifulsoup lib so that we arent brute forcing this
        testArray = list(map(parentTest, animeTable[1:]))
        parentTagTest = lambda data: type(data)
        testArray2 = list(map(parentTagTest, testArray))
        time.sleep(1)
        print(animeTable)
        print(testArray)
        print(testArray2)
        return testArray


#----------------------------------------------------------------------------------------------------


@watchsama.event
async def on_ready():
    print('Watchsama is watching')

@watchsama.command()
async def stop(ctx):
    await ctx.send(f'Goodbye {ctx.author.name}!')
    await watchsama.close()
  
@watchsama.command()

async def test(ctx):
    url ='https://myanimelist.net/login.php?from=%2F&'
    wrapper=MALSeleniumWrapper()
    driver = wrapper.createConnection()
    wrapper.accountLogin(driver=driver, url=url, username=mal_username, password=mal_password)
    data = wrapper.getData(driver)
    await ctx.send(f"Successful MAL login: Check Log")
    print(data)

    #await ctx.send(f"Here are the no Wathc {noWatch}")
    driver.close()

watchsama.run('MTEwMzM5NDU4OTQ3NTM0ODU2Nw.G2x86i.U4d9iaNSjTC93aMEA10hHiK1k_7C-w4baw4C3A')