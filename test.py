from selenium import webdriver
import time

driver = webdriver.Chrome()
driver.get('https://myanimelist.net/')
time.sleep(5)
driver.close()