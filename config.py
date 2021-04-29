import os
from information import *

SECRET_KEY = os.environ.get('SECRET_KEY') or 'kamehameha'
SQLALCHEMY_DATABASE_URI = "mysql://" + DB_USER + ":" + DB_PASSWORD + "@" + DB_HOST + "/" + DB_NAME
SQLALCHEMY_TRACK_MODIFICATIONS = True
MAIL_SERVER = 'smtp.zoho.eu'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = "noreply@beehaz.com"
MAIL_PASSWORD = "Beenorep45*"
ADMINS = ['noreply@beehaz.com']

MAIL_SERVER_GMAIL = 'smtp.googlemail.com'
MAIL_PORT_GMAIL = 587
MAIL_USE_TLS_GMAIL = True
MAIL_USE_SSL_GMAIL = False
MAIL_USERNAME_GMAIL = "beehaz.cloud@gmail.com"
MAIL_PASSWORD_GMAIL = "Beehaz557"
ADMINS_GMAIL = ['beehaz.cloud@gmail.com']
DEBUG = True

#oauth creds
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = ("https://accounts.google.com/.well-known/openid-configuration")
FACEBOOK_OAUTH_CLIENT_ID = os.environ.get("FACEBOOK_CLIENT_ID", None)
FACEBOOK_OAUTH_CLIENT_SECRET = os.environ.get("FACEBOOK_CLIENT_SECRET", None)
FACEBOOK_DISCOVERY_URL = "https://www.facebook.com/v10.0/dialog/oauth"
