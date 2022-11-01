from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


SECRET_KEY = environ.get('SECRET_KEY')

DATABASE='dfraudr/dfraudr.sqlite'

UPLOAD_LOCATION='instance/uploads'

    
