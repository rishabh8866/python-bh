from flask import jsonify, request, g
from app import app, db, auth
from app.guest import guest
from app.guest.model import Guest
from app.guest import utils
from app.booking.model import Booking
from app import views as common_views
from app.guest import mapper as guest_mapper
import constants

@guest.route("/", methods = ["POST"])
@auth.login_required
def add_guest():
    if not request.json:
        return common_views.bad_request(constants.view_constants.REQUEST_PARAMETERS_NOT_SUFFICIENT)
    data = utils.clean_up_request(request.json)
    try:
        guest = guest_mapper.get_obj_from_request(data, g.customer)
    except Exception as e:
        print("Jasdeep couldn't map " + str(e))
        return common_views.internal_error(constants.view_constants.MAPPING_ERROR)
    try:
        db.session.add(guest)
        db.session.commit()
    except:
        return common_views.internal_error(constants.view_constants.DB_TRANSACTION_FAULT)
    return common_views.as_success(constants.view_constants.SUCCESS)

@guest.route("/getGuestByBookingId/<string:bookingId>", methods = ["POST"])
@auth.login_required
def get_guests_for_booking(bookingId):
    if not request.json:
        return common_views.bad_request(constants.view_constants.REQUEST_PARAMETERS_NOT_SUFFICIENT)
    data = utils.clean_up_request(request.json)
    booking = Booking.query.get(int(bookingId))
    resp = []
    for guest in booking.guests:
        resp.append(guest.half_serialize())
    return jsonify({"guests": resp})

@guest.route("/addGuestByBookingId/<string:bookingId>", methods = ["POST"])
@auth.login_required
def add_guest_to_booking(bookingId):
    if not request.json:
        return common_views.bad_request(constants.view_constants.REQUEST_PARAMETERS_NOT_SUFFICIENT)
    data = utils.clean_up_request(request.json)
    guest = Guest.query.get(int(data["guest_id"]))
    booking = Booking.query.get(int(bookingId))
    guest.bookings.append(booking)
    try:
        db.session.add(guest)
        db.session.commit()
    except:
        return common_views.internal_error(constants.view_constants.DB_TRANSACTION_FAULT)
    return common_views.as_success(constants.view_constants.SUCCESS)
