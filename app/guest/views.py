from flask import jsonify, request, g
from app import app, db, auth
from app.guest import guest
from app.guest.model import Guest,guest_bookings
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
        request.json["id"] = guest.id
    except Exception as e:
        print(e)
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
            # Cancelled booking when guest deleted
            for booking in g._bookings:
                booking._status = 'Cancelled'
                db.session.commit()
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


@guest.route("/", methods = ["PUT"])
@auth.login_required
def update_guests():
    if not request.json:
        return common_views.bad_request(constants.view_constants.REQUEST_PARAMETERS_NOT_SUFFICIENT)
    data = request.json
    # Find record by email and update..
    guest_update = Guest.query.get(data['id'])
    if guest_update:
        guest_update._name = data['name']
        guest_update._email_id = data['emailId']
        guest_update._phone_no = data['phoneNo']
        guest_update._secondary_email_id = data['secondaryEmailId']
        guest_update._country = data['country']
        guest_update._address = data['address']
        guest_update._postal_code = data['postalCode']
        guest_update._state = data['state']
        guest_update._nationality = data['nationality']
        guest_update._language = data['language']
        guest_update._notes = data['notes']
    else:
        response_object = jsonify({
                "status" : 'failed',
                "message": 'please check provided details'
            })
        return response_object,400
    # c = utils.get_obj_from_request(data, g.customer)
    try:
        db.session.commit()
    except Exception as e:
        return common_views.internal_error(constants.view_constants.DB_TRANSACTION_FAULT)

    resp = guest_mapper.get_obj_from_Guest_info(guest_update.full_serialize())
    response_object = jsonify({
        "guest":resp,
        "status" : 'success',
        "message": 'Guest updated'
    })
    return response_object,200


@guest.route("/getGuestByBookingId/<string:bookingId>", methods = ["GET"])
@auth.login_required
def get_guests_for_booking(bookingId):
    if not bookingId:
        return common_views.bad_request(constants.view_constants.REQUEST_PARAMETERS_NOT_SUFFICIENT)
    booking = Booking.query.get(int(bookingId))
    if booking:
        resp = []
        for guest in booking.guests:
            resp.append(guest.half_serialize())
        return jsonify({"guests": resp})
    else:
        response_object = jsonify({
            "status" : 'fail',
            "message": 'Record not exists'
        })
        return response_object,200


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
    except Exception as e:
        return common_views.internal_error(constants.view_constants.DB_TRANSACTION_FAULT)
    return common_views.as_success(constants.view_constants.SUCCESS)


@guest.route("/addGuestByBookingId/<string:bookingId>", methods = ["PUT"])
@auth.login_required
def update_guest_to_booking(bookingId):
    if not request.json:
        return common_views.bad_request(constants.view_constants.REQUEST_PARAMETERS_NOT_SUFFICIENT)
    data = utils.clean_up_request(request.json)
    guest = Guest.query.get(int(data["guestId"]))
    if guest:
        db.engine.execute('UPDATE guest_bookings SET guest_id={0} WHERE booking_id={1}'.format(data['guestId'],bookingId))
        return common_views.as_success(constants.view_constants.SUCCESS)
    else:
        response_object = jsonify({
            "status" : 'fail',
            "message": 'Guest Record not exists'
        })
        return response_object,200