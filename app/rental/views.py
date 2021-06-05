from flask import jsonify, request, g
from app import app, db, auth
from app.rental import rental
from app.rental.model import Rental
from app.booking.model import Booking
from app.fee.model import Fee
from app.rental import mapper as rental_mapper
from app.rate import mapper as rate_mapper
from app import views as common_views
from app.rental import utils
import constants
import json

from app.rate.model import Rate
from app.rate import mapper as rate_mapper

@rental.route("/", methods = ["POST"])
@auth.login_required
def add_rental():
    if not request.json:
        # If data is blank or invalid
        response_object = jsonify({
            "status" : 'fail',
            "message": 'Invalid payload'
        })
        return response_object,400
        # return common_views.bad_request(constants.view_constants.REQUEST_PARAMETERS_NOT_SUFFICIENT)
    data = request.json
    utils.clean_up_request(data)
    check_rental_limit = Rental.query.filter(Rental._customer_id==g.customer.id).count()
    if check_rental_limit >= 10:
        response_object = jsonify({
            "status" : 'fail',
            "message": 'Maximum of 10 rentals allowed in free version. Please contact support if you wish to add more rentals.'
        })
        # return common_views.as_success(constants.view_constants.SUCCESS)
        return response_object,200
    else:
        try:
            r = rental_mapper.get_obj_from_request(data, g.customer)
        except Exception as e:
            print("Jasdeep db exception: " + str(e))
            return common_views.internal_error(constants.view_constants.MAPPING_ERROR)
        try:
            db.session.add(r)
            db.session.commit()
            db.session.flush()
            try:
                # Add default rate
                default_rate = Rate(rental_id=r.id, usd_per_guest=1, date_range="", minimum_stay_requirement=g.customer._minimum_stay_requirement, week_days="MON", daily_rate=g.customer._daily_rate, guest_per_night=2,
                                    allow_discount=False, weekly_discount=0, monthly_discount=0, allow_fixed_rate=False, week_price=0, monthly_price=0, customer_id=g.customer.id, group_id=None)
                db.session.add(default_rate)
                db.session.commit()
            except Exception as e:
                print(e)
            
        except Exception as e:
            print("Jasdeep db exception: " + str(e))
            return common_views.internal_error(constants.view_constants.DB_TRANSACTION_FAULT)
        response_object = jsonify({
            "data": rental_mapper.get_response_object(r.full_serialize()),
            "status" : 'success',
            "message": 'Successfully Added'
        })
        # return common_views.as_success(constants.view_constants.SUCCESS)
        return response_object,200


@rental.route("/", methods = ["PUT"])
@auth.login_required
def edit_rental():
    if not request.json:
        return common_views.bad_request(constants.view_constants.REQUEST_PARAMETERS_NOT_SUFFICIENT)
    rental_exists = Rental.query.get(request.json['id'])
    if  rental_exists:
        try:
            r = rental_mapper.update_obj_from_request(request.json)
        except Exception as e:
            print("Jasdeep mapping error: ", str(e))
            return common_views.internal_error(constants.view_constants.MAPPING_ERROR)
        try:
            db.session.commit()
        except Exception as e:
            print("dddJasdeep db exception: " + str(e))
            return common_views.internal_error(constants.view_constants.DB_TRANSACTION_FAULT)
        response_object = jsonify({
                "data": rental_mapper.get_response_object(r.full_serialize()),
                "status" : 'success',
                "message": 'Successfully Updated'
        })
        return response_object,200
    else:
        response_object = jsonify({
                "status" : 'fail',
                "message": 'record not exists'
        })
        return response_object,200



@rental.route("/", methods = ["GET"])
@auth.login_required
def list_rentals():
    customer = g.customer
    rentals = customer.rentals
    resp = []
    for rental in rentals:
        resp.append(rental_mapper.get_response_object(rental.full_serialize()))
    return jsonify({"rentals": resp})


@rental.route("/<string:rentalId>", methods = ["DELETE"])
@auth.login_required
def delete_rental(rentalId):
    if not rentalId:
        return common_views.bad_request(constants.view_constants.REQUEST_PARAMETERS_NOT_SUFFICIENT)
    rental_id = rentalId
    gp = Rental.query.get(rental_id)
    if gp is not None:
        try:
            ckeck_in_booking = Booking.query.filter_by(_rental_id=rental_id).first()
            try:
                # If booking exisits then delete first
                db.session.delete(ckeck_in_booking)
                db.session.commit()
                ckeck_in_booking_deleted_status = True
                try:
                    if ckeck_in_booking_deleted_status:
                        # Delete rate that assosiated with rental
                        check_in_rate = Rate.query.filter_by(_rental_id=rental_id).first()
                        db.session.delete(check_in_rate)
                        db.session.commit()

                        # Delete fee that assosiated with rental
                        check_in_fee = Fee.query.filter_by(_rental_id=rental_id).first()
                        db.session.delete(check_in_fee)
                        db.session.commit() 

                        # Delete rental
                        db.session.delete(gp)
                        db.session.commit() 

                        response_object = jsonify({
                            "status" : 'success',
                            "message": 'Successfully Deleted',
                            "id": rentalId
                        })
                        # return common_views.as_success(constants.view_constants.SUCCESS)
                        return response_object,200

                except Exception as e:
                    print(e)
            except Exception as e:
                print(e)
        except:
            return common_views.internal_error(constants.view_constants.DB_TRANSACTION_FAULT)
    else:
        response_object = jsonify({
            "status" : 'fail',
            "message": 'Record not exists'
        })
        return response_object,200


# Use to get a single record
@rental.route("/<string:rentalId>", methods = ["GET"])
@auth.login_required
def get_single_rental(rentalId):
    if not rentalId:
        return common_views.bad_request(constants.view_constants.REQUEST_PARAMETERS_NOT_SUFFICIENT)
    rental_id = rentalId
    gp = Rental.query.get(rental_id)
    if gp: 
        data = {
            "addressLine1": gp._address_line1,
            "addressLine2": gp._address_line2,
            "checkInTime": gp._checkin_time,
            "checkOutTime": gp._checkout_time,
            "currency": gp._currency,
            "groupId": gp._group_id,
            "id":gp.id,
            "maxGuests": gp._max_guests,
            "name": gp._name,
            "postalCode": gp._postal_code
        }
        jsonified_data = json.dumps(data)
        response_object = jsonify({
                "data":json.loads(jsonified_data),
                "status" : 'Success',
                "message": 'Record fetch successfully'
            })
        return response_object,200
    else:
        response_object = jsonify({
                "status" : 'fail',
                "message": 'Record not exists'
            })
        return response_object,200
