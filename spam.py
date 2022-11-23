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
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time



driver_path = "C:/DEV/Project/diploma/webdrivers/chromedriver.exe"
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
driver_chrome = webdriver.Chrome(executable_path=driver_path)
city_value = "warsaw"
name_value = "warsaw spire"
address_value = "Koszykowa 86"
zip_code_value = "00-630"
driver_chrome.get("https://www.google.com/maps/")

# accept the cookies - start
time.sleep(2)
try:
    myElem = WebDriverWait(driver_chrome, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button')))
    time.sleep(1)
except TimeoutException:
    print("Loading took too much time!")
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

search = driver_chrome.find_element(by=By.NAME, value='q')

# ADDRESS_VALUE => LAT_VALUE + LONG_LAT_VALUE
try:
    time.sleep(3)
    search.clear()
except Exception:
    pass
search.send_keys(address_value + " " + city_value)
search.send_keys(Keys.RETURN)
driver_chrome.find_element(by=By.XPATH, value="/html/body/div[1]/div[2]/div[3]/div[1]/form[1]/div[2]/div/button").click()
time.sleep(2)

try:
    s_name = driver_chrome.find_element(by=By.CLASS_NAME, value="bfdHYd Ppzolf")
    s_name = s_name.get_attribute("aria-label")
except NoSuchElementException:
    s_name="N/A"

if s_name=="N/A" or s_name.upper()==address_value.upper():
    try:
        s_name = driver_chrome.find_element(by=By.XPATH, value='//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[15]/div/div[2]/div[2]/div[1]/div/div/div/div[1]/div/span').text
    except NoSuchElementException:
        s_name="N/A"

if s_name=="N/A" or s_name.upper()==address_value.upper():
    try:
        s_name = driver_chrome.find_element(by=By.XPATH, value='//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[17]/div/div[2]/div[2]/div[1]/div/div/div/div[1]').text
    except NoSuchElementException:
        s_name="N/A"

if s_name=="N/A" or s_name.upper()==address_value.upper():
    try:
        s_name = driver_chrome.find_element(by=By.XPATH, value='//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[17]/div/div[2]/div[2]/div[1]/div/div/div/div[1]').text
    except NoSuchElementException:
        s_name="N/A"

if s_name=="N/A" or s_name.upper()==address_value.upper():
    try:
        s_name = driver_chrome.find_element(by=By.XPATH, value='//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[19]/div/div[2]/div[2]/div[1]/div/div/div/div[1]/div').text
    except NoSuchElementException:
        s_name="N/A"

if s_name=="N/A" or s_name.upper()==address_value.upper():
    try:
        s_name = driver_chrome.find_element(by=By.XPATH, value='//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[15]/div/div[2]/div[2]/div[1]/div/div/div/div[1]/div').text
    except NoSuchElementException:
        s_name="N/A"

if s_name=="N/A" or s_name.upper()==address_value.upper():
    try:
        s_name = driver_chrome.find_element(by=By.XPATH, value='//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[27]/div/div[2]/div[2]/div[1]/div/div/div/div[1]/div').text
    except NoSuchElementException:
        s_name="N/A"

if s_name=="N/A" or s_name.upper()==address_value.upper():
    try:
        s_name = driver_chrome.find_element(by=By.XPATH, value='//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[18]/div/div[2]/div[2]/div[1]/div/div/div/div[1]/div').text
    except NoSuchElementException:
        s_name="N/A"

if s_name=="":
    s_name="N/A"


print(s_name)



