
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import Select

import watchsama

#-------------------------------------------------------------------------------------------------------------------------------------------



class MAL_Controller():

    ''' This namespace manages Selenium's WebDriver to interact with MAL '''
    
    @staticmethod
    def create_WebDriver(isTesting = False) -> WebDriver:

        """This method creates a Chrome WebDriver which will be used to navigate around MAL

        Parameters:
        -------------
        isTesting:

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
        print(f"WebDriver: {driver} has been created.")
        return driver
    
    @staticmethod
    def close_WebDriver(driver: WebDriver) -> None:
        ''' This method closes the webdriver'''
        
        driver.close()
        print(f"WebDriver: {driver} has been successfully closed")
        
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
    
    @staticmethod
    def selenium_Account_Login(driver: WebDriver, username: str, password: str) -> None:
        
        ''' This method will log the user stored in .env to enable the WebDriver to update any account information and be 
            redirected to MAL's main page

            Note: This should be used sparingly and that the user should then be logged out once all information is up to date.

        Parameters:

        driver :class: `WebDriver`
            A preexisting webdriver which we are using to navigate MAL.
        username :class: `str`
        password :class: `str`

        '''

        login_url = 'https://myanimelist.net/login.php?from=%2F&'
        driver.get(login_url)
        login_element: WebElement = driver.find_element(By.ID, 'loginUserName')
        password_element: WebElement = driver.find_element(By.ID, 'login-password')
        login_button: WebElement = driver.find_element(By.CLASS_NAME, "btn-recaptcha-submit")
        login_element.send_keys(username)
        password_element.send_keys(password)
        login_button.click()
        time.sleep(1) #This wait may not be necessary but it allows the webpage to load up all its assets

    
    @staticmethod
    def get_List_WebElements(driver: WebDriver) -> list:

        ''' This method returns a list of Selenium WebElements for the list items in an anime list
            
            Note: This method can only be used if the WebDriver is on a profile animelist URI

        Parameters:

            driver :class: `WebDriver`
                A preexisting webdriver which is observing a URL of the form `myanimelist.net/animelist/{profile}`
        
        Return:
        
            anime_Web_Elements :class: list[`WebElement`]
                A list of WebElements that correspond to differnt MAL entries
    
            
        '''
        anime_Web_Elements = driver.find_elements(By.CLASS_NAME, 'list-item')
        return anime_Web_Elements
    
    @staticmethod
    def get_Item_Title(element: WebElement) -> str:

        ''' This method retrieves the title from a WebElement'''

        raw_title: WebElement = element.find_element(By.CLASS_NAME, 'title')
        title_a_tag: WebElement = raw_title.find_element(By.TAG_NAME, 'a')
        title: str = title_a_tag.text
        return title

    @staticmethod
    def get_Item_Status(element: WebElement) -> str:

        ''' This method retrieves the current watch status of an entry'''

        status_element: WebElement = element.find_element(By.CLASS_NAME, 'status')
        raw_classes: str = status_element.get_attribute('class')
        class_list: list[str] = list(raw_classes.split(" "))
        status: str = class_list[2]
        return status

    @staticmethod
    def get_Image(element: WebElement) -> str:

        ''' This method retrieves the image source of an entry'''

        raw_image: WebElement = element.find_element(By.CLASS_NAME, 'image')
        element_img_tag: WebElement = raw_image.find_element(By.TAG_NAME, 'img')
        image_src: str = element_img_tag.get_attribute('src')
        return image_src
    
    @staticmethod
    def get_Entry_URL(element:WebElement) -> str:

        ''' Returns the url for an entry that can be used to process more information for the bot'''

        raw_title: WebElement = element.find_element(By.CLASS_NAME, 'title')
        a_tag:WebElement = raw_title.find_element(By.TAG_NAME, 'a')
        result: str = a_tag.get_attribute('href')
        return result

    @staticmethod
    def get_Media_Type(element: WebElement) -> str:

        ''' Gets the media type of an entry such as `Movie` or `TV` '''

        type_class: WebElement = element.find_element(By.CLASS_NAME, 'type')
        result: str = type_class.text
        return result

    @staticmethod
    def get_Watch_Progress(element: WebElement) -> list:

        ''' This method will return the current watch progress of a show.
        
            Note: This can only be called on a show in Currently Watching
            
        Return
            result :class: list[`int`]
                The result is the start and stop index of show after being converted to int
        '''

        progress_class: WebElement = element.find_element(By.CLASS_NAME, 'progress')
        elements: list[WebElement] =  progress_class.find_elements(By.TAG_NAME, 'span')
        initial_text: WebElement = elements[0].find_element(By.TAG_NAME, 'a').text
        initial: str = '0' if initial_text == '-' else initial_text
        final: str = elements[1].text
        result = [initial, final]
        result = list(map(int,result))
        return result
    
    @staticmethod
    def get_Description(driver: WebDriver, entry_url: str) -> str: #This uses the webdriver to connect and get the url

        ''' This method navigates a webdriver to the url an anime entries information page and returns its description'''
        
        driver.get(entry_url)
        table_element: WebElement = driver.find_element(By.TAG_NAME, 'table')
        p_tag: WebElement = table_element.find_element(By.TAG_NAME, 'p')
        result = p_tag.text
        return result

    @staticmethod
    def press_Entry_Edit_Button(element: WebElement):

        ''' This method finds and clicks on edit button of a webelement anime entry in a list'''

        button_div: WebElement =  element.find_element(By.CLASS_NAME, 'add-edit-more')
        button_a_tag: WebElement =  button_div.find_element(By.TAG_NAME, 'a')
        button_a_tag.click()

