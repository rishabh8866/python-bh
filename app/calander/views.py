from flask import jsonify, request, g,json
from app.calander import calander
from app.rental.model import Rental
from app.booking.model import Booking
from datetime import datetime, timedelta
from itertools import groupby, permutations


# define a fuction for key to sort data..
def key_func(k):
    return k['rental']

# Use to get a single record
@calander.route("/", methods = ["post"])
def calander():
    rental_list = Rental.query.all()
    content = []
    rental_ap = []
    if not request.json:
        # If data is blank or invalid
        response_object = jsonify({
                "status" : 'fail',
                "message": 'Invalid payload'
        })
        return response_object,400
    else:
        all_status_updates = []
        all_status_updates_s = []

        data = request.json
        # Conver string to date
        date_object1 = datetime.strptime(data['startDate'] , '%Y-%m-%d').date()
        date_object2 = datetime.strptime(data['endDate'] , '%Y-%m-%d').date()

        # Copy date object
        copy_date_object_1 = date_object1
        day = timedelta(days=1)
        date_format = "%Y-%m-%d %H:%M:%S"
        for rental in rental_list: 
            # Get all assoicated booking with rental
            booking_details  = Booking.query.filter(Booking._rental_id==rental.id)
            match_checkin_time =  datetime.strptime(rental._checkin_time, date_format).date() 
            match_checkout_time =  datetime.strptime(rental._checkout_time, date_format).date() 

            # Loop through all date
            while date_object1 <= date_object2:
                if match_checkin_time <= date_object1 <= match_checkout_time:
                    data_append = {}
                    data_append["rental"] =rental._name
                    data_append["date"] = date_object1.strftime('%Y-%m-%d')
                    data_append["rate"] = data['rate']
                    data_append["nights"] = data['nights']
                    # Uncomment if need booking details
                    # for booking_detail in booking_details:
                    #     data_append["booking"] = booking_detail._title
                    # Check if booking is available or not if yes then booking status is true
                    if booking_details:
                        data_append["booking_status"] = True
                    content.append(data_append)
                    all_status_updates.append(date_object1.strftime('%Y-%m-%d'))
                elif not match_checkin_time <= date_object1 <= match_checkout_time:
                    if all_status_updates == []:
                        pass
                    else:
                        if date_object1.strftime('%Y-%m-%d') not in all_status_updates:
                            all_status_updates_s.append(date_object1.strftime('%Y-%m-%d'))
                date_object1 = date_object1 + day
            date_object1=copy_date_object_1

        # Find remianing dates and append it with response.
        list1 = list(set(all_status_updates))
        list2 = list(set(all_status_updates_s))
        if list1 != [] and list2 !=[]:
            for element in list1:
                if element in list2:
                    list2.remove(element)
            for i in sorted(list2, key=lambda x: datetime.strptime(x, '%Y-%m-%d')):
                data_append = {}
                data_append["rental"] =""
                data_append["date"] = i
                data_append["rate"] = ""
                data_append["nights"] = ""
                if booking_details:
                    data_append["booking_status"] = False
                content.append(data_append)

            # sort INFO data by 'rental' key.
            INFO = sorted(content, key=key_func)
            for key, value in groupby(INFO, key_func):
                data_append = {}
                data_append["rental"] =key
                data_append["rental_data"] = list(value)
                rental_ap.append(data_append)
            response_object = {
                "data":rental_ap,
                "status": 'success',
                "message": 'success'
            }
            return response_object,200
        else:
            date_object1 = datetime.strptime(data['startDate'] , '%Y-%m-%d').date()
            date_object2 = datetime.strptime(data['endDate'] , '%Y-%m-%d').date()
            while date_object1 <= date_object2:
                data_append = {}
                data_append["rental"] = ''
                data_append["date"] = date_object1.strftime('%Y-%m-%d')
                data_append["rate"] = ''
                data_append["nights"] = ''
                # Uncomment if need booking details
                # for booking_detail in booking_details:
                #     data_append["booking"] = booking_detail._title
                
                # Check if booking is available or not if yes then booking status is true
                if booking_details:
                    data_append["booking_status"] = False
                content.append(data_append)
                date_object1 = date_object1 + day
            
            INFO = sorted(content, key=key_func)
            for key, value in groupby(INFO, key_func):
                data_append = {}
                data_append["rental"] =key
                data_append["rental_data"] = list(value)
                rental_ap.append(data_append)
            response_object = {
                "data":rental_ap,
                "status": 'success',
                "message": 'success'
            }
            return response_object,200