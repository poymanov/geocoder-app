from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired, Email
from wtforms import validators

class UploadForm(FlaskForm):
	data = FileField('File', validators=[DataRequired()])
	submit = SubmitField('Submit')