import os
import time

from flask import Flask, Blueprint, render_template, jsonify, request, redirect, make_response, send_file
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from openpyxl.workbook import Workbook
from openpyxl import load_workbook

home = Blueprint('home', __name__)


@home.route('/')
def index():
    return render_template('home.html')


def download(filepath):
    print(filepath)
    return send_file(filepath, as_attachment=True)


@home.route('/download_template')
def download_template():
    path = 'C:/DEV/Project/diploma/files/template_files/Template.xlsx'
    return download(path)


@home.route('/upload_files', methods=["GET", "POST"])
def upload():

    driver_path = "C:/DEV/Project/diploma/webdrivers/chromedriver.exe"
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")

    path = 'C:/DEV/Project/diploma/files/upload'
    if request.method == "POST":
        if request.files:
            if len(os.listdir(path)) != 0:
                for filename in os.listdir(path):
                    filepath = os.path.join(path, filename)
                    os.remove(filepath)

            upload_file = request.files["excelfile"]
            upload_filename = upload_file.filename
            delay = request.form.get("delay")

            if delay == "" or delay == " ":
                delay = 0.5
            float(delay)

            if upload_filename != "":
                message = ""

                upload_file.save(os.path.join(path, upload_filename))
                data_filename = upload_filename
                data_file_path = path + "/" + data_filename

                data_tab_headers = pd.read_excel(data_file_path, 'Data', header=None)
                data_tab_value = pd.read_excel(data_file_path, 'Data')
                reader = pd.read_excel(data_file_path, 'Data', header=None, usecols='A:G')
                data_col_count = len(reader.columns)

                wb = load_workbook(filename=data_file_path)
                ws = wb['Data']

                if data_col_count == 7:
                    name = (data_tab_headers.iat[0, 0])
                    address = (data_tab_headers.iat[0, 1])
                    city = (data_tab_headers.iat[0, 2])
                    zip_code = (data_tab_headers.iat[0, 3])
                    lat = (data_tab_headers.iat[0, 4])
                    long_lat = (data_tab_headers.iat[0, 5])
                    nip = (data_tab_headers.iat[0, 6])

                    if name == "Name" and address == "Address" and city == "City" and zip_code == "Zip-code" and lat == "Lat" and long_lat == "Long Lat" and nip == "NIP":

                        ws['I1'] = "S_Name"
                        ws['J1'] = "S_Address"
                        ws['K1'] = "S_City"
                        ws['L1'] = "S_Zip-code"
                        ws['M1'] = "S_Lat"
                        ws['N1'] = "S_Long Lat"
                        ws['O1'] = "S_NIP"
                        wb.save(data_file_path)
                        driver_chrome = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
                        driver_chrome.get("https://www.google.com/maps/")

                        for record in range(len(data_tab_value.index)):
                            name_value = (data_tab_value.iat[record, 0])
                            address_value = (data_tab_value.iat[record, 1])
                            city_value = (data_tab_value.iat[record, 2])
                            zip_code_value = (data_tab_value.iat[record, 3])
                            lat_value = (data_tab_value.iat[record, 4])
                            long_lat_value = (data_tab_value.iat[record, 5])
                            nip_value = (data_tab_value.iat[record, 6])

# accept the cookies - start
                            if record == 0:
                                cookies(driver_chrome)
# accept the cookies - end

                            search = driver_chrome.find_element(by=By.NAME, value='q')

# NAME => ADDRESS
                            s_address = address_f_name(driver_chrome, search, delay, name_value)
# ZIP CODE => CITY
                            s_city = city_f_zipcode(driver_chrome, search, delay, zip_code_value)
# ADDRESS + CITY => NAME
                            s_name = name_f_address_city(driver_chrome, search, delay, address_value, city_value)
# NAME => CITY
                            s_city1 = city_f_name(driver_chrome, search, delay, name_value)
# NAME => ZIP CODE
                            s_zip_code = zipcode_f_name(driver_chrome, search, delay, name_value)
#ADDRESS => CITY
                            s_city2 = city_f_address(driver_chrome, search, delay, address_value)
