from abc import ABC, abstractmethod

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import Select



class RawAnimeData(ABC):
    
    @abstractmethod
    def create_Anime_List() -> list[dict]:
        ''' This will be the only method which return the anime data as a list of dicts'''
        pass


class SeleniumRawData(RawAnimeData): 
    def create_Anime_List() -> list[dict]:
        pass