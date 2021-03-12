from flask import jsonify, request, g
from app import app, db, auth
from app.rental import rental
from app.rental.model import Rental
from app.rental import mapper as rental_mapper
from app import views as common_views
from app.rental import utils
import constants
import json

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
    try:
        r = rental_mapper.get_obj_from_request(data, g.customer)
    except Exception as e:
        print("Jasdeep db exception: " + str(e))
        return common_views.internal_error(constants.view_constants.MAPPING_ERROR)
    try:
        db.session.add(r)
        db.session.commit()
    except Exception as e:
        print("Jasdeep db exception: " + str(e))
        return common_views.internal_error(constants.view_constants.DB_TRANSACTION_FAULT)
    response_object = jsonify({
        "data":request.json,
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
    try:
        r = rental_mapper.update_obj_from_request(request.json)
    except Exception as e:
        print("Jasdeep mapping error: ", str(e))
        return common_views.internal_error(constants.view_constants.MAPPING_ERROR)
    try:
        db.session.commit()
    except Exception as e:
        print("Jasdeep db exception: " + str(e))
        return common_views.internal_error(constants.view_constants.DB_TRANSACTION_FAULT)
    response_object = jsonify({
            "data":request.json,
            "status" : 'success',
            "message": 'Successfully Updated'
    })
    return response_object,200
    # return common_views.as_success(constants.view_constants.SUCCESS)


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
            db.session.delete(gp)
            db.session.commit()
        except:
            return common_views.internal_error(constants.view_constants.DB_TRANSACTION_FAULT)
        response_object = jsonify({
            "status" : 'success',
            "message": 'Successfully Deleted'
        })
        # return common_views.as_success(constants.view_constants.SUCCESS)
        return response_object,200
    else:
        response_object = jsonify({
            "status" : 'failed',
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
            "checkInTime": gp._check_in_time,
            "checkOutTime": gp._check_out_time,
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
                "status" : 'failed',
                "message": 'Record not exists'
            })
        return response_object,200