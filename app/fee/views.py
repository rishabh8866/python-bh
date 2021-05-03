from flask import jsonify, request, g
from app import app, db, auth
from app.fee import fee
from app.fee.model import Fee
from app.fee import mapper as fee_mapper
from app import views as common_views
from app.rate import utils
import constants
import json

@fee.route("/", methods = ["POST"])
@auth.login_required
def add_fee():
    if not request.json:
        # If data is blank or invalid
        response_object = jsonify({
            "status" : 'fail',
            "message": 'Invalid payload'
        })
        return response_object,400
    data = request.json
    utils.clean_up_request(data)
    try:
        r = fee_mapper.get_obj_from_request(data, g.customer)
    except Exception as e:
        print("Exception: " + str(e))
        return common_views.internal_error(constants.view_constants.MAPPING_ERROR)
    try:
        db.session.add(r)
        db.session.commit()
    except Exception as e:
        print("Exception",e)
        return common_views.internal_error(constants.view_constants.DB_TRANSACTION_FAULT)
    response_object = jsonify({
        "data": fee_mapper.get_response_object(r.full_serialize()),
        "status" : 'success',
        "message": 'Successfully Added'
    })
    return response_object,200

@fee.route("/", methods = ["GET"])
@auth.login_required
def get_all_fees():
    fees = Fee.query.filter(Fee._customer_id==g.customer.id)
    list_resp = []
    for fee in fees:
        list_resp.append(fee.full_serialize())
    return jsonify({"fee": list_resp})

@fee.route("/", methods = ["PUT"])
@auth.login_required
def edit_fee():
    if not request.json:
        print(request.json)
        return common_views.bad_request(constants.view_constants.REQUEST_PARAMETERS_NOT_SUFFICIENT)
    try:
        r = fee_mapper.update_obj_from_request(request.json)
    except Exception as e:
        print("Jasdeep mapping error: ", str(e))
        return common_views.internal_error(constants.view_constants.MAPPING_ERROR)
    try:
        db.session.commit()
    except Exception as e:
        print("Jasdeep db exception: " + str(e))
        return common_views.internal_error(constants.view_constants.DB_TRANSACTION_FAULT)
    response_object = jsonify({
            "data": fee_mapper.get_response_object(r.full_serialize()),
            "status" : 'success',
            "message": 'Successfully Updated'
    })
    return response_object,200


@fee.route("/<string:feeId>", methods = ["DELETE"])
@auth.login_required
def delete_fee(feeId):
    if not feeId:
        return common_views.bad_request(constants.view_constants.REQUEST_PARAMETERS_NOT_SUFFICIENT)
    fee_id = feeId
    gp = Fee.query.get(fee_id)
    if gp is not None:
        try:
            db.session.delete(gp)
            db.session.commit()
        except:
            return common_views.internal_error(constants.view_constants.DB_TRANSACTION_FAULT)
        response_object = jsonify({
            "status" : 'success',
            "message": 'Successfully Deleted',
            "id": feeId
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
@fee.route("/<string:feeId>", methods = ["GET"])
@auth.login_required
def get_single_fee(feeId):
    if not feeId:
        return common_views.bad_request(constants.view_constants.REQUEST_PARAMETERS_NOT_SUFFICIENT)
    fee_id = feeId
    gp = Fee.query.get(feeId)
    if gp: 
        data = {        
            "name"     : gp._name,                   
            "feeType" : gp._fee_type,
            "amount"     : gp._amount,               
            "modality"  : gp._modality         
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