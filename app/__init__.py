from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config
from geopy.geocoders import Nominatim
import pandas
import os

app = Flask(__name__)
app.config.from_object(Config)

Bootstrap(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() == 'csv'

def get_geo_data(address):
	nom = Nominatim(user_agent="geocoder-app")
	return nom.geocode(address)
	
def create_pandas_df(file):
	df = get_pandas_df(file)

	if 'Address' in df.columns:
		address_column = 'Address'
	elif 'address' in df.columns:
		address_column = 'address'
	else:	
		return None

	df['Coordinates'] = df[address_column].apply(get_geo_data)
	df['Latitude'] = df['Coordinates'].apply(lambda x: x.latitude if x != None else None)			
	df['Longitude'] = df['Coordinates'].apply(lambda x: x.longitude if x != None else None)

	return df

def get_pandas_df(file):
	return pandas.read_csv(file)	

def get_root_project_dir():
	return os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

def get_upload_path():
	return os.path.join(get_root_project_dir(), app.config['UPLOAD_FOLDER'])

from app import routes, forms