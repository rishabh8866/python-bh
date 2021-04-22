import json
from app.customer.model import Customer

fields = {
    "primary": ["email_id", "name"],
    "secondary": ["number_of_rooms", "website", "property_type","currency","number_of","country","check_in_time","check_out_time","daily_rate","minimum_stay_requirement"],
    "unique": ["email_id"]
}


mapFields = {
    "id":"id",
    "emailId": "email_id",
    "name": "name",
    "noOfUnits": "number_of_rooms",
    "companyName": "property_type",
    "propertyType": "property_type",
    "website": "website",
    "language":"language",
    "permissions":"permissions",
    "isFutureBooking":"is_future_booking",
    "allowBookingFor":"allow_booking_for",
    "accountType":"account_type",
    "currency": "currency",
    "timeDisplay": "time_display",
    "dateDisplay": "date_display",
    "numberDisplay": "number_display",
    "numberOf":"number_of",
    "country":"country",
    "checkInTime":"check_in_time",
    "checkOutTime":"check_out_time",
    "dailyRate":"daily_rate",
    "minimumStayRequirement":"minimum_stay_requirement",
}

fieldToMap = {
    "id":"id",
    "email_id": "emailId",
    "name": "name",
    "number_of_rooms": "noOfUnits",
    "property_type": "companyName",
    "property_type": "propertyType",
    "website": "website",
    "customer_type": "customerType",
    "created_at": "createdAt",
    "number_display": "numberDisplay",
    "date_display": "dateDisplay",
    "currency": "currency",
    "time_display": "timeDisplay",
    "language":"language",
    "permissions":"permissions",
    "is_future_booking":"isFutureBooking",
    "allow_booking_for":"allowBookingFor",
    "account_type":"accountType",
    "number_of":"numberOf",
    "country" : "country",
    "check_in_time":"checkInTime",
    "check_out_time":"checkOutTime",
    "daily_rate":"dailyRate",
    "minimum_stay_requirement":"minimumStayRequirement",
}

def get_obj_from_request(apiData,current_email):
    print("GET",current_email)
    # assume data is json
    data = {}
    for x in apiData:
      data[mapFields[x]] = apiData[x]
    for field in fields["primary"]:
        if field not in data.keys():
            raise Exception(field + " not present")
    for field in fields["unique"]:
        if getattr(Customer, "check_" + field)(data[field]):
            raise Exception(field + " ought to be unique")
    customer = Customer(current_email, name = data["name"])
    for field in data.keys():
        if not field in fields["secondary"] and not field in fields["primary"]:
            print(field + " field is not necessary")
            continue
        print("Jasdeep setting " + field + " " + str(data[field]))
        setattr(customer, field, data[field])
    print("jasdeep customer made")
    return customer

def update_obj_from_request(apiData, customer):
    data = {}
    for x in apiData:
      data[mapFields[x]] = apiData[x]
    for field in data:
        if field in field["unique"]:
            if getattr(Customer, "check_" + field)(data[field]):
                raise Exception(field + " ought to be unique")
    for field in data:
        setattr(customer, field, data[field])
    return customer

def get_obj_from_customer_info(data):
    apiData = {}
    for x in data:
        apiData[fieldToMap[x]] = data[x]
    return apiData  