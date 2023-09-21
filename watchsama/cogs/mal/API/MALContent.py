import MALManager

class MAL_Content():

    ''' This class acts as a means of processing the data from MALManager
        to integrate with Discord.py
    '''

    def __init__(self):
        self._webdriver = None

    @property
    def webdriver(self):
        return self._webdriver
    
    @webdriver.setter
    def webdriver(self, driver):
        self._webdriver = driver

    def create_Anime_Dict():
