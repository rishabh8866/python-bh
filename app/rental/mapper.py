from app.rental.model import Rental
from app.group.model import Group

fields = {
    "primary": ["name", "address_line1", "postal_code"],
    "secondary": ["address_line2", "country", "max_guests", "currency"],
    "unique": []
}




mapFields = {
    "rentalId":"rental_id",
    "name": "name",
    "postalCode": "postal_code",
    "addressLine1": "address_line1",
    "addressLine2": "address_line2",
    "country": "country",
    "checkInTime": "check_in_time",
    "checkOutTime": "check_out_time",
    "maxGuests": "max_guests",
    "groupId": "group_id",
    "currency": "currency",
}


fieldToMap = {
    "rental_id":"rentalId",
    "name": "name",
    "postal_code": "postalCode",
    "address_line1": "addressLine1",
    "address_line2": "addressLine2",
    "country": "country",
    "check_in_time": "checkInTime",
    "check_out_time": "checkOutTime",
    "id": "id",
    "group_id": "groupId",
    "currency": "currency",
    "max_guests": "maxGuests",
}

def get_obj_from_request(apiData, customer):
    data = {}
    for x in apiData:
      data[mapFields[x]] = apiData[x]
    for field in fields["primary"]:
        if field not in data.keys():
            raise Exception(field + " not present")
    for field in fields["unique"]:
        if getattr(Rental, "check_" + field)(data[field]):
            raise Exception(field + " ought to be unique")
    rental = Rental(name = data["name"], address_line1 = data["address_line1"], postal_code = "postal_code")
    for field in data.keys():
        if not field in fields["secondary"] and not field in fields["primary"]:
            print(field + " field is not necessary")
            continue
        print("Jasdeep setting " + field + " " + str(data[field]))
        setattr(rental, field, data[field])
    rental.customer_id = customer.id
    if "group_id" in data:
        gp_id = int(data["group_id"])
        gp = Group.query.get(gp_id)
        if gp:
            rental.group_id = gp_id
    print("jasdeep rental made")
    return rental

def update_obj_from_request(apiData):
    data = {}
    for x in apiData:
      data[mapFields[x]] = apiData[x]
    for field in fields["unique"]:
        if getattr(Rental, "check_" + field)(data[field]):
            raise Exception(field + " ought to be unique")
    rental = Rental.query.get(int(data["rental_id"]))
    for field in data.keys():
        if not field in fields["secondary"] and not field in fields["primary"]:
            print(field + " field is not necessary")
            continue
        print("Jasdeep setting " + field + " " + str(data[field]))
        setattr(rental, field, data[field])
    if "group_id" in data:
        gp_id = int(group_id)
        gp = Group.query.get(gp_id)
        if gp:
            rental.group_id = gp_id
    return rental

def get_response_object(data):
    apiData = {}
    for x in data:
        apiData[fieldToMap[x]] = data[x]
    return apiData  
    
