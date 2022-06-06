import os
import time

from flask import Flask, Blueprint, render_template, jsonify, request, redirect, make_response, send_file
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
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
                        driver_chrome = webdriver.Chrome(executable_path=driver_path)

                        for record in range(len(data_tab_value.index)):
                            name_value = (data_tab_value.iat[record, 0])
                            address_value = (data_tab_value.iat[record, 1])
                            city_value = (data_tab_value.iat[record, 2])
                            zip_code_value = (data_tab_value.iat[record, 3])
                            lat_value = (data_tab_value.iat[record, 4])
                            long_lat_value = (data_tab_value.iat[record, 5])
                            nip_value = (data_tab_value.iat[record, 6])

                            driver_chrome.get("https://www.google.com/maps/")

# accept the cookies - start
                            if record == 0:
                                time.sleep(2)
                                try:
                                    driver_chrome.find_element(by=By.XPATH, value="/html/body/div[2]/div[2]/div[3]/span/div/div/div/div[3]/button[2]/div").click()
                                except Exception:
                                    pass
# accept the cookies - end

                            search = driver_chrome.find_element(by=By.NAME, value='q')

# NAME

                            search.send_keys(name_value)
                            search.send_keys(Keys.RETURN)
                            try:
                                s_address = driver_chrome.find_element(by=By.XPATH, value='//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/h2[1]/span').text
                            except NoSuchElementException:
                                s_address="No address could be found"

# ZIP CODE
                            driver_chrome.get("https://www.google.pl/")
                            search.send_keys(zip_code_value)
                            search.send_keys(Keys.RETURN)
                            data_table = driver_chrome.find_element(by=By.XPATH, value="/html/body/div[7]/div/div[10]/div[2]/div/div/div[2]/div/div[4]/div/div/div/div/div[1]/div/div/div/div/div/div[1]/div/div/div/span[2]")
                            temp_city = [td.text for td in data_table.find_elements(by=By.CLASS_NAME, value='fl')]
                            s_city = temp_city[0]

                            print("address: " + s_address)
                            print("city: " + s_city)

                            wb.save(data_file_path)
                            message = "Success! - file will be downloaded"
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