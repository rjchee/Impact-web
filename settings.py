import os

def _getbool(var_name):
    return os.getenv(var_name, '').lower() in ['true', '1', 'yes']

PORT = int(os.getenv('PORT', 5000))
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
SQLALCHEMY_TRACK_MODIFICATIONS=False

DEBUG = _getbool('DEBUG')
APP_SECRET = os.getenv('APP_SECRET')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
