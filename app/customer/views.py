from flask import jsonify, request, g
from app import app, db, auth
from app.customer import customer
from app.customer import mapper as customer_mapper
from app.customer import utils
from app import views as common_views
from app.customer.model import Customer
import constants,json


@auth.verify_password
def verify_password(unused_1, unused_2):
    auth_token = request.headers.get("auth-token")
    print("Jasdeep auth token is: ", auth_token)
    if auth_token:
        customer = Customer.verify_auth_token(auth_token)
        if not customer:
            return False
        g.customer = customer
        return True
    return False

@auth.error_handler
def auth_error(status):
    response = jsonify({
        'token_expire':"Access is denied or Expired, please request a new token"
    })
    return response, status

@app.before_request
def before_request():
    g.customer = customer

@customer.route("/index", methods = ["GET", "POST"])
def index():
    return jsonify({"msg": "success"})

@customer.route("/register", methods = ["POST"])
def register():
    if not request.json:
        response_object = jsonify({
            "status" : 'fail',
            "message": 'Invalid payload'
        })
        return response_object,400
    # check if user us alredy exists or not
    user = Customer.query.filter_by(_email_id=request.json['emailId']).first()
    if user:
        response_object = jsonify({
            "status" : 'fail',
            "message": 'That email is taken. Please choose another.'
        })
        return response_object,400
    else:
        data = utils.clean_up_request(request.json)
        try:
            c = customer_mapper.get_obj_from_request(data)
        except Exception as e:
            return common_views.internal_error(constants.view_constants.MAPPING_ERROR)
        try:
            db.session.add(c)
            db.session.commit()
        except Exception as e:
            response_object = jsonify({
                    "status" : 'fail',
                    "message": 'Invalid payload'
                })
            return response_object,400
            # return common_views.internal_error(constants.view_constants.DB_TRANSACTION_FAULT)
        
        #customer made send the email process
        utils.send_mail(c)
        #return common_views.as_success(constants.view_constants.USER_REGISTRATION_SUCCESSFUL)
        response_object = jsonify({
            "data":request.json,
            "token": str(c.generate_auth_token().decode("utf-8")),
            "status" : 'success',
            "message": 'Customer created'
        })
        return response_object,200

@customer.route("/login", methods = ["POST"])
def email_login():
    if not request.json:
        response_object = jsonify({
            "status" : 'fail',
            "message": 'Invalid payload'
        })
        return response_object,400
        # return common_views.bad_request(constants.view_constants.REQUEST_PARAMETERS_NOT_SUFFICIENT)
    data = utils.clean_up_request(request.json)
    email_id = data["emailId"]
    c = Customer.query.filter_by(_email_id = email_id).first()
    if c: 
        data = {
            "createdAt": str(c._created_at),
            "customerType": c._customer_type,
            "emailId": c._email_id,
            "name": c._name,
            "noOfUnits": c._number_of_rooms,
        }
        # utils.send_mail(c)
        jsonified_data = json.dumps(data)
        response_object = jsonify({
                "data":json.loads(jsonified_data),
                "token": str(c.generate_auth_token().decode("utf-8")),
                "status" : 'Success',
                "message": 'User logged in'
            })
        return response_object,200
    else:
        response_object = jsonify({
            "status" : 'failed',
            "message": 'Customer not exists'
        })
        return response_object,200

@customer.route("/login/<string:auth_token>", methods = ["GET"])
def login(auth_token):
    if not auth_token:
        return common_views.bad_request(constants.view_constants.REQUEST_PARAMETERS_NOT_SUFFICIENT)
    print("Jasdeep auth token is " + auth_token)
    c = Customer.verify_auth_token(auth_token).half_serialize()
    if not c:
        return common_views.not_authenticated(constants.view_constants.TOKEN_NOT_VALID)
    c = customer_mapper.get_obj_from_customer_info(c)   
    return jsonify({"user": c, "success": constants.view_constants.USER_LOGGED_IN})


