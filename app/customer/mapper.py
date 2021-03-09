import json
from app.customer.model import Customer

fields = {
    "primary": ["email_id", "name"],
    "secondary": ["number_of_rooms", "website", "property_type"],
    "unique": ["email_id"]
}


mapFields = {
    "emailId": "email_id",
    "name": "name",
    "noOfUnits": "number_of_rooms",
    "companyName": "property_type",
    "propertyType": "property_type",
    "website": "website",
}

def get_obj_from_request(apiData):
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
    customer = Customer(data["email_id"], name = data["name"])
    for field in data.keys():
        if not field in fields["secondary"] and not field in fields["primary"]:
            print(field + " field is not necessary")
            continue
        print("Jasdeep setting " + field + " " + str(data[field]))
        setattr(customer, field, data[field])
    print("jasdeep customer made")
    return customer

def update_obj_from_request(data, customer):
    for field in data:
        if field in field["unique"]:
            if getattr(Customer, "check_" + field)(data[field]):
                raise Exception(field + " ought to be unique")
    for field in data:
        setattr(customer, field, data[field])
    return customer
