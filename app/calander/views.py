from flask import jsonify, request, g,json
from app.calander import calander
from datetime import datetime, timedelta


# Use to get a single record
@calander.route("/", methods = ["post"])
def calander():
    content = []
    if not request.json:
        # If data is blank or invalid
        response_object = jsonify({
                "status" : 'fail',
                "message": 'Invalid payload'
        })
        return response_object,400
    data = request.json
    # date_object1 = datetime.strptime(data['dateRange'].split()[0], '%Y-%m-%d').date()
    # date_object2 = datetime.strptime(data['dateRange'].split()[2], '%Y-%m-%d').date()
    date_object1 = datetime.strptime(data['startDate'] , '%Y-%m-%d').date()
    date_object2 = datetime.strptime(data['endDate'] , '%Y-%m-%d').date()
    day = timedelta(days=1)
    while date_object1 <= date_object2:
        data_append = {}
        data_append["date"] = date_object1
        data_append["rate"] = data['rate']
        data_append["nights"] = data['nights']
        date_object1 = date_object1 + day
        content.append(data_append)
    response_object = {
        "data":content,
        "status": 'success',
        "message": 'success'
    }
    return response_object,200
