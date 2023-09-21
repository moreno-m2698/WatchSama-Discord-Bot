






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
    