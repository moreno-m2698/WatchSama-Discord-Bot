from abc import ABC, abstractmethod
import time

from watchsama.config import App_Config

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


from watchsama.cogs.mal.API.MALController import MAL_Controller

class RawAnimeData(ABC):
    
    @abstractmethod
    def create_Anime_List(driver: WebDriver, username: str, status: int) -> list[dict]:
        ''' This will be the only method which return the anime data as a list of dicts'''
        pass


class SeleniumRawData(RawAnimeData): 

    @staticmethod
    def create_Anime_List(driver: WebDriver, username=App_Config.mal_user(), status = 0) -> list[dict]:

        ''' This method creates a webDriver and then navigates it around for the data'''

        allowed_status = [0, 1, 2, 3, 4, 6]

        if status not in allowed_status:
            return []
        
        s = SeleniumRawData
        ctrlr = MAL_Controller


        ctrlr.go_To_Anime_List(driver = driver, username = App_Config.mal_user(), status=status)
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
                "media": media
            }
            result.append(anime_dict)

        
        
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
    
    @staticmethod
    def list_chunking(l:list, n:int) -> list[list]:
        #TODO: move out of this since this will be a standard
        #We could also move this into create_Anime_List
        for i in range(0, len(l), n):
            yield l[i:i+n]
    
    @staticmethod
    def get_Description(driver: WebDriver, url) ->str:
        driver.get(url)
        table_element: WebElement = driver.find_element(By.TAG_NAME, 'table')
        p_tag: WebElement = table_element.find_element(By.TAG_NAME, 'p')
        result = p_tag.text
        return result
    
    
class SeleniumSearchData(RawAnimeData):
    
    @staticmethod
    def create_Anime_List(driver:WebDriver, search: str, amount = 5) -> list[dict]:
        
        ctrlr = MAL_Controller
        search_url = f'https://myanimelist.net/search/all?cat=anime&q={search}'
        search_webElements = ctrlr.search_MAL(driver, search_url)
        time.sleep(5)
        first_results = search_webElements[0:amount]
        s = SeleniumSearchData

        result = []
        for entry in first_results:
            a_tag:WebElement = entry.find_element(By.TAG_NAME, 'a')
            url = s._get_Entry_URL(entry)
            result.append(url)

        return result
    
    def _get_Entry_URL(element:WebElement):
        a_tag: WebElement = element.find_element(By.TAG_NAME, 'a')
        url = a_tag.get_attribute('href')
        return url
    
class ExtendedSeleniumRawData(SeleniumRawData):

    @staticmethod
    def create_Anime_List(driver: WebDriver, username=App_Config.mal_user(), status=1) -> list[dict]:
       
        allowed_status = [0, 1, 2, 3, 4, 6]

        if status not in allowed_status:
            return []
        
        e = ExtendedSeleniumRawData
        ctrlr = MAL_Controller


        ctrlr.go_To_Anime_List(driver = driver, username = username, status=status)
        anime_list_web_elements: list[WebDriver] = ctrlr.get_Anime_List_WebElements(driver = driver)
        result = []

        for element in anime_list_web_elements:
            title = e._get_Title(element)
            url_reference = e._get_Entry_URL(element)
            status = e._get_Status(element)
            image_src = e._get_Image_Src(element)
            media = e._get_Media(element)
            progress = e._get_Progress(element)
            anime_dict = {
                "name": title,
                "reference": url_reference,
                "status": status,
                "image": image_src,
                "media": media,
                "progress": progress
            }
            result.append(anime_dict)

        
        
        return result 

    def _get_Progress(element: WebElement) -> list[str]:
        progress_td: WebElement = element.find_element(By.CLASS_NAME, 'progress')
        span_elements: list[WebElement] = progress_td.find_elements(By.TAG_NAME, 'span')
        progress = list(map(lambda x : x.text,span_elements))
        progress[0] = progress[0][0:1]
        
        progress[0] = '0' if progress[0] == '-' else progress[0]
        result = list(map(int,progress))
        
        return result