#ADDRESS => ZIP CODE
                            s_zip_code1 = zipcode_f_address(driver_chrome, search, delay, address_value)

                            print("address from name: " + s_address)
                            print("city from zipcode: " + s_city)
                            print("name from address: " + s_name)
                            print("city from name: " + s_city1)
                            print("zip code from name: " + str(s_zip_code))
                            print("city from address: " + s_city2)
                            print("zip code from address: " + str(s_zip_code1))
                            print("")

                            wb.save(data_file_path)
                            message = "Success! - file will be downloaded"

                        driver_chrome.quit()
                    else:
                        message = "Please use the official version of the template file available on main page"
                else:
                    message = "Please use the official version of the template file available on main page"
            else:
                message = "please reload page and make sure to choose the data file"
        else:
            message = "please reload page and make sure to choose the data file"
    else:
        message = "upload filed!"
    return render_template('summary.html', message=message)


@home.route('/home')
def home_return():
    return render_template('home.html')

def cookies(driver_chrome):
    delay_cookie = 10
    try:
        myElem = WebDriverWait(driver_chrome, delay_cookie).until(EC.visibility_of_element_located((By.XPATH, '/html/body/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button')))
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


def page_to_load(driver_chrome, delay):
    try:
        myElem = WebDriverWait(driver_chrome, 6).until(EC.visibility_of_element_located((By.CLASS_NAME, 'S9kvJb')))

    except TimeoutException:
        print("Loading took too much time!")
    try:
        myElem = WebDriverWait(driver_chrome, 6).until(EC.visibility_of_element_located((By.CLASS_NAME, 'TIHn2')))

    except TimeoutException:
        print("Loading took too much time!")
    try:
        myElem = WebDriverWait(driver_chrome, 6).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div')))

    except TimeoutException:
        print("Loading took too much time!")
    time.sleep(float(delay))


def address_f_name(driver_chrome, search, delay, name_value):
    try:
        driver_chrome.find_element(by=By.NAME, value='q').clear()
    except Exception:
        pass

    search.send_keys(name_value)
    search.send_keys(Keys.RETURN)

    page_to_load(driver_chrome, delay)

    try:
        s_address = driver_chrome.find_element(by=By.XPATH, value='//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[7]/div[1]/button/div[1]/div[2]').text
    except NoSuchElementException:
        s_address="N/A"

    if s_address=="N/A" or s_address=="":
        try:
            s_address = driver_chrome.find_element(by=By.XPATH, value='//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[7]/div[3]/button/div[1]').text
        except NoSuchElementException:
            s_address="N/A"

    if s_address=="N/A" or s_address=="":
        try:
            s_address = driver_chrome.find_element(by=By.XPATH, value='//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[7]/div[3]/button/div[1]/div[2]/div[1]').text
        except NoSuchElementException:
            s_address="N/A"

    if s_address=="N/A" or s_address=="":
        try:
            s_address = driver_chrome.find_element(by=By.XPATH, value='//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/h2[1]/span').text
        except NoSuchElementException:
            s_address="N/A"

    if s_address=="N/A" or s_address=="":
        try:
            s_address = driver_chrome.find_element(by=By.XPATH, value='//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/h2[1]').text
        except NoSuchElementException:
            s_address="N/A"

    if s_address=="N/A" or s_address=="":
        try:
            s_address = driver_chrome.find_element(by=By.XPATH, value='//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[9]/div[1]/button/div[1]').text
        except NoSuchElementException:
            s_address="N/A"

    if s_address=="":
        s_address="N/A"
    return s_address


def city_f_zipcode(driver_chrome, search, delay, zip_code_value):
    try:
        driver_chrome.find_element(by=By.NAME, value='q').clear()
    except Exception:
        pass

    search.send_keys(zip_code_value)
    search.send_keys(Keys.RETURN)

    page_to_load(driver_chrome, delay)

    try:
        s_city = driver_chrome.find_element(by=By.XPATH, value='//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[1]/h1').text
    except NoSuchElementException:
        s_city="N/A"

    try:
        if s_city != "N/A":
            temp_city = s_city
            s_city = temp_city.split()[1]
    except Exception:
        print("too fast")

    if s_city=="":
        s_city="N/A"
    return s_city


