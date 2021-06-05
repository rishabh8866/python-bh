from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_script import Manager
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS
from flask_mail import Mail
from oauthlib.oauth2 import WebApplicationClient

import os
if not os.environ.get("DB_USER"):
    from dotenv import load_dotenv
    load_dotenv()

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


register_blueprints()
