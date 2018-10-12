from flask import render_template,url_for,redirect,session
from . import main
from .form import nameForm

@main.route('/',methods=['GET','POST'])
def index():
	return render_template('index.html')


