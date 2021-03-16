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
        response_object = jsonify({
            "status" : 'fail',
            "message": 'Invalid payload'
        })
        return response_object,400
        # return common_views.bad_request(constants.view_constants.REQUEST_PARAMETERS_NOT_SUFFICIENT)
    data = utils.clean_up_request(request.json)
    try:
        guest = guest_mapper.get_obj_from_request(data, g.customer)
    except Exception as e:
        print("Jasdeep couldn't map " + str(e))
        return common_views.internal_error(constants.view_constants.MAPPING_ERROR)
    try:
        db.session.add(guest)
        db.session.commit()
        request.json["id"] = guest.id;
    except Exception as e:
        return common_views.internal_error(constants.view_constants.DB_TRANSACTION_FAULT)
    response_object = jsonify({
        "guest" : request.json,
        "status":"success",
        "message":"Guest created"
    })
    return response_object,200
    # return common_views.as_success(constants.view_constants.SUCCESS)

@guest.route("/", methods = ["GET"])
@auth.login_required
def list_guests():
    print(g.customer.id)
    guests = Guest.query.filter(Guest._customer_id == g.customer.id)
    list_resp = []
    for guest in guests:
        list_resp.append(guest_mapper.get_obj_from_Guest_info(guest.full_serialize()))
    return jsonify({"guests": list_resp})

@guest.route("/<string:guestId>", methods = ["DELETE"])
@auth.login_required
def delete_guest(guestId):
    if not guestId:
        return common_views.bad_request(constants.view_constants.REQUEST_PARAMETERS_NOT_SUFFICIENT)
    g = Guest.query.get(int(guestId))
    if g:
        try:
            db.session.delete(g)
            db.session.commit()
        except:
            return common_views.internal_error(constants.view_constants.DB_TRANSACTION_FAULT)
        response_object = jsonify({
            "status" : 'success',
            "message": 'Guest deleted',
            "id": guestId
        })
        return response_object,200
    else:
        response_object = jsonify({
            "status" : 'fail',
            "message": 'Guest not exists'
        })
        return response_object,200

@guest.route("/getGuestByBookingId/<string:bookingId>", methods = ["GET"])
@auth.login_required
def get_guests_for_booking(bookingId):
    if not bookingId:
        return common_views.bad_request(constants.view_constants.REQUEST_PARAMETERS_NOT_SUFFICIENT)
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
    guest = Guest.query.get(int(data["guestId"]))
    booking = Booking.query.get(int(bookingId))
    guest.bookings.append(booking)
    try:
        db.session.add(guest)
        db.session.commit()
    except:
        return common_views.internal_error(constants.view_constants.DB_TRANSACTION_FAULT)
    return common_views.as_success(constants.view_constants.SUCCESS)
