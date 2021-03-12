from flask import jsonify, request, g
from app import app, db, auth
from app.group import group
from app.group.model import Group
from app.group import mapper as group_mapper
from app import views as common_views
import constants

@group.route("/", methods = ["POST"])
@auth.login_required
def add_group():
    if not request.json:
        return common_views.bad_request(constants.view_constants.REQUEST_PARAMETERS_NOT_SUFFICIENT)
    data = request.json
    try:
        gp = group_mapper.get_obj_from_request(data, g.customer)
    except Exception as e:
        print("Jasdeep exception : " + str(e))
        return common_views.internal_error(constants.view_constants.MAPPING_ERROR)
    try:
        db.session.add(gp)
        db.session.commit()
    except:
        return common_views.internal_error(constants.view_constants.DB_TRANSACTION_FAULT)
    response_object = jsonify({
        "group": gp.full_serialize(),
        "status" : 'success',
        "message": 'Group Created'
        })
    return response_object,200

@group.route("/", methods = ["PUT"])
@auth.login_required
def edit_group():
    if not request.json:
        return common_views.bad_request(constants.view_constants.REQUEST_PARAMETERS_NOT_SUFFICIENT)
    try:
        data = request.json
        gp = group_mapper.update_obj_from_request(data)
    except Exception as e:
        return common_views.internal_error(constants.view_constants.MAPPING_ERROR)
    try:
        db.session.commit()
    except:
        return common_views.internal_error(constants.view_constants.DB_TRANSACTION_FAULT)
    # return common_views.as_success(constants.view_constants.SUCCESS)
    response_object = jsonify({
        "data":request.json,
        "status" : 'success',
        "message": 'Successfully Updated'
    })
    return response_object,200

@group.route("/", methods = ["GET"])
@auth.login_required
def list_groups():
    groups = Group.query.filter(Group._customer_id == g.customer.id)
    list_resp = []
    for group in groups:
        list_resp.append(group.half_serialize())
    return jsonify({"groups": list_resp})

@group.route("/<string:groupId>", methods = ["DELETE"])
@auth.login_required
def delete_group(groupId):
    if not groupId:
        return common_views.bad_request(constants.view_constants.REQUEST_PARAMETERS_NOT_SUFFICIENT)
    gp = Group.query.get(int(groupId))
    if gp:
        try:
            db.session.delete(gp)
            db.session.commit()
        except:
            return common_views.internal_error(constants.view_constants.DB_TRANSACTION_FAULT)
        response_object = jsonify({
            "status" : 'success',
            "message": 'Group deleted'
        })
        return response_object,200
    else:
        response_object = jsonify({
            "status" : 'fail',
            "message": 'Group not exists'
        })
        return response_object,200

@group.route("/groupRental", methods = ["POST"])
@auth.login_required
def add_rental_to_group():
    if not request.json:
        return common_views.bad_request(constants.view_constants.REQUEST_PARAMETERS_NOT_SUFFICIENT)
    data = request.json
    group = Group.query.get(data["groupId"])
    rental = Rental.query.get(data["rentalId"])
    group.rentals.append(rental)
    try:
        db.session.add(group)
        db.session.commit()
    except:
        return common_views.internal_error(constants.view_constants.DB_TRANSACTION_FAULT)
    return common_views.as_success(constants.view_constants.SUCCESS)
