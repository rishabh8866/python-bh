from flask import jsonify, request, g
from flask.globals import session
from app import app, db, auth
from app.customer import customer
from app.group.model import Group
from app.customer.enums import PropertyEnum, CurrencyEnum, TimeDisplayEnum, DateDisplayEnum, TypeEnum, NumberDisplayEnum, OauthTypeEnum
from app.customer import mapper as customer_mapper
from app.customer import utils
from app import views as common_views
from app.customer.model import Customer
import constants,json

from app.group import group
from app.group.model import Group
from app.group import mapper as group_mapper

from app.rental.model import Rental
from app.rate.model import Rate
from app.rate import mapper as rate_mapper

from app.invoice.model import Invoice

NumberDisplay={
    "M1":"1,000.00",
    "M2":"1'000.00",
    "M3":"1.000,00"
}

dateDisplay={
    "M1" : "YYYY/MM/DD",
    "M2" : "YY/MM/DD",
    "M3" : "YYYY-MM-DD",
    "M4" : "YY-MM-DD",
    "M5" : "MM/DD/YYYY",
    "M6" : "MM/DD/YY",
    "M7" : "MM-DD-YYYY",
    "M8" : "MM-DD-YY",
    "M9" : "MMM DD, YYYY",
    "M10" : "MMM DD 'YY"
}

timeDisplay={
    "AM_PM": "AM_PM",
    "H" : "H"
}

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
        return response_object,200
    # check if user us already exists or not
    user = Customer.query.filter_by(_email_id=request.json['emailId']).first()
    if user:
        response_object = jsonify({
            "status" : 'fail',
            "message": 'This email is alredy associated with an account. Please sign in or choose another email address.'
        })
        return response_object,200
    else:
        data = utils.clean_up_request(request.json)
        try:
            c = customer_mapper.get_obj_from_request(data,request.json['emailId'])
        except Exception as e:
            return common_views.internal_error(constants.view_constants.MAPPING_ERROR)
        try:
            db.session.add(c)
            db.session.commit()

            # Creating default group when user creating
            try:
                group_data = {
                    "groupName": "Default",
                    "color": "Yellow"
                }
                user = Customer.query.filter_by(_email_id=request.json['emailId']).first()
                gp = Group(name = group_data["groupName"], color = group_data["color"], customer_id = user.id)
            except Exception as e:
                return common_views.internal_error(constants.view_constants.MAPPING_ERROR)
            try:
                db.session.add(gp)
                db.session.commit()

                # Bulk default rental creation up to noOfUnits passed by the user at signup time
                for i in range(1,data['noOfUnits']+1):
                    r = Rental(name="Rental {0}".format(i), address_line1="", postal_code="", country=data['country'], max_guests="4", currency=data['currency'],
                               checkin_time=data['checkInTime'], checkout_time=data['checkOutTime'], customer_id=user.id, group_id=gp.id)
                    db.session.add(r)
                    db.session.commit()
                    db.session.flush()
                    try:
                        # Add default rate
                        default_rate = Rate(rental_id=r.id, usd_per_guest=1, date_range="", minimum_stay_requirement=data['minimumStayRequirement'], week_days="MON", daily_rate=data[
                                            'dailyRate'], guest_per_night=2, allow_discount=False, weekly_discount=0, monthly_discount=0, allow_fixed_rate=False, week_price=0, monthly_price=0, customer_id=user.id, group_id=gp.id)
                        db.session.add(default_rate)
                        db.session.commit()
                    except Exception as e:
                        print(e)
            except Exception as e:
                return common_views.internal_error(constants.view_constants.DB_TRANSACTION_FAULT)

        except Exception as e:
            response_object = jsonify({
                    "status" : 'fail',
                    "message": 'Invalid payload'
                })
            return response_object,200
        #customer made send the email process
        utils.send_mail(c)
        #return common_views.as_success(constants.view_constants.USER_REGISTRATION_SUCCESSFUL)
        response_object = jsonify({
            "data":request.json,
            "token": str(c.generate_auth_token().decode("utf-8")),
            "status" : 'success',
             "message": 'Account created successfully! Please check your email to log in.'
        })
        return response_object,200


@customer.route("/oauth/login", methods = ["GET"])
def oauth_login():
    type = request.args.get('type')
    return jsonify({
        "data": {
            "uri": utils.get_oauth_url(type, request.base_url + "/callback")
            }
        }), 302


@customer.route("/oauth/login/callback", methods = ["GET"])
def oauth_login_callback():
    code = request.args.get("code")
    type = OauthTypeEnum.GOOGLE
    # facebook login
    if "state" in request.args and request.args.get("state") == "abc":
        type = OauthTypeEnum.FACEBOOK
    email = utils.get_user_email_from_oauth(code, request.url, request.base_url, type)
    return login_user_through_email(email, False)


