import stripe
from app.customer.model import Customer
from app import utils
from datetime import datetime

def get_customer_from_webhook_event(event):
    customer_id = event['data']['object']['customer']
    user_id = stripe.Customer.retrieve(customer_id)["metadata"]["id"]
    print("Jasdeep id is: " + str(user_id))
    return int(user_id)

def update_customer_payment_status(customer_id, updated_status):
    customer = Customer.query.get(customer_id)
    customer.payment_status = updated_status
    utils.add_or_update_to_db(customer)