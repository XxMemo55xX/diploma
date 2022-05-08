import os

from flask import Flask, session, redirect, url_for
from home import home

app = Flask(__name__)
app.register_blueprint(home)
app.config['SECRET_KEY'] = 'diploma_secret_key'

@app.errorhandler(404)
def page_not_found(e):
    session['message'] = ('Requested page does not exist', 'danger')
    return redirect(url_for('home.index'))
