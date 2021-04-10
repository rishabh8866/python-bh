from flask import jsonify, request, g
from app import app, db, auth
from app.booking import booking
from app.booking.model import Booking
from app.rental.model import Rental
from app.booking import utils
from app.booking import mapper as booking_mapper
import app.views as common_views
import constants,json
from sqlalchemy import and_
import datetime

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
        # check if booking availbale or not by filtering customer id and rental id
        booking_lists = Booking.query.filter_by(_customer_id=b.customer_id,_rental_id=data['rentalId']).all()
        if booking_lists:
            for booking_list in booking_lists:
                # Get dates from DB
                start_date = booking_list._arrive
                end_date = booking_list._depart

                get_post_arrive_date = data['arrive']
                get_post_depart_date = data['depart']

                if (start_date <= get_post_arrive_date <= end_date) or (get_post_arrive_date <= start_date <= get_post_depart_date) :
                    data = {
                            "rentalId": booking_list._rental_id,
                            "noOfAdults": booking_list._no_of_adults,
                            "noOfChildrens": booking_list._no_of_children,
                            "price": booking_list._price,
                            "tax": booking_list._tax,
                            "id":booking_list.id,
                            "noOfGuests": booking_list._no_of_guests,
                            "checkInTime": booking_list._check_in_time,
                            "checkOutTime": booking_list._check_out_time,
                            "arrival": booking_list._arrive,
                            "depart": booking_list._depart,
                            "paymentStatus": booking_list._payment_status,
                            "source": booking_list._source,
                            "bookingType": booking_list._booking_type,
                        }
                    jsonified_data = json.dumps(data,sort_keys=True,default=str)
                    response_object = jsonify({
                        "data": json.loads(jsonified_data),
                        "status": 'fail',
                        "message": 'Double bookings not avaiable,please change date or rental'
                    })
                    return response_object,200
            db.session.add(b)
            db.session.commit()
            db.session.flush()
            booking_list = Booking.query.filter_by(id=b.id).first()
            data = {
                    "rentalId": booking_list._rental_id,
                    "noOfAdults": booking_list._no_of_adults,
                    "noOfChildrens": booking_list._no_of_children,
                    "price": booking_list._price,
                    "tax": booking_list._tax,
                    "id":booking_list.id,
                    "noOfGuests": booking_list._no_of_guests,
                    "checkInTime": booking_list._check_in_time,
                    "checkOutTime": booking_list._check_out_time,
                    "arrival": booking_list._arrive,
                    "depart": booking_list._depart,
                    "paymentStatus": booking_list._payment_status,
                    "source": booking_list._source,
                    "bookingType": booking_list._booking_type,
                }
            response_object = jsonify({
                'booking': data,
                "status": "success",
                "message": 'Booking created'
            })
            return response_object,200
        else:
            # Check if rental id is correct or not.
            check_rental_id = Rental.query.filter_by(id=data['rentalId']).first()
            if check_rental_id == None:
                response_object = jsonify({
                    "status": "fail",
                    "message": 'Rental with this id does not exist, please enter valid id'
                })
                return response_object,200
            else:
                db.session.add(b)
                db.session.commit()
                db.session.flush()
                booking_list = Booking.query.filter_by(id=b.id).first()
                data = {
                        "rentalId": booking_list._rental_id,
                        "price": booking_list._price,
                        "noOfAdults": booking_list._no_of_adults,
                        "noOfChildrens": booking_list._no_of_children,
                        "tax": booking_list._tax,
                        "id":booking_list.id,
                        "noOfGuests": booking_list._no_of_guests,
                        "checkInTime": booking_list._check_in_time,
                        "checkOutTime": booking_list._check_out_time,
                        "arrival": booking_list._arrive,
                        "depart": booking_list._depart,
                        "paymentStatus": booking_list._payment_status,
                        "source": booking_list._source,
                        "bookingType": booking_list._booking_type,
                    }
                response_object = jsonify({
                    'booking': data,
                    "status": "success",
                    "message": 'Booking created'
                })
                return response_object,200
    except Exception as e:
        return common_views.internal_error(constants.view_constants.MAPPING_ERROR)


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

@booking.route("/", methods = ["GET"])
@auth.login_required
def list_booking():
    bookings = Booking.query.filter(Booking._customer_id == g.customer.id)
    list_resp = []
    for booking in bookings:
        list_resp.append(booking.full_serialize())
    return jsonify({"booking": list_resp})
