from flask import jsonify, request, g
from app import app, db, auth
from app.booking import booking
from app.booking.model import Booking
from app.booking import utils
from app.booking import mapper as booking_mapper
import app.views as common_views
import constants

@booking.route("/", methods = ["POST"])
@auth.login_required
def add_booking():
    if not request.json:
        return common_views.bad_request(constants.view_constants.REQUEST_PARAMETERS_NOT_SUFFICIENT)
    data = utils.clean_up_request(request.json)
    try:
        b = booking_mapper.get_obj_from_request(data, g.customer)
    except:
        return common_views.internal_error(constants.view_constants.MAPPING_ERROR)
    try:
        db.session.add(b)
        db.session.commit()
    except:
        return common_views.internal_error(constants.view_constants.DB_TRANSACTION_FAULT)
    return common_views.as_success(constants.view_constants.SUCCESS)

@booking.route("/<string:bookingId>", methods = ["DELETE"])
@auth.login_required
def delete_booking(bookingId):
    if not bookingId:
        return common_views.bad_request(constants.view_constants.REQUEST_PARAMETERS_NOT_SUFFICIENT)
    booking = Booking.query.get(bookingId)
    try:
        db.session.delete(booking)
        db.session.commit()
    except:
        return common_views.internal_error(constants.view_constants.DB_TRANSACTION_FAULT)
    return common_views.as_success(constants.view_constants.SUCCESS)
