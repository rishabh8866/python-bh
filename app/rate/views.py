from os import pathsep
from flask import jsonify, request, g
from app import app, db, auth
from app.rate import rate
from app.rate.model import Rate
from app.rate import mapper as rate_mapper
from app import views as common_views
from app.rate import utils
import constants
from app.rental.model import Rental
import json

from app.group.model import Group
from app.customer.model import Customer

@rate.route("/", methods = ["POST"])
@auth.login_required
def add_rate():
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
        exists =  Rental.query.filter_by(id=data['rentalId']).scalar()
        if exists:
            r = rate_mapper.get_obj_from_request(data, g.customer)
        else:
            response_object = jsonify({
            "status" : 'fail',
            "message": 'Rental not available'})
            return response_object,400
    except Exception as e:
        print("Exception: " + str(e))
        return common_views.internal_error(constants.view_constants.MAPPING_ERROR)
    try:
        db.session.add(r)
        db.session.commit()
    except Exception as e:
        return common_views.internal_error(constants.view_constants.DB_TRANSACTION_FAULT)
    response_object = jsonify({
        "data": rate_mapper.get_response_object(r.full_serialize()),
        "status" : 'success',
        "message": 'Successfully Created'
    })
    return response_object,200


@rate.route("/", methods = ["PUT"])
@auth.login_required
def edit_rate():
    if not request.json:
        print(request.json)
        return common_views.bad_request(constants.view_constants.REQUEST_PARAMETERS_NOT_SUFFICIENT)
    try:
        r = rate_mapper.update_obj_from_request(request.json)
    except Exception as e:
        print("Jasdeep mapping error: ", str(e))
        return common_views.internal_error(constants.view_constants.MAPPING_ERROR)
    try:
        db.session.commit()
    except Exception as e:
        print("Jasdeep db exception: " + str(e))
        return common_views.internal_error(constants.view_constants.DB_TRANSACTION_FAULT)
    response_object = jsonify({
            "data": rate_mapper.get_response_object(r.full_serialize()),
            "status" : 'success',
            "message": 'Successfully Updated'
    })
    return response_object,200


@rate.route("/<string:rateId>", methods = ["DELETE"])
@auth.login_required
def delete_rate(rateId):
    if not rateId:
        return common_views.bad_request(constants.view_constants.REQUEST_PARAMETERS_NOT_SUFFICIENT)
    rate_id = rateId
    gp = Rate.query.get(rate_id)
    if gp is not None:
        try:
            db.session.delete(gp)
            db.session.commit()
        except:
            return common_views.internal_error(constants.view_constants.DB_TRANSACTION_FAULT)
        response_object = jsonify({
            "status" : 'success',
            "message": 'Successfully Deleted',
            "id": rateId
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
@rate.route("/<string:rateId>", methods = ["GET"])
@auth.login_required
def get_single_rate(rateId):
    if not rateId:
        return common_views.bad_request(constants.view_constants.REQUEST_PARAMETERS_NOT_SUFFICIENT)
    rate_id = rateId
    gp = Rate.query.get(rateId)
    if gp: 
        data = {
            "rentalId":gp._rental_id,
            "dateRange": gp._date_range,
            "minimumStayRequirement":gp._minimum_stay_requirement,
            "dailyRate":gp._daily_rate,
            "guestPerNight":gp._guest_per_night ,
            "usdPerGuest":gp._usd_per_guest ,
            "allowDiscount":gp._allow_discount,
            "weeklyDiscount":gp._weekly_discount,
            "monthlyDiscount":gp._monthly_discount,
            "allowFixedRate":gp._allow_fixed_rate,
            "weekPrice":gp._week_price,
            "monthlyPrice":gp._monthly_price,
            "groupId":gp._group_id,
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


@rate.route("/", methods = ["GET"])
@auth.login_required
def  get_all_rate():
    rates = Rate.query.filter(Rate._customer_id == g.customer.id)
    list_resp = []
    for rate in rates:
        list_resp.append(rate_mapper.get_response_object(rate.full_serialize()))
    response_object = jsonify({
        "data": list_resp,
        "status" : 'success',
        "message": 'Successfully fetched'
    })
    return response_object,200


# Use to get a single record
@rate.route("/getRatesByRentalId/<string:rentalId>", methods = ["GET"])
@auth.login_required
def get_rates_by_rental(rentalId):
    if not rentalId:
        return common_views.bad_request(constants.view_constants.REQUEST_PARAMETERS_NOT_SUFFICIENT)
    rate_lists = Rate.query.filter(Rate._rental_id==rentalId)
    for rate_list in rate_lists:
        print(rate_list._group_id)
        if rate_list._group_id !=None:
            group= Group.query.get(rate_list._group_id)
            groupName = group._name
        else:
            groupName= ""
        data = {
            "id":rate_list.id,
            "rentalId":rate_list._rental_id,
            "dateRange": rate_list._date_range,
            "minimumStayRequirement":rate_list._minimum_stay_requirement,
            "dailyRate":rate_list._daily_rate,
            "guestPerNight":rate_list._guest_per_night ,
            "usdPerGuest":rate_list._usd_per_guest ,
            "allowDiscount":rate_list._allow_discount,
            "weeklyDiscount":rate_list._weekly_discount,
            "monthlyDiscount":rate_list._monthly_discount,
            "allowFixedRate":rate_list._allow_fixed_rate,
            "weekPrice":rate_list._week_price,
            "monthlyPrice":rate_list._monthly_price,
            "groupName":groupName,
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


# Multiple Rate update based on Rental id..
@rate.route("/multiple", methods = ["PUT"])
@auth.login_required
def multiple_update_rate():
    try:
        dataJson = request.json
        list_resp = []
        for data in dataJson:
            # Add default rate
            try:
                rates_lists = Rate.query.filter_by(_rental_id=data['rentalId'])
                for row in rates_lists:  # all() is extra
                    row._minimum_stay_requirement = data['minimumStayRequirement']
                    row._daily_rate = data['dailyRate']
                    rates = Rate.query.filter(Rate._customer_id == g.customer.id,Rate._rental_id==data['rentalId'])
                for rate in rates:
                    list_resp.append(rate_mapper.get_response_object(rate.full_serialize()))
                db.session.commit()
            except:
                for key,value in data.items():
                    if 'default' in key:
                        customer_update = Customer.query.filter_by(id=g.customer.id).first()
                        if customer_update:
                            customer_update._minimum_stay_requirement = data['default']['minimumStayRequirement']
                            customer_update._daily_rate = data['default']['dailyRate']
                            db.session.commit()    
        response_object = jsonify({
            "data": list_resp,
            "status" : 'success',
            "message": 'Successfully updated'
        })
        return response_object,200
    except Exception as e:
        print(e)