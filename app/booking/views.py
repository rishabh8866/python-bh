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
        # check if booking availbale or not
        booking_lists = Booking.query.filter_by(_customer_id=b.customer_id)
        if booking_lists:
            for booking_list in booking_lists:

                # Get dates from DB
                start_date = booking_list._arrive
                end_date = booking_list._depart

                get_post_arrive_date = data['arrive']
                get_post_depart_date = data['depart']

                if (start_date <= get_post_arrive_date <= end_date):
                    # check in rental table
                    rental_lists = Rental.query.filter_by(_customer_id=b.customer_id)
                    for rental_list in rental_lists:
                        # Convert dates from string to date format
                        start_date = datetime.datetime.strptime(rental_list._checkin_time, "%Y-%m-%d %H:%M:%S").date()
                        end_date = datetime.datetime.strptime(rental_list._checkout_time, "%Y-%m-%d %H:%M:%S").date()
                        get_post_arrive_date = datetime.datetime.strptime(data['arrive'], "%Y-%m-%d").date()
                        get_post_depart_date = datetime.datetime.strptime(data['depart'], "%Y-%m-%d").date()

                        # Check if the booking date is in rental and not overlap
                        if (start_date <= get_post_arrive_date <= end_date) or (start_date <= get_post_depart_date <= end_date):
                            data = {
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
                            }
                            jsonified_data = json.dumps(data,sort_keys=True,default=str)
                            response_object = jsonify({
                                "data": json.loads(jsonified_data),
                                "status": 'fail',
                                "message": 'You have already booking'
                            })
                            return response_object,200
                        else:
                            db.session.add(b)
                            db.session.commit()
                            response_object = jsonify({
                                'booking': data,
                                "status": "success",
                                "message": 'Booking created'
                            })
                else:
                    booking_lists = Booking.query.filter_by(_customer_id=b.customer_id)
                    for booking_list in booking_lists:

                        # Get dates from DB
                        start_date = booking_list._arrive
                        end_date = booking_list._depart

                        get_post_arrive_date = data['arrive']
                        get_post_depart_date = data['depart']

                        if (start_date <= get_post_arrive_date <= end_date):
                            db.session.add(b)
                            db.session.commit()
                            response_object = jsonify({
                                'booking': data,
                                "status": "success",
                                "message": 'Booking created'
                            })
                        else:
                            # check in rental table if date is not match in Booking and rental
                            rental_lists = Rental.query.filter_by(_customer_id=b.customer_id)
                            for rental_list in rental_lists:
                                start_date = datetime.datetime.strptime(rental_list._checkin_time, "%Y-%m-%d %H:%M:%S").date()
                                end_date = datetime.datetime.strptime(rental_list._checkout_time, "%Y-%m-%d %H:%M:%S").date()
                                get_post_arrive_date = datetime.datetime.strptime(data['arrive'], "%Y-%m-%d").date()
                                get_post_depart_date = datetime.datetime.strptime(data['depart'], "%Y-%m-%d").date()
                                if (start_date <= get_post_arrive_date <= end_date) or (start_date <= get_post_depart_date <= end_date):
                                    data = {
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
                                    }
                                    jsonified_data = json.dumps(data,sort_keys=True,default=str)
                                    response_object = jsonify({
                                        "data": json.loads(jsonified_data),
                                        "status": 'fail',
                                        "message": 'You have already booking'
                                    })
                                    return response_object,200
                                else:
                                    db.session.add(b)
                                    db.session.commit()
                                    response_object = jsonify({
                                        'booking':data,
                                        "status":"success",
                                        "message":'Booking created'
                                    })   
        db.session.add(b)
        db.session.commit()
        response_object = jsonify({
            'booking': data,
            "status": "success",
            "message": 'Booking created'
        })
        return response_object,200
    except Exception as e: 
        response_object = jsonify({
            'error_message': e,
            "status": "fail",
        })


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
