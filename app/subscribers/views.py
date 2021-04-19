from flask import jsonify, request, g
from app import app, db, auth
from app.subscribers import subscribers
from app import views as common_views
from app.subscribers import utils
import constants
import json
from datetime import datetime
from app.subscribers.model import Subscriber
from app.subscribers import mapper as subscriber_mapper


# TODO :
# 1. Need to add email functinality and send email to all users.
# 2. Need to add cancellation to unscubscribe
@subscribers.route("", methods = ["POST"])
def add_subscribers():
    if not request.json:
        # If data is blank or invalid
        response_object = jsonify({
            "status" : 'fail',
            "message": 'Invalid payload'
        })
        return response_object,400
    data = request.json
    exists = Subscriber.query.filter_by(_email_id=data['emailId']).first()
    if not exists:
        utils.clean_up_request(data)
        try:
            r = subscriber_mapper.get_obj_from_request(data)
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
            "data": subscriber_mapper.get_response_object(r.full_serialize()),
            "status" : 'success',
            "message": 'Successfully Added'
        })
        return response_object,200
    else:
        response_object = jsonify({
            "status" : 'fail',
            "message": 'Already subscribed'
        })
        return response_object,200



@subscribers.route("/list", methods = ["GET"])
def list_subscribers():
    subscribers_list = Subscriber.query.all()
    list_resp = []
    for subscriber in subscribers_list:
        list_resp.append(subscriber.full_serialize())
    
    response_object =jsonify({
        'subscribers' : list_resp,
        'status':'success',
        'message':'all subscribers'
    })
    return response_object,200