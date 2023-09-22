
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import Select



class Anime_List():
    ''' This class will brings us to a MAL Lists to process web information'''
    
    @staticmethod
    def get_MAL_Anime_List(username: str, driver: WebDriver, status: int) -> None:

        '''This method redirects us to called user's list.

            Note: This does not log a user in for updates.
        
        Parameters:

        username :class: `str`
        driver :class: `WebDriver`
            The preexisting webdriver which we are using to navigate MAL.
        status :class: `int`
            An interger that correlates with one of MAL's list query params.
        
        '''

        single_list_url = f'https://myanimelist.net/animelist/{username}?status={status}'
        driver.get(single_list_url)