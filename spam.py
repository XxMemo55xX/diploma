import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time


driver_path = "C:/DEV/Project/diploma/webdrivers/chromedriver.exe"
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
driver_chrome = webdriver.Chrome(executable_path=driver_path)
product = "sluchawki JBL bezprzewodowe"

#====================================================================================================== script

# Allegro
driver_chrome.get("https://allegro.pl/")
time.sleep(3)

# allegro cookies

driver_chrome.find_element(by=By.XPATH, value="/html/body/div[3]/div[1]/div/div[2]/div[2]/button[1]").click()

# search
time.sleep(3)
search_allegro = driver_chrome.find_element(by=By.XPATH, value='/html/body/div[3]/div[3]/div/div/div/div/div/div[3]/header/div/div/div/div/form/input')
search_allegro.send_keys(product)
search_allegro.send_keys(Keys.RETURN)
result_table = driver_chrome.find_element(by=By.ID, value="search-results")

