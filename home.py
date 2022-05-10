import os

from flask import Flask, Blueprint, render_template, jsonify, request, redirect, make_response, send_file
import pandas as pd

home = Blueprint('home', __name__)


@home.route('/')
def index():
    return render_template('home.html')


def download(filepath):
    print(filepath)
    return send_file(filepath, as_attachment=True)


@home.route('/download_template')
def download_template():
    path = 'C:/DEV/Project/diploma/files/template_files/Template.xlsx'                                   #dell
    # path = 'C:/Users/wujec/Desktop/Szymek/CodeProjects/diploma/files/template_files/Template.xlsx'       #lenovo
    download(path)


@home.route('/upload_files', methods=["GET", "POST"])
def upload():

    path = 'C:/DEV/Project/diploma/files/upload'           #dell
    # path = 'C:/Users/wujec/Desktop/Szymek/CodeProjects/diploma/files/upload'       #lenovo
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

                if data_col_count == 7:
                    name = (data_tab_headers.iat[0, 0])
                    address = (data_tab_headers.iat[0, 1])
                    city = (data_tab_headers.iat[0, 2])
                    zip_code = (data_tab_headers.iat[0, 3])
                    lat = (data_tab_headers.iat[0, 4])
                    long_lat = (data_tab_headers.iat[0, 5])
                    nip = (data_tab_headers.iat[0, 6])

                    if name == "Name" and address == "Address" and city == "City" and zip_code == "Zip-code" and lat == "Lat" and long_lat == "Long Lat" and nip == "NIP":
                        for record in range(len(data_tab_value.index)):
                            name_value = (data_tab_value.iat[record, 0])
                            address_value = (data_tab_value.iat[record, 1])
                            city_value = (data_tab_value.iat[record, 2])
                            zip_code_value = (data_tab_value.iat[record, 3])
                            lat_value = (data_tab_value.iat[record, 4])
                            long_lat_value = (data_tab_value.iat[record, 5])
                            nip_value = (data_tab_value.iat[record, 6])

                            download(data_file_path)

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