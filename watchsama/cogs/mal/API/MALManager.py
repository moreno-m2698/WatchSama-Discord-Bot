from dataclasses import dataclass
import time
import json


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import Select

import watchsama

#-------------------------------------------------------------------------------------------------------------------------------------------



class MAL_Manager():
    
    @staticmethod
    def create_WebDriver(isTesting = False) -> WebDriver:

        """This method creates a Chrome WebDriver which will be used to navigate around MAL

        Parameters:
        -------------
        isTesting:
            boolean is used in testing to bring up a phyical browser to observer the order of operations

        Return:
        -------------
        :class: WebDriver
            Returns a basic Chrome WebDriver
        
        """

        if not isTesting:
            options = ChromeOptions()
            options.headless=True
            driver = webdriver.Chrome(options=options)
        else:
            driver = webdriver.Chrome()
        return driver
    
    @staticmethod
    def get_MAL_Anime_List(username: str, driver: WebDriver, status: int) -> WebDriver:

        '''This method redirects us to called user's list.

            Note: This does not log a user in for updates.
        
        Parameters:

        username :class: `str`
            The name of the user whos account we are observing.
        driver :class: `WebDriver`
            The preexisting webdriver which we are using to navigate mal.
        status :class: `int`
            An interger that correlates with one of MAL's list query params.
        
        Return: 
        
        driver :class: `WebDriver`
            This is the inputted driver after redirecting it to the desired URI

        '''

        single_list_url = f'https://myanimelist.net/animelist/{username}?status={status}'
        driver.get(single_list_url)
        return driver

    





def write_to_anime_list() -> WebDriver: #Returns a driver with write capability

    url: str ='https://myanimelist.net/login.php?from=%2F&'
    wrapper = MALSeleniumWrapper
    driver: WebDriver = wrapper.get_WebDriver()
    app_config = watchsama.config.App_Config
    wrapper.account_Login(driver=driver, url=url, username=app_config.mal_user(), password=app_config.mal_password())
    return driver

def get_to_anime_list(driver:WebDriver, status:int): #returns a driver with read-only capability
    wrapper=MALSeleniumWrapper
    app_config = watchsama.config.App_Config
    wrapper.get_MAL_Anime_List(username=app_config.mal_user(), driver=driver, status=status)


#TODO: MAKE THIS INTO A STATIC METHOD THAT PASSES IN A DRIVER
#ALTERNATIVLY TRY AND MAKE THIS NONBLOCKING
def cache_anime_meta(key: str) -> None:
    app_config = watchsama.config.App_Config
    
    #TODO break up the json
    username=app_config.mal_user()
    wrapper = MALSeleniumWrapper
    driver: WebDriver = wrapper.get_WebDriver()

    json_status_map = {
        '1': 'watchsama/cogs/mal/JSON/anime_watching_data.json',
        '2': 'watchsama/cogs/mal/JSON/anime_complete_data.json',
        '3': 'watchsama/cogs/mal/JSON/anime_hold_data.json',
        '4': 'watchsama/cogs/mal/JSON/anime_dropped_data.json',
        '6': 'watchsama/cogs/mal/JSON/anime_planned_data.json'
        }
    
   
    if key == '1':
        get_to_anime_list(driver=driver, status=key)
        data_dict = wrapper.get_Extended_Data(username=username, driver=driver)
    else:
        get_to_anime_list(driver=driver, status=key)
        data_dict = wrapper.get_Data(username=username,driver=driver)
    
    embeds_json = json.dumps(data_dict, indent=4)
    with open(json_status_map[key], "w") as outfile:
        outfile.write(embeds_json)

    driver.close()

class MALSeleniumWrapper():  

    @staticmethod
    def get_WebDriver(isTesting = False) -> WebDriver:
        if not isTesting:
            options = ChromeOptions()
            options.headless=True
            driver = webdriver.Chrome(options=options)
        else:
            driver = webdriver.Chrome()
        return driver
    
    @staticmethod
    #TODO: Take in int so that we can perform this based on watchtype

    def get_MAL_Anime_List(username: str, driver: WebDriver, status: int) -> WebDriver:
        driver.get(f'https://myanimelist.net/animelist/{username}?status={status}')
        return driver
    
    @staticmethod
    def account_Login(driver: WebDriver, username: str, password: str) -> None: #Only call if we need to adjust something
        driver.get('https://myanimelist.net/login.php?from=%2F&')
        login_element: WebElement = driver.find_element(By.ID, 'loginUserName')
        password_element: WebElement = driver.find_element(By.ID, 'login-password')
        login_button: WebElement = driver.find_element(By.CLASS_NAME, "btn-recaptcha-submit")
        login_element.send_keys(username)
        password_element.send_keys(password)
        login_button.click()
        time.sleep(1)

    #===============================================================================

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
        initial_text: WebElement = elements[0].find_element(By.TAG_NAME, 'a').text
        initial: str = '0' if initial_text == '-' else initial_text
        final: str = elements[1].text
        result = [initial, final]
        result = list(map(int,result))
        return result
    
    @staticmethod
    def press_Edit_Button(element: WebElement):
        button_div: WebElement =  element.find_element(By.CLASS_NAME, 'add-edit-more')
        button_a_tag: WebElement =  button_div.find_element(By.TAG_NAME, 'a')
        button_a_tag.click()
    
    @staticmethod
    def get_Data(driver:WebDriver, username: str) -> list[dict]:
        m = MALSeleniumWrapper
        raw_data: WebElement = m.get_WebElements(driver)
        result: list[dict] = [m.create_Base_Entry_Dict(username, element) for element in raw_data]
        return result
    
    @staticmethod
    def get_Extended_Data(driver:WebDriver, username: str) -> list[dict]:
        m = MALSeleniumWrapper
        raw_data: WebElement = m.get_WebElements(driver)
        result: list[dict] = [m.create_Currently_Watching_Dict(username, element) for element in raw_data]
        return result
    
    @staticmethod
    def edit_Anime_Status(driver: WebDriver, embed_index: int, status: int) -> None:
        m = MALSeleniumWrapper
        raw_data: list[WebElement] = m.get_WebElements(driver)
        element: WebElement = raw_data[embed_index]
        m.press_Edit_Button(element)
        driver.switch_to.frame(driver.find_element(By.ID, "fancybox-frame"))
        status_select  = Select(driver.find_element(By.NAME, 'add_anime[status]'))
        status_select.select_by_index(status)
        driver.find_element(By.CLASS_NAME, 'main_submit')

        print('button located')
        #TODO: press button later
        time.sleep(5)

    @staticmethod 
    def create_Base_Entry_Dict(element: WebElement) -> dict:
        m = MALSeleniumWrapper
        result = {
            'name': m.get_Title(element),
            "reference": m.get_Entry_URL(element),
            'status': m.get_Status(element),
            "image": m.get_Image(element),
            "type": m.get_Media_Type(element)
        }
        return result
    
    @staticmethod 
    def create_Currently_Watching_Dict(username: str, element: WebElement) -> dict:
        m=MALSeleniumWrapper
        result = m.create_Base_Entry_Dict(username, element)
        result['progress'] = m.get_Progress(element)
        return result
    