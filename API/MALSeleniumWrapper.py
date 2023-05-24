from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from dataclasses import dataclass
import time

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
    def getRandomizerRange(data: list[dict]) -> int: 
        initial: int = 0
        final: int = len(data) - 1
        for i in range(0, len(data)):
            if data[i].status == 'plantowatch':
                initial = i 
                break
            i += 1
        result: range = range(initial, final)
        return result