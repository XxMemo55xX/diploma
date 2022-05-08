import os

from flask import Flask, Blueprint, render_template, jsonify, request, redirect, make_response
import pandas as pd

home = Blueprint('home', __name__)


@home.route('/')
def index():
    return render_template('home.html')


@home.route('/upload_files')
def upload():
    path = '/module/files/upload'
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

                data_tab = pd.read_excel(data_file_path, 'Data')
                reader = pd.read_excel(data_file_path, 'Data', header=None, usecols='A:G')
                data_col_count = len(reader.columns)

                if data_col_count == 7:
                    name = (data_tab.iat[0, 0])
                    address = (data_tab.iat[0, 1])
                    city = (data_tab.iat[0, 2])
                    zip_code = (data_tab.iat[0, 3])
                    lat = (data_tab.iat[0, 4])
                    long_lat = (data_tab.iat[0, 5])
                    nip = (data_tab.iat[0, 6])

                    if name == "Name" and address == "Address" and city == "City" and zip_code == "Zip-code" and lat == "Lat" and long_lat == "Long Lat" and nip == "NIP":
                        for record in range(len(data_tab.index)):
                            name_value = (data_tab.iat[record, 0])
                            address_value = (data_tab.iat[record, 1])
                            city_value = (data_tab.iat[record, 2])
                            zip_code_value = (data_tab.iat[record, 3])
                            lat_value = (data_tab.iat[record, 4])
                            long_lat_value = (data_tab.iat[record, 5])
                            nip_value = (data_tab.iat[record, 6])
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