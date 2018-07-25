from flask import render_template, redirect, request, url_for
from app import app, allowed_file, create_pandas_df
from app.forms import UploadForm
from werkzeug import secure_filename
import os

@app.route('/')
def home():
	form = UploadForm()
	return render_template('home.html', form=form)

@app.route('/process', methods=['POST'])
def process():
	form = UploadForm()

	if form.validate_on_submit():
		file = request.files['upload_file']		
		filename = secure_filename(file.filename)

		if file and allowed_file(filename):
			df = create_pandas_df(file)

			if df is None:
				form.upload_file.errors.append("Your file is missing a column 'Address' or 'address'")
				return render_template('home.html', form=form)		
			else:
				df.to_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename), encoding='utf-8', index=False)
				return redirect(url_for('home'))
		else:
			form.upload_file.errors.append("You must upload only .csv files")
			return render_template('home.html', form=form)	

	else:
		return render_template('home.html', form=form)	