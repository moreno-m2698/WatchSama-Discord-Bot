from abc import ABC, abstractmethod
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import Select


from watchsama.cogs.mal.API.MALController import MAL_Controller


class RawAnimeData(ABC):
    
    @abstractmethod
    def create_Anime_List() -> list[dict]:
        ''' This will be the only method which return the anime data as a list of dicts'''
        pass


class SeleniumRawData(RawAnimeData): 

    def __init__(self):
        pass

    def create_Anime_List(username='gabslittlepogger', status = 0) -> list[dict]:

        ''' This method creates a webDriver and then navigates it around for the data'''

        allowed_status = [0, 1, 2, 3, 4, 6]

        if status not in allowed_status:
            return []

        driver = webdriver.Chrome()
        print("A WebDriver has been initiated")

        ctrlr = MAL_Controller
        ctrlr.go_To_Anime_List(driver = driver, username = username)
        anime_list_web_elements: list[WebDriver] = ctrlr.get_Anime_List_WebElements(driver = driver)

        print(anime_list_web_elements[0])


        driver.close()
        print("WebDriver is now closed")

        result = []
        return result 
    
    def _get_Title(element: WebElement) -> str:
        ''' This method retrieves the title from a WebElement'''

        raw_title: WebElement = element.find_element(By.CLASS_NAME, 'title')
        title_a_tag: WebElement = raw_title.find_element(By.TAG_NAME, 'a')
        title: str = title_a_tag.text
        return title
    
    def _get_Status(element: WebElement) -> str:
    
        ''' This method retrieves the current watch status of an entry'''

        status_element: WebElement = element.find_element(By.CLASS_NAME, 'status')
        raw_classes: str = status_element.get_attribute('class')
        class_list: list[str] = list(raw_classes.split(" "))
        status: str = class_list[2]
        return status
    
    def _get_Image_Src(element: WebElement) -> str:
        
        ''' This method retrieves the image source of an entry'''

        raw_image: WebElement = element.find_element(By.CLASS_NAME, 'image')
        element_img_tag: WebElement = raw_image.find_element(By.TAG_NAME, 'img')
        image_src: str = element_img_tag.get_attribute('src')
        return image_src