@customer.route("/login", methods = ["POST"])
def email_login():
    if not request.json:
        response_object = jsonify({
            "status" : 'fail',
            "message": 'Invalid payload'
        })
        return response_object,200
    data = utils.clean_up_request(request.json)
    email_id = data["emailId"]
    return login_user_through_email(email_id)


def login_user_through_email(email_id, do_send_email = True):
    c = Customer.query.filter_by(_email_id = email_id).first()
    if c:
        data = {
            "id": c.id,
            "createdAt": str(c._created_at),
            "customerType": c._customer_type,
            "emailId": c._email_id,
            "name": c._name,
            "noOfUnits": c._number_of_rooms,
            "checkInTime":c._check_in_time,
            "checkOutTime":c._check_out_time,
            "country":c._country,
            "minimumStayRequirement":c._minimum_stay_requirement
        }
        if do_send_email:
            utils.send_mail(c)
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
            "status" : 'fail',
            "message": 'This email address is not registered in our system. Please check the spelling or create an account.'
        })
        return response_object,200


@customer.route("/login/<string:auth_token>", methods = ["GET"])
def login(auth_token):
    if not auth_token:
        return common_views.bad_request(constants.view_constants.REQUEST_PARAMETERS_NOT_SUFFICIENT)
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
    c = Customer.query.get(g.customer.id)
    # Check if invoice Data is in DB or not.
    invoice = Invoice.query.filter_by(_customer_id=g.customer.id).first()
    if invoice:
        customer_data = {
            "accountType": c._account_type,
            "allowBookingFor": c._allow_booking_for,
            "country": c._country,
            "createdAt": c._created_at,
            "currency": c._currency,
            "customerType": c._customer_type,
            "dateDisplay":c._date_display.name,
            "emailId": c._email_id,
            "id": c.id,
            "isFutureBooking": c._is_future_booking,
            "language": c._language,
            "name": c._name,
            "noOfUnits": c._number_of_rooms,
            "numberDisplay": c._number_display,
            "permissions": c._permissions,
            "propertyType": c._property_type,
            "timeDisplay": c._time_display,
            "website": c._website,
            "invoiceName":invoice._name,
            "address1":invoice._address1,
            "address2":invoice._address2,
            "address3":invoice._address3,
            "invoiceText":invoice._invoice_text,
            "invoiceFooter":invoice._invoice_footer,
            "country":{
                "label":invoice._country_label,
                "value":invoice._country_value,
            }
        }
    else:
        customer_data = {
            "accountType": c._account_type,
            "allowBookingFor": c._allow_booking_for,
            "country": c._country,
            "createdAt": c._created_at,
            "currency": c._currency,
            "customerType": c._customer_type,
            "dateDisplay":c._date_display.name,
            "emailId": c._email_id,
            "id": c.id,
            "isFutureBooking": c._is_future_booking,
            "language": c._language,
            "name": c._name,
            "noOfUnits": c._number_of_rooms,
            "numberDisplay": c._number_display,
            "permissions": c._permissions,
            "propertyType": c._property_type,
            "timeDisplay": c._time_display,
            "website": c._website,
        }
    response_object = jsonify({
        "customer":customer_data,
        "status" : 'success',
        "message": 'Customer fetched'
    })
    return response_object,200


