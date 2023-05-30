from dataclasses import dataclass
import time
import json


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import ChromeOptions
import discord


import watchsama

#-------------------------------------------------------------------------------------------------------------------------------------------

@dataclass
class AnimeEntry():
    title: str
    status: str
    image: str
    def __init__(self, title, status, image):
        self.title: str =title
        self.status: str =status
        self.image: str =image

def get_to_anime_list() -> WebDriver:
    url: str ='https://myanimelist.net/login.php?from=%2F&'
    wrapper = MALSeleniumWrapper
    driver: WebDriver = wrapper.get_WebDriver()
    wrapper.account_Login(driver=driver, url=url, username=watchsama.config.mal_user(), password=watchsama.mal_password())
    return driver

def cache_anime_embeds()-> None:
    wrapper = MALSeleniumWrapper
    driver = get_to_anime_list()
    data: list[AnimeEntry] = wrapper.get_Data(driver)
    embeds: list[discord.Embed] = list(map(create_embed, data))
    embeds_dict: list[dict] = list(map(discord.Embed.to_dict, embeds))
    plan_to_watch_range = wrapper.getRandomizerRange(data)
    json_prototype = { 
        'embeds': embeds_dict,
        'plan_to_watch_range': plan_to_watch_range           
    }
    embeds_json = json.dumps(json_prototype, indent=4)
    with open("watchsama/cogs/mal/JSON/anime_embed.json", "w") as outfile:
        outfile.write(embeds_json)
    driver.close()

def create_embed(data: AnimeEntry):
    color = discord.Colour.from_str('#FFB7C5')
    title: str = data.title
    result = discord.Embed(title=title,color=color)
    result.set_image(url=data.image)
    return result




class MALSeleniumWrapper(): #This class acts as a "namespace"  

    @staticmethod
    def get_WebDriver() -> WebDriver:
        # options = ChromeOptions()
        # options.headless=True
        # driver = webdriver.Chrome(options=options)
        driver = webdriver.Chrome()
        return driver
    
    @staticmethod
    def account_Login(driver: WebDriver, url: str, username: str, password: str) -> None: #Only call if we need to adjust something
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
    #TODO: convert to dict
    def get_Data(driver: WebDriver) -> list[AnimeEntry]:
        m = MALSeleniumWrapper
        raw_data: WebElement = m.get_WebElements(driver)
        result: list[AnimeEntry] = [AnimeEntry(m.get_Title(element), m.get_Status(element), m.get_Image(element)) for element in raw_data]
        return result
    
    @staticmethod
    def get_Entry_URL(element:WebElement) -> str:
        raw_title: WebElement = element.find_element(By.CLASS_NAME, 'title')
        a_tag:WebElement = raw_title.find_element(By.TAG_NAME, 'a')
        result: str = a_tag.get_attribute('href')
        return result
    
    @staticmethod
    def get_Media_Type(element: WebElement) -> str:
        type_class: WebElement = element.find_element(By.CLASS_NAME, 'type')
        result: str = type_class.text
        return result
    
    @staticmethod
    def get_Progress(element: WebElement) -> list: #Only use this method when calling watch on currently watching
        progress_class: WebElement = element.find_element(By.CLASS_NAME, 'progress')
        elements: list[WebElement] =  progress_class.find_elements(By.TAG_NAME, 'span')
        initial_element: WebElement = elements[0].find_element(By.TAG_NAME, 'a')
        initial: str = initial_element.text
        if initial == '-':
            initial = '0'
        final: str = elements[1].text
        initial = int(initial)
        final = int(final)
        return [initial, final]

    
    @staticmethod
    def getRandomizerRange(data: list[dict]) -> range: 
        initial: int = 0
        final: int = len(data) - 1
        for i in range(0, len(data)):
            if data[i].status == 'plantowatch':
                initial = i 
                break
            i += 1
        result: list = [initial, final]
        return result
    



    #TODO: 
    #yellow: on-hold
    #red: dropped
    #green: watching
    #order: green, blue, yellow, red, grey