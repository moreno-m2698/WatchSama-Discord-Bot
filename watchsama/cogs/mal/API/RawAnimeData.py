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
        
        s = SeleniumRawData
        ctrlr = MAL_Controller

        driver = webdriver.Chrome()
        print("A WebDriver has been initiated")

        ctrlr.go_To_Anime_List(driver = driver, username = username, status=status)
        anime_list_web_elements: list[WebDriver] = ctrlr.get_Anime_List_WebElements(driver = driver)
        result = []

        for element in anime_list_web_elements:
            title = s._get_Title(element)
            url_reference = s._get_Entry_URL(element)
            status = s._get_Status(element)
            image_src = s._get_Image_Src(element)
            media = s._get_Media(element)
            anime_dict = {
                "name": title,
                "reference": url_reference,
                "status": status,
                "image": image_src,
                "type": media
            }
            result.append(anime_dict)

        driver.close()
        print("WebDriver is now closed")
        
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
    
    
    def _get_Entry_URL(element:WebElement) -> str:

        ''' Returns the url for an entry that can be used to process more information for the bot'''

        raw_title: WebElement = element.find_element(By.CLASS_NAME, 'title')
        a_tag:WebElement = raw_title.find_element(By.TAG_NAME, 'a')
        url: str = a_tag.get_attribute('href')
        return url
    
    def _get_Media(element: WebElement) -> str:

        ''' Gets the media type of an entry such as `Movie` or `TV` '''

        type_class: WebElement = element.find_element(By.CLASS_NAME, 'type')
        media: str = type_class.text
        return media
    