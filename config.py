import os
from information import *

SECRET_KEY = os.environ.get('SECRET_KEY') or 'kamehameha'
SQLALCHEMY_DATABASE_URI = "mysql://" + DB_USER + ":" + DB_PASSWORD + "@" + DB_HOST + "/" + DB_NAME
SQLALCHEMY_TRACK_MODIFICATIONS = True
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = ""
MAIL_PASSWORD = ""
ADMINS = ['jasdeeplance@gmail.com']
DEBUG = True
