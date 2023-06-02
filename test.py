import watchsama
import time

driver=watchsama.MALSelenium.MALSeleniumWrapper.get_WebDriver()
time.sleep(5)
test = watchsama.MALSelenium.MALSeleniumWrapper.get_Description(driver=driver, url='https://myanimelist.net/anime/28223/Death_Parade')

print(test)