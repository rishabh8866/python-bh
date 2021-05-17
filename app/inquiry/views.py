from flask import jsonify, request, g
from app import app, db, auth
from app.inquiry import inquiry
from app.booking.model import Booking
from app.guest.model import Guest,guest_bookings
from app.customer.model import Customer
from app.rental.model import Rental
# from app.tax import mapper as tax_mapper
from app import views as common_views
from app.rate import utils
import constants
import json
from datetime import datetime,date
import calendar

# Use to get a single record
@inquiry.route("/", methods = ["GET"])
def list_inquiry():
    todays_date = datetime.now()
    last_day_of_month = calendar.monthrange(todays_date.year,todays_date.month)[1]
    last_date =  str(todays_date.year)+"-"+str(todays_date.month)+"-"+str(last_day_of_month)
    if not request.json:
        response_object = jsonify({
            "status" : 'fail',
            "message": 'Invalid payload'
        })
        return response_object,400
    data = utils.clean_up_request(request.json)
    # check blank values
    d = []
    if data['dateFrom'] == None and data['dateTo']==None and data['rentalId']==None:
        booking_lists = Booking.query.filter(Booking._customer_id==data['customerId'])
        guest_names = Guest.query.filter(Booking._customer_id==data['customerId'])
        
        for booking_list,guest_name in zip(booking_lists,guest_names):
            date_format = "%Y-%m-%d"
            a = datetime.strptime(booking_list._arrive, date_format)
            b = datetime.strptime(booking_list._depart, date_format)
            delta = b - a  # number of nights.
            rental = Rental.query.get(booking_list._rental_id)
            data = {
                "bookingNumber":booking_list.id,
                "channel":booking_list._source,
                "guestName":guest_name.name,
                "checkInTime":booking_list._check_in_time,
                "checkOutTime":booking_list._check_out_time,
                "nights":str(delta.days),
                "netAmount": booking_list._price,
                "createdDate": "2021-01-1",
                "paymentStatus": booking_list._payment_status,
                "status": booking_list._status,
                "arrive":booking_list._arrive,
                "depart":booking_list._depart,
                "rentalId":booking_list._rental_id,
                "rentalName":rental.name,
                "currency":rental._currency,
                "createdAt":booking_list._created_at
            }
            d.append(data)
        if d == []:
            response_object = jsonify({
                "status" : 'fail',
                "message": 'Records not found'
            })
            return response_object,200
        else:
            response_object = jsonify({
                "data":d,
                "status" : 'success',
                "message": 'Records found'
            })
            return response_object,200
    elif data['rentalId']!=None and data['dateFrom'] == None and data['dateTo'] == None:
        booking_lists = Booking.query.filter(Booking._customer_id==data['customerId'],Booking._rental_id==data['rentalId'])
        guest_name = Guest.query.filter(Booking._customer_id==data['customerId']).first()
        for booking_list in booking_lists:
            date_format = "%Y-%m-%d"
            a = datetime.strptime(booking_list._arrive, date_format)
            b = datetime.strptime(booking_list._depart, date_format)
            delta = b - a  # number of nights.
            
            data = {
                "bookingNumber":booking_list.id,
                "channel":booking_list._source,
                "guestName":guest_name.name,
                "checkInTime":booking_list._check_in_time,
                "checkOutTime":booking_list._check_out_time,
                "nights":str(delta.days),
                "netAmount": booking_list._price,
                "createdDate": "2021-01-1",
                "paymentStatus": booking_list._payment_status,
                "status": booking_list._status,
                "arrive":booking_list._arrive,
                "depart":booking_list._depart,
                "rentalId":booking_list._rental_id,
            }
            d.append(data)
        if d == []:
            response_object = jsonify({
                "status" : 'fail',
                "message": 'Records not found'
            })
            return response_object,200
        else:
            response_object = jsonify({
                "data":d,
                "status" : 'success',
                "message": 'Records found'
            })
            return response_object,200
    elif data['dateFrom'] != None and data['dateTo'] != None and data['rentalId'] != None:
        booking_lists = Booking.query.filter(Booking._customer_id==data['customerId'],Booking._rental_id==data['rentalId'])
        guest_name = Guest.query.filter(Booking._customer_id==data['customerId']).first()
        
        get_post_arrive_date = data['dateFrom']
        get_post_depart_date = data['dateTo']

        for booking_list in booking_lists:
            start_date = booking_list._arrive
            end_date = booking_list._depart
            if (start_date <= get_post_arrive_date <= end_date) or (get_post_arrive_date <= start_date <= get_post_depart_date) :
                # Find number of nights
                date_format = "%Y-%m-%d"
                a = datetime.strptime(booking_list._arrive, date_format)
                b = datetime.strptime(booking_list._depart, date_format)
                delta = b - a  # number of nights.
                data = {
                    "bookingNumber":booking_list.id,
                    "channel":booking_list._source,
                    "guestName":guest_name.name,
                    "checkInTime":booking_list._check_in_time,
                    "checkOutTime":booking_list._check_out_time,
                    "nights":str(delta.days),
                    
                    "netAmount": booking_list._price,
                    "createdDate": "2021-01-1",
                    
                    "paymentStatus": booking_list._payment_status,
                    "status": booking_list._status,
                    "arrive":booking_list._arrive,
                    "depart":booking_list._depart,
                    "rentalId":booking_list._rental_id,
                }
                d.append(data)
        if d == []:
            response_object = jsonify({
                "status" : 'fail',
                "message": 'Records not found'
            })
            return response_object,200
        else:
            response_object = jsonify({
                "data":d,
                "status" : 'success',
                "message": 'Records found'
            })
            return response_object,200
    elif data['dateFrom'] != None and data['dateTo'] == None and data['rentalId'] == None:
        # 'datefrom chee and dateto and rentalid nathi'
        booking_lists = Booking.query.filter(Booking._customer_id==data['customerId'])
        guest_name = Guest.query.filter(Booking._customer_id==data['customerId']).first()
        
        get_post_arrive_date = data['dateFrom']
        get_post_depart_date = Booking.query.filter(Booking._customer_id==data['customerId']).order_by(Booking.id.desc()).first()._depart
        

        for booking_list in booking_lists:
            start_date = booking_list._arrive
            end_date = booking_list._depart
            if (start_date <= get_post_arrive_date <= end_date) or (get_post_arrive_date <= start_date <= get_post_depart_date) :
                # Find number of nights
                date_format = "%Y-%m-%d"
                a = datetime.strptime(booking_list._arrive, date_format)
                b = datetime.strptime(booking_list._depart, date_format)
                delta = b - a  # number of nights.
                data = {
                    "bookingNumber":booking_list.id,
                    "channel":booking_list._source,
                    "guestName":guest_name.name,
                    "checkInTime":booking_list._check_in_time,
                    "checkOutTime":booking_list._check_out_time,
                    "nights":str(delta.days),
                    
                    "netAmount": booking_list._price,
                    "createdDate": "2021-01-1",
                    
                    "paymentStatus": booking_list._payment_status,
                    "status": booking_list._status,
                    "arrive":booking_list._arrive,
                    "depart":booking_list._depart,
                    "rentalId":booking_list._rental_id,
                }
                d.append(data)
        if d == []:
            response_object = jsonify({
                "status" : 'fail',
                "message": 'Records not found'
            })
            return response_object,200
        else:
            response_object = jsonify({
                "data":d,
                "status" : 'success',
                "message": 'Records found'
            })
            return response_object,200
    elif data['dateFrom'] == None and data['dateTo'] != None and data['rentalId'] == None:
        # 'datefrom chee and dateto and rentalid nathi'
        booking_lists = Booking.query.filter(Booking._customer_id==data['customerId'])
        guest_name = Guest.query.filter(Booking._customer_id==data['customerId']).first()
        
        get_post_arrive_date = Booking.query.filter(Booking._customer_id==data['customerId']).first()._arrive
        get_post_depart_date = data['dateTo']

        for booking_list in booking_lists:
            start_date = booking_list._arrive
            end_date = booking_list._depart
            if (start_date <= get_post_arrive_date <= end_date) or (get_post_arrive_date <= start_date <= get_post_depart_date) :
                # Find number of nights
                date_format = "%Y-%m-%d"
                a = datetime.strptime(booking_list._arrive, date_format)
                b = datetime.strptime(booking_list._depart, date_format)
                delta = b - a  # number of nights.
                data = {
                    "bookingNumber":booking_list.id,
                    "channel":booking_list._source,
                    "guestName":guest_name.name,
                    "checkInTime":booking_list._check_in_time,
                    "checkOutTime":booking_list._check_out_time,
                    "nights":str(delta.days),
                    
                    "netAmount": booking_list._price,
                    "createdDate": "2021-01-1",
                    
                    "paymentStatus": booking_list._payment_status,
                    "status": booking_list._status,
                    "arrive":booking_list._arrive,
                    "depart":booking_list._depart,
                    "rentalId":booking_list._rental_id,
                }
                d.append(data)
        if d == []:
            response_object = jsonify({
                "status" : 'fail',
                "message": 'Records not found'
            })
            return response_object,200
        else:
            response_object = jsonify({
                "data":d,
                "status" : 'success',
                "message": 'Records found'
            })
            return response_object,200    
    elif data['dateFrom'] != None and data['dateTo'] == None and data['rentalId'] != None:
        #'datefrom and rentalid  chee and dateto nathi'
        booking_lists = Booking.query.filter(Booking._customer_id==data['customerId'],Booking._rental_id==data['rentalId'])
        guest_name = Guest.query.filter(Booking._customer_id==data['customerId']).first()
        
        get_post_arrive_date = data['dateFrom']
        get_post_depart_date = Booking.query.filter(Booking._customer_id==data['customerId']).order_by(Booking.id.desc()).first()._depart
        
        for booking_list in booking_lists:
            start_date = booking_list._arrive
            end_date = booking_list._depart
            if (start_date <= get_post_arrive_date <= end_date) or (get_post_arrive_date <= start_date <= get_post_depart_date) :
                # Find number of nights
                date_format = "%Y-%m-%d"
                a = datetime.strptime(booking_list._arrive, date_format)
                b = datetime.strptime(booking_list._depart, date_format)
                delta = b - a  # number of nights.
                data = {
                    "bookingNumber":booking_list.id,
                    "channel":booking_list._source,
                    "guestName":guest_name.name,
                    "checkInTime":booking_list._check_in_time,
                    "checkOutTime":booking_list._check_out_time,
                    "nights":str(delta.days),
                    
                    "netAmount": booking_list._price,
                    "createdDate": "2021-01-1",
                    
                    "paymentStatus": booking_list._payment_status,
                    "status": booking_list._status,
                    "arrive":booking_list._arrive,
                    "depart":booking_list._depart,
                    "rentalId":booking_list._rental_id,
                }
                d.append(data)
        if d == []:
            response_object = jsonify({
                "status" : 'fail',
                "message": 'Records not found'
            })
            return response_object,200
        else:
            response_object = jsonify({
                "data":d,
                "status" : 'success',
                "message": 'Records found'
            })
            return response_object,200
    elif data['dateFrom'] == None and data['dateTo'] != None and data['rentalId'] != None:
        #'datefrom and rentalid  chee and dateto nathi'
        booking_lists = Booking.query.filter(Booking._customer_id==data['customerId'],Booking._rental_id==data['rentalId'])
        guest_name = Guest.query.filter(Booking._customer_id==data['customerId']).first()
        
        get_post_arrive_date = Booking.query.filter(Booking._customer_id==data['customerId']).first()._arrive
        get_post_depart_date = data['dateTo']
        

        for booking_list in booking_lists:
            start_date = booking_list._arrive
            end_date = booking_list._depart
            if (start_date <= get_post_arrive_date <= end_date) or (get_post_arrive_date <= start_date <= get_post_depart_date) :
                # Find number of nights
                date_format = "%Y-%m-%d"
                a = datetime.strptime(booking_list._arrive, date_format)
                b = datetime.strptime(booking_list._depart, date_format)
                delta = b - a  # number of nights.
                data = {
                    "bookingNumber":booking_list.id,
                    "channel":booking_list._source,
                    "guestName":guest_name.name,
                    "checkInTime":booking_list._check_in_time,
                    "checkOutTime":booking_list._check_out_time,
                    "nights":str(delta.days),
                    
                    "netAmount": booking_list._price,
                    "createdDate": "2021-01-1",
                    
                    "paymentStatus": booking_list._payment_status,
                    "status": booking_list._status,
                    "arrive":booking_list._arrive,
                    "depart":booking_list._depart,
                    "rentalId":booking_list._rental_id,
                }
                d.append(data)
        if d == []:
            response_object = jsonify({
                "status" : 'fail',
                "message": 'Records not found'
            })
            return response_object,200
        else:
            response_object = jsonify({
                "data":d,
                "status" : 'success',
                "message": 'Records found'
            })
            return response_object,200
    elif data['dateFrom'] != None and data['dateTo'] != None and data['rentalId'] == None:
        #'datefrom and rentalid  chee and dateto nathi'
        booking_lists = Booking.query.filter(Booking._customer_id==data['customerId'])
        guest_name = Guest.query.filter(Booking._customer_id==data['customerId']).first()
        
        get_post_arrive_date = data['dateFrom']
        get_post_depart_date = data['dateTo']
        

        for booking_list in booking_lists:
            start_date = booking_list._arrive
            end_date = booking_list._depart
            if (start_date <= get_post_arrive_date <= end_date) or (get_post_arrive_date <= start_date <= get_post_depart_date) :
                # Find number of nights
                date_format = "%Y-%m-%d"
                a = datetime.strptime(booking_list._arrive, date_format)
                b = datetime.strptime(booking_list._depart, date_format)
                delta = b - a  # number of nights.
                data = {
                    "bookingNumber":booking_list.id,
                    "channel":booking_list._source,
                    "guestName":guest_name.name,
                    "checkInTime":booking_list._check_in_time,
                    "checkOutTime":booking_list._check_out_time,
                    "nights":str(delta.days),
                    
                    "netAmount": booking_list._price,
                    "createdDate": "2021-01-1",
                    
                    "paymentStatus": booking_list._payment_status,
                    "status": booking_list._status,
                    "arrive":booking_list._arrive,
                    "depart":booking_list._depart,
                    "rentalId":booking_list._rental_id,
                }
                d.append(data)
        if d == []:
            response_object = jsonify({
                "status" : 'fail',
                "message": 'Records not found'
            })
            return response_object,200
        else:
            response_object = jsonify({
                "data":d,
                "status" : 'success',
                "message": 'Records found'
            })
            return response_object,200