from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired, Email

class UploadForm(FlaskForm):
	upload_file = FileField('File', validators=[DataRequired()])
	submit = SubmitField('Submit')