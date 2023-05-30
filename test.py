from watchsama.cogs.mal.API.MALSeleniumWrapper import MALSeleniumWrapper

def test():
    wrapper= MALSeleniumWrapper
    driver=wrapper.get_WebDriver()
    driver.get('https://myanimelist.net/animelist/gabslittlepogger?status=4')
    anime_list = wrapper.get_WebElements(driver)
    result = list(map(wrapper.get_Progress,anime_list))

    print(result)
    print(len(result))
test()