from flask import Flask, make_response, redirect, g, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_script import Manager
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS
from flask_mail import Mail
from oauthlib.oauth2 import WebApplicationClient
import flask_admin as admin
from flask_admin import BaseView
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, expose
from logging.config import dictConfig
from slack_sdk import WebClient
import os

if not os.environ.get("DB_USER"):
    from dotenv import load_dotenv
    load_dotenv()

debug = os.getenv("FLASK_DEBUG", 'False').lower() in ('true', '1', 't')

dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
        },
        "access": {
            "format": "%(message)s",
        }
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
        # "slack": {
        #     "class": "app.HTTPSlackHandler",
        #     "formatter": "default",
        #     "level": "ERROR",
        # },
        "error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default",
            "filename": "/var/log/gunicorn.error.log",
            "maxBytes": 10000,
            "backupCount": 10,
            "delay": "True",
        },
        "access_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "access",
            "filename": "/var/log/gunicorn.access.log",
            "maxBytes": 10000,
            "backupCount": 10,
            "delay": "True",
        }
    },
    "loggers": {
        "gunicorn.error": {
            # "handlers": ["console"] if debug else ["console", "slack", "error_file"],
            "handlers": ["console"] if debug else ["console", "error_file"],
            "level": "INFO",
            "propagate": False,
        },
        "gunicorn.access": {
            "handlers": ["console"] if debug else ["console", "access_file"],
            "level": "INFO",
            "propagate": False,
        }
    },
    "root": {
        "level": "DEBUG" if debug else "INFO",
        # "handlers": ["console"] if debug else ["console", "slack"],
        "handlers": ["console"] if debug else ["console"],
    }
})

app = Flask(__name__)
manager = Manager(app)
CORS(app)
app.config.from_object("config.config")
db = SQLAlchemy(app)
migrate = Migrate(app, db)
auth = HTTPBasicAuth()
mail = Mail(app)
oauth_vars = {
    "client_id": app.config["GOOGLE_CLIENT_ID"],
    "discovery_url": app.config["GOOGLE_DISCOVERY_URL"],
    "client_secret": app.config["GOOGLE_CLIENT_SECRET"],
    "social_id": app.config["FACEBOOK_OAUTH_CLIENT_ID"],
    "social_secret": app.config["FACEBOOK_OAUTH_CLIENT_SECRET"],
    "social_url": app.config["FACEBOOK_DISCOVERY_URL"]
}
oauth_google_client = WebApplicationClient(oauth_vars["client_id"])

import stripe
stripe.api_key = app.config["STRIPE_KEY"]


slack_client = WebClient(token = app.config["SLACK_TOKEN"])



def register_blueprints():
    from app.customer import customer
    from app.rental import rental
    from app.group import group
    from app.booking import booking
    from app.guest import guest
    from app.rate import rate
    from app.fee import fee
    from app.calander import calander
    from app.subscribers import subscribers
    from app.invoice import invoice
    from app.payment import payment_blueprint

    # from app.tax import tax
    from app.inquiry import inquiry
    app.register_blueprint(customer, url_prefix = "/api/customer")
    app.register_blueprint(rental, url_prefix = "/api/rental")
    app.register_blueprint(group, url_prefix = "/api/group")
    app.register_blueprint(booking, url_prefix = "/api/booking")
    app.register_blueprint(guest, url_prefix = "/api/guest")
    app.register_blueprint(rate, url_prefix = "/api/rate")
    app.register_blueprint(fee, url_prefix = "/api/fee")
    # app.register_blueprint(tax, url_prefix = "/api/tax")
    app.register_blueprint(inquiry, url_prefix = "/api/inquiry")
    app.register_blueprint(calander, url_prefix = "/api/calander")
    app.register_blueprint(subscribers, url_prefix = "/api/subscribers")
    # app.register_blueprint(invoice,url_prefix = "/api/invoice")
    app.register_blueprint(payment_blueprint, url_prefix= "/api/payment")



class MyAdminView(admin.AdminIndexView):
    """Handle admin login"""
    @expose('/', methods=['POST', 'GET'])
    def index(self):
        print("Jasdeep here")
        if request.cookies.get('ok') == 'man':
            return super(MyAdminView, self).index()

        if (request.form
            and request.form.get('username') == 'admin'
            and request.form.get('password') == 'admin_password'):
            g.ok = True

            response = make_response(super(MyAdminView, self).index())
            response.set_cookie('ok', 'man')
            return response

        return """
        <form method="POST">
        <input type="text" name="username">
        <input type="password" name="password">
        <input type="submit" value="Login">
        </form>
        """
from app.customer.model import Customer
admin = Admin(app, name='beehaz', template_mode='bootstrap3', index_view=MyAdminView())
admin.add_view(ModelView(Customer, db.session))
register_blueprints()