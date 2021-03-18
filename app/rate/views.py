from flask import jsonify, request, g
from app import app, db, auth
from app.rate import rate
from app.rate.model import Rate
from app.rate import mapper as rate_mapper
from app import views as common_views
from app.rate import utils
import constants
import json

@rate.route("/", methods = ["POST"])
@auth.login_required
def add_rate():
    print('CALL')
    if not request.json:
        # If data is blank or invalid
        response_object = jsonify({
            "status" : 'fail',
            "message": 'Invalid payload'
        })
        return response_object,400
        # return common_views.bad_request(constants.view_constants.REQUEST_PARAMETERS_NOT_SUFFICIENT)
    data = request.json
    print(data)
    utils.clean_up_request(data)
    try:
        r = rate_mapper.get_obj_from_request(data, g.customer)
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
        "data": rate_mapper.get_response_object(r.full_serialize()),
        "status" : 'success',
        "message": 'Successfully Added'
    })
    # return common_views.as_success(constants.view_constants.SUCCESS)
    return response_object,200