def name_f_address_city(driver_chrome, search, delay, address_value, city_value):
    try:
        driver_chrome.find_element(by=By.NAME, value='q').clear()
    except Exception:
        pass

    search.send_keys(address_value + " " + city_value)
    search.send_keys(Keys.RETURN)

    page_to_load(driver_chrome, delay)

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
    return s_name


def city_f_name(driver_chrome, search, delay, name_value):
    try:
        driver_chrome.find_element(by=By.NAME, value='q').clear()
    except Exception:
        pass
    exception_check = 0

    search.send_keys(name_value)
    search.send_keys(Keys.RETURN)

    page_to_load(driver_chrome, delay)

    try:
        s_city = driver_chrome.find_element(by=By.XPATH, value='//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/h2[2]/span').text
        exception_check = 1
    except NoSuchElementException:
        s_city="N/A"

    if s_city=="N/A" or s_city=="":
        try:
            s_city = driver_chrome.find_element(by=By.XPATH, value='//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[7]/div[2]/button/div[1]/div[2]/div[1]').text
        except NoSuchElementException:
            s_city="N/A"

    if s_city=="N/A" or s_city=="":
        try:
            s_city = driver_chrome.find_element(by=By.XPATH, value='//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[11]/div[3]/button/div[1]/div[2]/div[1]').text
        except NoSuchElementException:
            s_city="N/A"

    if s_city=="N/A" or s_city=="":
        try:
            s_city = driver_chrome.find_element(by=By.XPATH, value='//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[7]/div[3]/button/div[1]/div[2]/div[1]').text
        except NoSuchElementException:
            s_city="N/A"

    if s_city=="N/A" or s_city=="":
        try:
            s_city = driver_chrome.find_element(by=By.XPATH, value='//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[17]/div[3]/button/div[1]/div[2]/div[1]').text
        except NoSuchElementException:
            s_city="N/A"

    if s_city=="N/A" or s_city=="":
        try:
            s_city = driver_chrome.find_element(by=By.XPATH, value='//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[9]/div[2]/button/div[1]/div[2]/div[1]').text
        except NoSuchElementException:
            s_city="N/A"

    if s_city=="N/A" or s_city=="":
        try:
            s_city = driver_chrome.find_element(by=By.XPATH, value='//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[15]/div[3]/button/div[1]/div[2]/div[1]').text
        except NoSuchElementException:
            s_city="N/A"
    try:
        if s_city!="N/A" or s_city!="":
            temp_city = s_city
            if exception_check == 0:
                temp_city = temp_city.split(sep=",")[1]
            s_city = temp_city.split()[1]
    except Exception:
        s_city="N/A"

    if s_city=="":
        s_city="N/A"
    return s_city


def zipcode_f_name(driver_chrome, search, delay, name_value):
    try:
        driver_chrome.find_element(by=By.NAME, value='q').clear()
    except Exception:
        pass
    exception_check = 0

    search.send_keys(name_value)
    search.send_keys(Keys.RETURN)

    page_to_load(driver_chrome, delay)

    try:
        s_zip_code = driver_chrome.find_element(by=By.XPATH, value='//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/h2[2]/span').text
        exception_check = 1
    except NoSuchElementException:
        s_zip_code="N/A"

    if s_zip_code=="N/A" or s_zip_code=="":
        try:
            s_zip_code = driver_chrome.find_element(by=By.XPATH, value='//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[7]/div[2]/button/div[1]/div[2]/div[1]').text
        except NoSuchElementException:
            s_zip_code="N/A"

    if s_zip_code=="N/A" or s_zip_code=="":
        try:
            s_zip_code = driver_chrome.find_element(by=By.XPATH, value='//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[11]/div[3]/button/div[1]/div[2]/div[1]').text
        except NoSuchElementException:
            s_zip_code="N/A"

    if s_zip_code=="N/A" or s_zip_code=="":
        try:
            s_zip_code = driver_chrome.find_element(by=By.XPATH, value='//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[7]/div[3]/button/div[1]/div[2]/div[1]').text
        except NoSuchElementException:
            s_zip_code="N/A"

    if s_zip_code=="N/A" or s_zip_code=="":
        try:
            s_zip_code = driver_chrome.find_element(by=By.XPATH, value='//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[17]/div[3]/button/div[1]/div[2]/div[1]').text
        except NoSuchElementException:
            s_zip_code="N/A"

    if s_zip_code=="N/A" or s_zip_code=="":
        try:
            s_zip_code = driver_chrome.find_element(by=By.XPATH, value='//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[9]/div[2]/button/div[1]/div[2]/div[1]').text
        except NoSuchElementException:
            s_zip_code="N/A"

    if s_zip_code=="N/A" or s_zip_code=="":
        try:
            s_zip_code = driver_chrome.find_element(by=By.XPATH, value='//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[15]/div[3]/button/div[1]/div[2]/div[1]').text
        except NoSuchElementException:
            s_zip_code="N/A"
    try:
        if s_zip_code!="N/A" or s_zip_code!="":
            temp_zip_code = s_zip_code
            if exception_check == 0:
                temp_zip_code = temp_zip_code.split(sep=",")[1]
            s_zip_code1 = temp_zip_code.split()[0]
            s_zip_code = s_zip_code1
    except Exception:
        s_zip_code="N/A"

    if s_zip_code=="":
        s_zip_code="N/A"
    return s_zip_code


