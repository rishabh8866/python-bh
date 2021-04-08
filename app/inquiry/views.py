from flask import jsonify, request, g
from app import app, db, auth
from app.inquiry import inquiry
from app.booking.model import Booking
from app.guest.model import Guest
from app.customer.model import Customer
from app.rental.model import Rental
# from app.tax import mapper as tax_mapper
from app import views as common_views
from app.rate import utils
import constants
import json

# Use to get a single record
@inquiry.route("/", methods = ["GET"])
def list_inquiry():
    inquiry_query = Guest.query.filter_by(_customer_id=34)
    for i in inquiry_query:
        print(i._name)