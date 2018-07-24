from flask import render_template
from app import app
from app.forms import UploadForm


@app.route('/')
def home():
	form = UploadForm()
	return render_template('home.html', form=form)