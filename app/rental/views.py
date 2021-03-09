from flask import jsonify, request, g
from app import app, db, auth
from app.rental import rental
from app.rental.model import Rental
from app.rental import mapper as rental_mapper
from app import views as common_views
from app.rental import utils
import constants

@rental.route("/", methods = ["POST"])
@auth.login_required
def add_rental():
    if not request.json:
        return common_views.bad_request(constants.view_constants.REQUEST_PARAMETERS_NOT_SUFFICIENT)
    data = request.json
    utils.clean_up_request(data)
    try:
        r = rental_mapper.get_obj_from_request(data, g.customer)
    except:
        return common_views.internal_error(constants.view_constants.MAPPING_ERROR)
    try:
        db.session.add(r)
        db.session.commit()
    except Exception as e:
        print("Jasdeep db exception: " + str(e))
        return common_views.internal_error(constants.view_constants.DB_TRANSACTION_FAULT)
    return common_views.as_success(constants.view_constants.SUCCESS)

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
    return common_views.as_success(constants.view_constants.SUCCESS)


@rental.route("/", methods = ["GET"])
@auth.login_required
def list_rentals():
    customer = g.customer
    rentals = customer.rentals
    resp = []
    for rental in rentals:
        resp.append(rental.half_serialize())
    return jsonify({"rentals": resp})

@rental.route("/", methods = ["DELETE"])
@auth.login_required
def delete_rental():
    if not request.json:
        return common_views.bad_request(constants.view_constants.REQUEST_PARAMETERS_NOT_SUFFICIENT)
    data = request.json
    rental_id = data["rental_id"]
    gp = Rental.query.get(rental_id)
    try:
        db.session.delete(gp)
        db.session.commit()
    except:
        return common_views.internal_error(constants.view_constants.DB_TRANSACTION_FAULT)
    return common_views.as_success(constants.view_constants.SUCCESS)
