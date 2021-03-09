import app.utils as common_utils
import calendar
import time

def clean_up_request(d):
    return common_utils.clean_up_request(d)

def send_mail(customer):
    common_utils.send_auth_email(customer)
