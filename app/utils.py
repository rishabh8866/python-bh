import re
import hashlib
from urllib.parse import urlencode
from app import app
from flask_mail import Message
from app import mail


AUTH_VERIFICATION = '''<html>
<body>
Dear {name},

The token is:

<a href="http://beehaz.com/verify/{token}">Login</a>

If you have not requested a verification simply ignore this message.

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
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.html = body
    mail.send(msg)


def send_auth_email(user):
    token = str(user.generate_auth_token().decode("utf-8"))
    message = ""
    send_mail('[BeeHaz] Log In',
                message,
               app.config['ADMINS'][0],
               [user.email_id],
               AUTH_VERIFICATION.format(name = user.name, token = token))