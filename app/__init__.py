from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config
from geopy.geocoders import Nominatim
import pandas

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
	df = pandas.read_csv(file)

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

from app import routes, forms