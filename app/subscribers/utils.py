from app import utils as common_utils

def clean_up_request(data):
    return common_utils.clean_up_request(data)

def send_mail(customer):
    common_utils.send_subscribers_email(customer)