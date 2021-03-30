from flask import jsonify, request, g
from app import app, db, auth
from app.inquiry import inquiry
from app.booking.model import Booking
from app.guest.model import Guest
from app.customer.model import Customer
# from app.tax import mapper as tax_mapper
from app import views as common_views
from app.rate import utils
import constants
import json

# Use to get a single record
@inquiry.route("/", methods = ["GET"])
@auth.login_required
def list_inquiry():
    booking = Booking.query.filter_by(_customer_id=1)
    guest = Guest.query.filter_by(_customer_id=1)
    for g in guest:
        name = g.name

    for a in booking:
        data = {
            "guestName":name,
            "bookingNumber":a.id,
            "rentalId":a._rental_id,
            "checkInTime":a._check_in_time,
            "checkOutTime":a._check_out_time,
            "arrive":a._arrive,
            "depart":a._depart,
            "payment_status":a._payment_status
        }
    return jsonify(data)
