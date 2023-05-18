import discord
from discord.ext import commands
import random
import datetime
import json
import time


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

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
    
    def getImage(self, element):
        rawImage = element.find_element(By.CLASS_NAME, 'image')
        image = rawImage.find_element(By.TAG_NAME, 'img').get_attribute('src')
        return image
    
    def getData(self, driver):
        rawData = self.getEntries(driver)
        result = []
        for element in rawData:
            refinement = {
                'name': self.getTitle(element),
                'status': self.getStatus(element),
                'image': self.getImage(element)
            }
            result.append(refinement)
        
        return result
    
    def randomizerRange(self, data):
        initial = 0
        final = len(data) - 1
        for i in range(0, len(data)):
            if data[i]['status'] == 'plantowatch':
                initial = i
                break
            i += 1
        result = random.randint(initial, final)
        return result
        
    def findRange(driver): #Assume we are not finding a new webpage
        animeTable = driver.find_elements(By.CLASS_NAME, 'completed')
        parentTest = lambda data: data.parent #This returns the driver

        testArray = list(map(parentTest, animeTable[1:]))
        parentTagTest = lambda data: type(data)
        testArray2 = list(map(parentTagTest, testArray))
        time.sleep(1)
        print(animeTable)
        print(testArray)
        print(testArray2)
        return testArray

# [['A Silent Voice', 'completed', 'https://cdn.myanimelist.net/r/192x272/images/anime/1122/96435.webp?s=f8162c1735ac8075df9ba9974c934b24']] 
# This will be the test

#----------------------------------------------------------------------------------------------------

#Choicing random anime feature

#Create a view to interact with embed
#synthesize embed
#Needs to have a single track reroll thats tracked with date



def createEmbed(data):
    color = discord.Color.from_str('#FFB7C5')
    description = data['status']
    title= data['name']
    result = discord.Embed(title=title,color=color, description=description)
    result.set_image(url=data['image'])
    return result

#----------------------------------------------------------------------------------


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
    firstwatch = wrapper.randomizerRange(data)
    await ctx.send(f"Watching: {firstwatch}")
    print(data)

    #await ctx.send(f"Here are the no Wathc {noWatch}")
    driver.close()

@watchsama.command()
async def embed(ctx):
    
    testCase = [{'name': 'A Silent Voice', 'status': 'completed', 'image': 'https://cdn.myanimelist.net/r/192x272/images/anime/1122/96435.webp?s=f8162c1735ac8075df9ba9974c934b24'}]
    embed = createEmbed(testCase[0])
    await ctx.send(embed=embed)

watchsama.run('MTEwMzM5NDU4OTQ3NTM0ODU2Nw.G2x86i.U4d9iaNSjTC93aMEA10hHiK1k_7C-w4baw4C3A')