def city_f_address(driver_chrome, search, delay, address_value):
    try:
        driver_chrome.find_element(by=By.NAME, value='q').clear()
    except Exception:
        pass

    search.send_keys(address_value)
    search.send_keys(Keys.RETURN)

    page_to_load(driver_chrome, delay)

    try:
        s_city = driver_chrome.find_element(by=By.XPATH, value='//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div/div[2]/div[2]/div[1]/div/div/div/div[4]/div').text
    except NoSuchElementException:
        s_city="N/A"

    if s_city=="N/A" or s_city=="" or s_city.upper() == address_value.upper():
        try:
            s_city = driver_chrome.find_element(by=By.XPATH, value='//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/h2/span').text
        except NoSuchElementException:
            s_city="N/A"

    if s_city=="N/A" or s_city=="" or s_city.upper() == address_value.upper():
        try:
            s_city = driver_chrome.find_element(by=By.XPATH, value='//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/h2[3]/span').text
        except NoSuchElementException:
            s_city="N/A"

    if s_city=="N/A" or s_city=="" or s_city.upper() == address_value.upper():
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

    return s_city


def zipcode_f_address(driver_chrome, search, delay, address_value):
    try:
        driver_chrome.find_element(by=By.NAME, value='q').clear()
    except Exception:
        pass

    search.send_keys(address_value)
    search.send_keys(Keys.RETURN)

    page_to_load(driver_chrome, delay)

    try:
        s_zip_code = driver_chrome.find_element(by=By.XPATH, value='//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div/div[2]/div[2]/div[1]/div/div/div/div[4]/div').text
    except NoSuchElementException:
        s_zip_code="N/A"

    if s_zip_code=="N/A" or s_zip_code=="" or s_zip_code.upper() == address_value.upper():
        try:
            s_zip_code = driver_chrome.find_element(by=By.XPATH, value='//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/h2/span').text
        except NoSuchElementException:
            s_zip_code="N/A"

    if s_zip_code=="N/A" or s_zip_code=="" or s_zip_code.upper() == address_value.upper():
        try:
            s_zip_code = driver_chrome.find_element(by=By.XPATH, value='//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/h2[3]/span').text
        except NoSuchElementException:
            s_zip_code="N/A"

    if s_zip_code=="N/A" or s_zip_code=="" or s_zip_code.upper() == address_value.upper():
        try:
            s_zip_code = driver_chrome.find_element(by=By.XPATH, value='//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/h2[2]/span').text
        except NoSuchElementException:
            s_zip_code="N/A"

    try:
        if s_zip_code!="N/A" or s_zip_code!="" or s_zip_code.upper() != address_value.upper():
            temp_zip_code = s_zip_code
            s_zip_code = temp_zip_code.split()[0]
    except Exception:
        s_zip_code="N/A"

    if s_zip_code == "" or s_zip_code.upper() == address_value.upper():
        s_zip_code="N/A"

    return s_zip_code
