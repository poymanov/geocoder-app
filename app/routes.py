from flask import render_template, redirect, request, url_for, send_file
from app import app, allowed_file, create_pandas_df, get_pandas_df, get_upload_path
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

				upload_directory = get_upload_path()
				if not os.path.exists(upload_directory):
					os.makedirs(upload_directory)

				df.to_csv(os.path.join(upload_directory, filename), encoding='utf-8', index=False)
				return redirect(url_for('result', filename=filename))
		else:
			form.upload_file.errors.append("You must upload only .csv files")
			return render_template('home.html', form=form)	

	else:
		return render_template('home.html', form=form)	

@app.route('/result/<filename>')
def result(filename):
	path = os.path.join(get_upload_path(), filename)

	df = get_pandas_df(path)
	return render_template('result.html', df=df, filename=filename, path=path)

@app.route("/download/<filename>")
def download(filename):
	upload_path = get_upload_path()
	path = os.path.join(upload_path, filename)

	new_filename = "modified_%s.csv" % filename
	return send_file(path, attachment_filename=new_filename, as_attachment=True)	