import discord
from discord.ext import commands
import random
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from dataclasses import dataclass

#---------------------------------------------------------------------------

mal_username: str = "gabslittlepogger"
mal_password: str = 'qaz890poimnb'
intents = discord.Intents.default()
intents.message_content = True
watchsama = commands.Bot(command_prefix="!", intents=intents)

#-------------------------------------------------------------------------

@dataclass
class AnimeEntry():
    title: str
    status: str
    image: str
    def __init__(self, title, status, image):
        self.title: str =title
        self.status: str =status
        self.image: str =image

class MALSeleniumWrapper(): #This class acts as a "namespace"  
    @staticmethod
    def get_WebDriver() -> WebDriver:
        driver = webdriver.Chrome()
        return driver
    
    @staticmethod
    def account_Login(driver: WebDriver, url: str, username: str, password: str) -> None:
        driver.get(url)
        login_element: WebElement = driver.find_element(By.ID, 'loginUserName')
        password_element: WebElement = driver.find_element(By.ID, 'login-password')
        login_button: WebElement = driver.find_element(By.CLASS_NAME, "btn-recaptcha-submit")
        login_element.send_keys(username)
        password_element.send_keys(password)
        login_button.click()
        time.sleep(1)
        driver.get(f'https://myanimelist.net/animelist/{username}')

    @staticmethod
    def get_WebElements(driver: WebDriver) -> list:
        anime_list = driver.find_elements(By.CLASS_NAME, 'list-item')
        return anime_list

    @staticmethod
    def get_Title(element: WebElement) -> str:
        raw_title: WebElement = element.find_element(By.CLASS_NAME, 'title')
        title: str = raw_title.find_element(By.TAG_NAME, 'a').text
        return title
    
    @staticmethod
    def get_Status(element: WebElement) -> str:
        status_element: WebElement = element.find_element(By.CLASS_NAME, 'status')
        raw_classes: str = status_element.get_attribute('class')
        class_list: list[str] = list(raw_classes.split(" "))
        status: str = class_list[2]
        return status
    
    @staticmethod
    def get_Image(element: WebElement) -> str:
        raw_image: WebElement = element.find_element(By.CLASS_NAME, 'image')
        image: str = raw_image.find_element(By.TAG_NAME, 'img').get_attribute('src')
        return image
    
    @staticmethod
    def get_Data(driver: WebDriver) -> list[AnimeEntry]:
        m = MALSeleniumWrapper
        raw_data: WebElement = m.get_WebElements(driver)
        result: list[AnimeEntry] = [AnimeEntry(m.get_Title(element), m.get_Status(element), m.get_Image(element)) for element in raw_data]
        return result
    
    @staticmethod
    def randomizerRange(data: list[dict]) -> int:
        initial: int = 0
        final: int = len(data) - 1
        for i in range(0, len(data)):
            if data[i].status == 'plantowatch':
                initial = i 
                break
            i += 1
        result: int = random.randint(initial, final)
        return result
        

#----------------------------------------------------------------------------------------------------

#TODO: Choicing random anime feature

#Create a view to interact with embed
#synthesize embed
#Needs to have a single track reroll thats tracked with date
#Should I synthesize or make from a cached list

class WatchingView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout = 180)

def create_embed(data: AnimeEntry):
    color = discord.Color.from_str('#FFB7C5')
    description = data.status
    title= data.title
    result = discord.Embed(title=title,color=color, description=description)
    result.set_image(url=data.image)
    return result

#----------------------------------------------------------------------------------


@watchsama.event
async def on_ready():
    print('Watchsama is watching')

@watchsama.command()
async def stop(ctx: commands.Context):
    await ctx.send(f'Goodbye {ctx.author.name}!')
    await watchsama.close()
  
@watchsama.command()
#TODO: TYPE HINT THIS SHIT
async def test(ctx: commands.Context):
    url: str ='https://myanimelist.net/login.php?from=%2F&'
    wrapper = MALSeleniumWrapper
    driver: WebDriver = wrapper.get_WebDriver()
    wrapper.account_Login(driver=driver, url=url, username=mal_username, password=mal_password)
    data: list[AnimeEntry] = wrapper.get_Data(driver)
    await ctx.send(f"Successful MAL login: Check Log")
    firstwatch: int = wrapper.randomizerRange(data)
    await ctx.send(f"Watching: {firstwatch}")
    print(data)
    driver.close()

@watchsama.command()
async def embed(ctx: commands.Context):
    testCase = [{'name': 'A Silent Voice', 'status': 'completed', 'image': 'https://cdn.myanimelist.net/r/192x272/images/anime/1122/96435.webp?s=f8162c1735ac8075df9ba9974c934b24'}]
    embed = create_embed(testCase[0])
    await ctx.send(embed=embed)

#TODO: ADD TO ENV VARIABLE
watchsama.run('MTEwMzM5NDU4OTQ3NTM0ODU2Nw.G2x86i.U4d9iaNSjTC93aMEA10hHiK1k_7C-w4baw4C3A')