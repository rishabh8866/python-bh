from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_script import Manager
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS
from flask_mail import Mail


app = Flask(__name__)
manager = Manager(app)
CORS(app)
app.config.from_object("config")
db = SQLAlchemy(app)
migrate = Migrate(app, db)
auth = HTTPBasicAuth()
mail = Mail(app)

if app.config['MAIL_SERVER']:
    mail_auth = None
    if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
        mail_auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
    secure = None
    if app.config['MAIL_USE_TLS']:
        secure = ()
    """
    mail_handler = SMTPHandler(
        mailhost = (app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
        fromaddr = 'no-reply@' + app.config['MAIL_SERVER'],
        toaddrs = app.config['ADMINS'], subject = 'Beehaz Failure',
        credentials = auth, secure = secure)
    """

def register_blueprints():
    from app.customer import customer
    from app.rental import rental
    from app.group import group
    from app.booking import booking
    from app.guest import guest
    from app.rate import rate
    from app.fee import fee
    app.register_blueprint(customer, url_prefix = "/api/customer")
    app.register_blueprint(rental, url_prefix = "/api/rental")
    app.register_blueprint(group, url_prefix = "/api/group")
    app.register_blueprint(booking, url_prefix = "/api/booking")
    app.register_blueprint(guest, url_prefix = "/api/guest")
    app.register_blueprint(rate, url_prefix = "/api/rate")
    app.register_blueprint(fee, url_prefix = "/api/fee")

register_blueprints()
