import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

#-------------------------------------------------------------------------------------------------------------------------------------------
class MAL_Controller(): 

    ''' This namespace manages Selenium's WebDriver to interact with MAL '''


    @staticmethod
    def go_To_Anime_List(driver: WebDriver, username: str, status = 0) -> None:

        ''' This method will by default will access the entire anime list unless specified'''

        list_url = f'https://myanimelist.net/animelist/{username}?status={status}'
        driver.get(list_url)
        

    
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
    def get_Anime_List_WebElements(driver: WebDriver) -> list:

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
    def press_Entry_Edit_Button(element: WebElement):

        ''' This method finds and clicks on edit button of a webelement anime entry in a list'''

        button_div: WebElement =  element.find_element(By.CLASS_NAME, 'add-edit-more')
        button_a_tag: WebElement =  button_div.find_element(By.TAG_NAME, 'a')
        button_a_tag.click()

    @staticmethod
    def search_MAL(driver: WebDriver, search: str):
        driver.get(search)
        search_results = driver.find_element(By.CLASS_NAME, 'js-scrollfix-bottom-rel')
        article:WebElement = search_results.find_element(By.TAG_NAME, 'article')
        results: list[WebElement] = article.find_elements(By.CLASS_NAME, 'di-t')
    
        #May want to look at explicit/implicit waits
        return results
