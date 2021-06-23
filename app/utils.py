import re
import hashlib
from urllib.parse import urlencode
from app import app, db
from flask_mail import Message
from app import mail
from flask_mail import Mail
from app.exceptions import DBException
import datetime
import calendar
from app import slack_client
from slack_sdk.errors import SlackApiError
import constants

AUTH_VERIFICATION = '''<html>
<body>
Dear {name},

To login please click on the link :

<a href="http://beehaz.com/verify/{token}">Login to Beehaz</a>

If you have not requested a login for Beehaz, please ignore this message.

Sincerely,

The Beehaz Team
</body>
</html>
'''


EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

def is_valid_email(val):
    if EMAIL_REGEX.match(val):
        return True
    return False

def clean_up_request(data):
    data1={}
    for key in data.keys():
        if isinstance(data[key],type("")):
            data1[key.strip()]=data[key].strip()
        else:
            data1[key.strip()]=data[key]
    return data1

def send_mail(subject, sender, recipients, body):
    app.logger.info("Sending mail")
    app.config.update(dict(
    MAIL_SERVER = app.config['MAIL_SERVER_GMAIL'],
    MAIL_PORT = app.config['MAIL_PORT_GMAIL'],
    MAIL_USE_TLS = app.config['MAIL_USE_TLS_GMAIL'],
    MAIL_USERNAME = app.config['MAIL_USERNAME_GMAIL'],
    MAIL_PASSWORD = app.config['MAIL_PASSWORD_GMAIL'],
    MAIL_USE_SSL =  app.config['MAIL_USE_SSL_GMAIL'],
    ))
    try:
        mail = Mail(app)
        msg = Message(subject, sender=sender, recipients=recipients)
        msg.html = body
        mail.send(msg)
    except Exception as e:
        app.logger.info("Couldn't send mail: " + str(e))
    app.logger.info("Sent mail")

def send_mail_ZOHO(subject, sender, recipients, body):
    app.config.update(dict(
    MAIL_SERVER = app.config['MAIL_SERVER'],
    MAIL_PORT = app.config['MAIL_PORT'],
    MAIL_USE_TLS = app.config['MAIL_USE_TLS'],
    MAIL_USERNAME = app.config['MAIL_USERNAME'],
    MAIL_PASSWORD = app.config['MAIL_PASSWORD'],
    MAIL_USE_SSL =  app.config['MAIL_USE_SSL'],
    ))
    mail.init_app(app)
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.html = body
    mail.send(msg)


def send_auth_email(user):
    token = str(user.generate_auth_token().decode("utf-8"))
    send_mail('[BeeHaz] Log In',
               app.config['ADMINS'][0],
               [user.email_id],
               AUTH_VERIFICATION.format(name = user.name, token = token))

def send_subscribers_email(email_list):
    print('\n\n\n\n\n\n\nemail list',email_list)
    send_mail_ZOHO('[BeeHaz] New features',
               app.config['ADMINS'][0],
               email_list,'New features contents')


def add_or_update_to_db(obj):
    try:
        db.session.add(obj)
        db.session.commit()
    except Exception as e:
        app.logger.error("Unable to save obj to db: {e}".format(e = e))
        raise DBException(e)

def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime.datetime(year, month, day)

def get_https(url):
    if url[:4] == "https":
        return url
    return "https" + url[4:]


def send_message_to_slack(msg, channel_id):
    response = None
    try:
        response = slack_client.chat_postMessage(channel = constants.SLACK_CHANNELS[channel_id]["channel"], text = constants.SLACK_CHANNELS[channel_id]["msg"].format(msg = str(msg)))
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        print("wtf why: " + str(e))
        assert e.response["error"]  #
    print("finish")