import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time



driver_path = "C:/DEV/Project/diploma/webdrivers/chromedriver.exe"
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
driver_chrome = webdriver.Chrome(executable_path=driver_path)
city_value = "Lublin"
name_value = "warsaw spire"
address_value = "Marii Curie-Skłodowskiej 5"
zip_code_value = "00-630"
driver_chrome.get("https://www.google.com/maps/")

# accept the cookies - start
time.sleep(2)
try:
    driver_chrome.find_element(by=By.XPATH, value="/html/body/div[2]/div[2]/div[3]/span/div/div/div/div[3]/button[2]/div").click()
except Exception:
    pass
try:
    driver_chrome.find_element(by=By.XPATH, value="/html/body/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button").click()
except Exception:
    pass
# accept the cookies - end

#====================================================================================================== script


# search
time.sleep(3)

search = driver_chrome.find_element(by=By.NAME, value='q')

# NAME_VALUE => ADDRESS_VALUE

search.send_keys(address_value)
search.send_keys(Keys.RETURN)
time.sleep(2)

try:
    s_city = driver_chrome.find_element(by=By.XPATH, value='//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div/div[2]/div[2]/div[1]/div/div/div/div[4]/div').text
except NoSuchElementException:
    s_city="N/A"

if s_city=="N/A" or s_city=="":
    try:
        s_city = driver_chrome.find_element(by=By.XPATH, value='//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/h2/span').text
    except NoSuchElementException:
        s_city="N/A"

if s_city=="N/A" or s_city=="":
    try:
        s_city = driver_chrome.find_element(by=By.XPATH, value='//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/h2[3]/span').text
    except NoSuchElementException:
        s_city="N/A"

if s_city=="N/A" or s_city=="":
    try:
        s_city = driver_chrome.find_element(by=By.XPATH, value='//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/h2[2]/span').text
    except NoSuchElementException:
        s_city="N/A"

try:
    if s_city!="N/A" or s_city!="":
        temp_city = s_city
        s_city = temp_city.split()[1]
except Exception:
    s_city="N/A"

if s_city=="":
    s_city="N/A"

print(s_city)