@customer.route("/customerInfo", methods = ["GET"])
@auth.login_required
def get_customer():
    if not g.customer:
        return common_views.not_authenticated(constants.view_constants.NOT_AUTHENTICATED)
    c = customer_mapper.get_obj_from_customer_info(g.customer.half_serialize())    
    return jsonify({"customer": c})

# @customer.route("/customerSettings", methods = ["GET"])
# @auth.login_required
# def customer_settings():
#     if not g.customer:
#         return common_views.not_authenticated(constants.view_constants.NOT_AUTHENTICATED)
#     c = customer_mapper.get_obj_from_customer_info(g.customer.full_serialize()) 
#     return jsonify({"customer": c})

# Current users settings.
@customer.route("/customerSettings", methods = ["PUT"])
@auth.login_required
def customer_settings():
    if not g.customer:
        return common_views.not_authenticated(constants.view_constants.NOT_AUTHENTICATED)
    if not request.json:
        return common_views.bad_request(constants.view_constants.REQUEST_PARAMETERS_NOT_SUFFICIENT)
    data = utils.clean_up_request(request.json)
    c = customer_mapper.get_obj_from_request(data)
    # Find record by email..
    customer_update = Customer.query.filter_by(_email_id=data['emailId']).first()
    customer_update._email_id = data['emailId']
    customer_update._language = data['language']
    customer_update._is_future_booking = data['isFutureBooking']
    customer_update._permissions = data['permissions']
    customer_update._allow_booking_for = data['allowBookingFor']
    customer_update._account_type = data['accountType']
    try:
        db.session.commit()
    except Exception as e:
        return common_views.internal_error(constants.view_constants.DB_TRANSACTION_FAULT)
    response_object = jsonify({
            "data":request.json,
            "status" : 'success',
            "message": 'Customer updated'
        })
    return response_object,200

@customer.route("/generalSettings", methods = ["PUT"])
@auth.login_required
def general_settings():
    if not g.customer:
        return common_views.not_authenticated(constants.view_constants.NOT_AUTHENTICATED)
    if not request.json:
        return common_views.bad_request(constants.view_constants.REQUEST_PARAMETERS_NOT_SUFFICIENT)
    data = utils.clean_up_request(request.json)
    c = customer_mapper.get_obj_from_request(data)
    # Find record by email..
    customer_update = Customer.query.filter_by(_email_id=data['emailId']).first()
    customer_update._currency = data['currency']
    customer_update._time_display = data['timeDisplay']
    customer_update._date_display = data['dateDisplay']
    customer_update._number_display = data['numberDisplay']
    try:
        db.session.commit()
    except Exception as e:
        print("Exceptions :",e)
        return common_views.internal_error(constants.view_constants.DB_TRANSACTION_FAULT)
    response_object = jsonify({
            "data":request.json,
            "status" : 'success',
            "message": 'general settings updated'
        })
    return response_object,200
  
@customer.route("/updateCustomer", methods = ["PUT"])
@auth.login_required
def update_customer():
    if not g.customer:
        return common_views.not_authenticated(constants.view_constants.NOT_AUTHENTICATED)
    if not request.json:
        return common_views.bad_request(constants.view_constants.REQUEST_PARAMETERS_NOT_SUFFICIENT)
    data = utils.clean_up_request(request.json)
    c = customer_mapper.get_obj_from_request(data)
    # Find record by email and update..
    customer_update = Customer.query.filter_by(_email_id=data['emailId']).first()
    customer_update._name = data['name']
    customer_update._number_of_rooms = data['noOfUnits']
    customer_update._property_type = data['propertyType']
    customer_update._website = data['website']
    # c = utils.get_obj_from_request(data, g.customer)
    try:
        db.session.commit()
    except Exception as e:
        return common_views.internal_error(constants.view_constants.DB_TRANSACTION_FAULT)
    c = customer_mapper.get_obj_from_customer_info(c.full_serialize())  
    return jsonify({"customer": c})
