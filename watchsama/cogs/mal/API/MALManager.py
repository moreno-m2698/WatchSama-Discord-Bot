# from MALController import MAL_Controller

class MAL_Manager():

    ''' This class acts as a means of processing the data from MALManager
        to integrate with Discord.py
    '''

    #TODO: Create singleton for webdriver
    def __init__(self, webdriver):
        self._webdriver = webdriver
    @property
    def webdriver(self):
        return self._webdriver
    
    @webdriver.setter
    def webdriver(self, driver):
        self._webdriver = driver

    # def create_Anime_WebElement_List(self, *args):

    #     ''' This method will create a list of webElements for further processing'''

    #     if self._webdriver == None:
    #         raise TypeError("WebDriver was not initialized")

    #     ctrlr = MAL_Controller
    #     result = ctrlr.get_List_WebElements()

    def create_Anime_Dict(self, web_element):

        ''' This method will create a dict for a single anime entry'''

        if self._webdriver == None:
            raise TypeError("WebDriver was not initialized")
        
        result = {
            'name': '',
            'url_ref': '',
            'status': '',
            'image_src': '',
            'media_type': ''
        }