# Current users settings.
@customer.route("/customerSettings", methods = ["PUT"])
@auth.login_required
def customer_settings():
    if not g.customer:
        return common_views.not_authenticated(constants.view_constants.NOT_AUTHENTICATED)
    if not request.json:
        return common_views.bad_request(constants.view_constants.REQUEST_PARAMETERS_NOT_SUFFICIENT)
    data = utils.clean_up_request(request.json)
    current_email = g.customer._email_id
    c = customer_mapper.get_obj_from_request(data,current_email)
    # Find record by email..
    customer_update = Customer.query.filter_by(_email_id=g.customer._email_id).first()
    if customer_update:
        customer_update._name = data['name']
        customer_update._language = data['language']
        customer_update._is_future_booking = data['isFutureBooking']
        customer_update._permissions = data['permissions']
        customer_update._allow_booking_for = data['allowBookingFor']
        customer_update._account_type = data['accountType']
        customer_update._number_of = data['numberOf']
    else:
        response_object = jsonify({
            "status" : 'fail',
            "message": 'please check provided details'
        })
        return response_object,200
    try:
        db.session.commit()
        cust_data = {
            "id":g.customer.id,
            "accountType": data['accountType'],
            "allowBookingFor":  data['allowBookingFor'],
            "emailId": "demringen@hotmail.red.com",
            "isFutureBooking": data['isFutureBooking'],
            "language": data['name'],
            "name": data['name'],
            "numberOf": data['numberOf'],
            "permissions":  data['permissions']
        }
    except Exception as e:
        return common_views.internal_error(constants.view_constants.DB_TRANSACTION_FAULT)
    response_object = jsonify({
            "data":cust_data,
            "status" : 'success',
            "message": 'Customer Settings updated'
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
    current_email = g.customer._email_id
    c = customer_mapper.get_obj_from_request(data,current_email)
    # Find record by email of currently logged-in user..
    customer_update = Customer.query.filter_by(_email_id=current_email).first()
    if customer_update:
        customer_update._currency = data['currency']
        customer_update._time_display = data['timeDisplay']
        customer_update._date_display = data['dateDisplay']
        customer_update._number_display = data['numberDisplay']

        # Check if record exists in invoice table,if exists then update else add as new record
        invoice_update = Invoice.query.filter_by(_customer_id=g.customer.id).first()
        if invoice_update:
            invoice_update._name =data['invoiceName']
            invoice_update._address1 =data['address1']
            invoice_update._address2 =data['address2']
            invoice_update._address3 =data['address3']
            invoice_update._country_label=data['country']['label']
            invoice_update._country_value=data['country']['value']
            invoice_update._invoice_text=data['invoiceText']
            invoice_update._invoice_footer=data['invoiceFooter']
            db.session.commit()
        else:
            # Create new Record in DB if not available
            invoice = Invoice(customer_id=g.customer.id,name=data['invoiceName'],address1=data['address1'],\
                address2=data['address2'],address3=data['address3'],country_label=data['country']['label'],country_value=data['country']['value'],\
                    invoice_text=data['invoiceText'],invoice_footer=data['invoiceFooter'])
            db.session.add(invoice)
            db.session.commit()
    else:
        response_object = jsonify({
                "status" : 'fail',
                "message": 'please check provided details'
            })
        return response_object,200
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        return common_views.internal_error(constants.view_constants.DB_TRANSACTION_FAULT)
    response_object = jsonify({
            "data":{
                "id": g.customer.id,
                "currency":data['currency'],
                "dateDisplay":data['dateDisplay'],
                "emailId":data['emailId'],
                "name":data['name'],
                "numberDisplay":NumberDisplay[data["numberDisplay"]],
                "timeDisplay":data['timeDisplay'],
                "invoiceName":data['invoiceName'],
                "address1":data['address1'],
                "address2":data['address2'],
                "address3":data['address3'],
                "invoiceText":data['invoiceText'],
                "invoiceFooter":data['invoiceFooter'],
                "country":{
                    "label":data['country']['label'],
                    "value":data['country']['value']
                }
            },
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
    current_email = g.customer._email_id
    c = customer_mapper.get_obj_from_request(data,current_email)
    # Find record by email and update..
    customer_update = Customer.query.filter_by(_email_id=current_email).first()
    if customer_update:
        customer_update._name = data['name']
        customer_update._number_of_rooms = data['noOfUnits']
        customer_update._property_type = data['propertyType']
        customer_update._website = data['website']
    else:
        response_object = jsonify({
                "status" : 'fail',
                "message": 'please check provided details'
            })
        return response_object,400
    # c = utils.get_obj_from_request(data, g.customer)
    try:
        db.session.commit()
    except Exception as e:
        return common_views.internal_error(constants.view_constants.DB_TRANSACTION_FAULT)
    c = customer_mapper.get_obj_from_customer_info(g.customer.full_serialize())
    response_object = jsonify({
        "customer":c,
        "status" : 'success',
        "message": 'Customer updated'
    })
    return response_object,200
    # return jsonify({"customer": c})


@customer.route("/<string:Id>", methods = ["DELETE"])
@auth.login_required
def delete_customer(Id):
    if not Id:
        return common_views.bad_request(constants.view_constants.REQUEST_PARAMETERS_NOT_SUFFICIENT)
    customer = Customer.query.get(Id)
    if customer:
        try:
            db.session.delete(customer)
            db.session.commit()
        except Exception as e:
            print(e)
            return common_views.internal_error(constants.view_constants.DB_TRANSACTION_FAULT)
        response_object = jsonify({
            "status":"success",
            "message":'Customer deleted',
            "id": Id
        })
        return response_object,200
    else:
        response_object = jsonify({
            "status":"fail",
            "message":"Customer not exists"
        })
        return response_object,200
