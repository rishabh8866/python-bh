from flask import jsonify, request, g
from app import app, db, auth
from app.booking import booking
from app.booking.model import Booking
from app.booking import utils
from app.booking import mapper as booking_mapper
import app.views as common_views
import constants,json
from sqlalchemy import and_


@booking.route("/", methods = ["POST"])
@auth.login_required
def add_booking():
    if not request.json:
        return common_views.bad_request(constants.view_constants.REQUEST_PARAMETERS_NOT_SUFFICIENT)
    data = utils.clean_up_request(request.json)
    try:
        b = booking_mapper.get_obj_from_request(data, g.customer)
    except Exception as e:
        return common_views.internal_error(constants.view_constants.MAPPING_ERROR)
    try:
        check_booking = Booking.query.filter_by(_customer_id=b.customer_id).filter(and_(Booking._arrive <= data['arrive'], Booking._depart >= data['depart'])).first()
        if check_booking:
            data = {
                "noOfAdults": check_booking._no_of_adults,
                "noOfChildrens": check_booking._no_of_children,
                "price": check_booking._price,
                "tax": check_booking._tax,
                "id":check_booking.id,
                "noOfGuests": check_booking._no_of_guests,
                "checkInTime": check_booking._check_in_time,
                "checkOutTime": check_booking._check_out_time,
                "paymentStatus": check_booking._payment_status,
                "source": check_booking._source,
            }
            jsonified_data = json.dumps(data,sort_keys=True,default=str)
            response_object = jsonify({
                    "data":json.loads(jsonified_data),
                    "status" : 'fail',
                    "message": 'You have already booking'
                })
            return response_object,200
        else:
            db.session.add(b)
            db.session.commit()
        data["id"] = b.id
    except Exception as e:
        print('Ex',e)
        return common_views.internal_error(constants.view_constants.DB_TRANSACTION_FAULT)
    response_object = jsonify({
        'booking':data,
        "status":"success",
        "message":'Booking created'
    })
    return response_object,200

@booking.route("/<string:bookingId>", methods = ["DELETE"])
@auth.login_required
def delete_booking(bookingId):
    if not bookingId:
        return common_views.bad_request(constants.view_constants.REQUEST_PARAMETERS_NOT_SUFFICIENT)
    booking = Booking.query.get(bookingId)
    if booking:
        try:
            db.session.delete(booking)
            db.session.commit()
        except:
            return common_views.internal_error(constants.view_constants.DB_TRANSACTION_FAULT)
        response_object = jsonify({
            "status":"success",
            "message":'Booking deleted',
            "id": bookingId
        })
        return response_object,200
    else:
        response_object = jsonify({
            "status":"fail",
            "message":"Record not exists"
        })
        return response_object,200

    # return common_views.as_success(constants.view_constants.SUCCESS)


@booking.route("/", methods = ["GET"])
@auth.login_required
def list_booking():
    bookings = Booking.query.filter(Booking._customer_id == g.customer.id)
    list_resp = []
    for booking in bookings:
        list_resp.append(booking.full_serialize())
    return jsonify({"booking": list_resp})
