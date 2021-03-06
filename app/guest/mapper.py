from app.guest.model import Guest

fields = {
    "primary": ["name", "email_id", "phone_no", "customer_id"],
    "secondary": ["secondary_email_id", "country", "address", "postal_code", "state", "nationality", "language", "notes","company"],
    "unique": []
}


mapFields = {
    "id":"id",
    "emailId": "email_id",
    "name": "name",
    "phoneNo": "phone_no",
    "customerId": "customer_id",
    "secondaryEmailId": "secondary_email_id",
    "country": "country",
    "address": "address",
    "postalCode": "postal_code",
    "state": "state",
    "nationality": "nationality",
    "language": "language",
    "notes": "notes",
    "bookings": "bookings",
    "company": "company"
}

fieldToMap = {
    "id":"id",
    "email_id": "emailId",
    "name": "name",
    "phone_no": "phoneNo",
    "customer_id": "customerId",
    "secondary_email_id": "secondaryEmailId",
    "country": "country",
    "address": "address",
    "postal_code": "postalCode",
    "state": "state",
    "nationality": "nationality",
    "language": "language",
    "notes": "notes",
    "company": "company"
}

def get_obj_from_request(apiData, customer):
    data = {}
    for x in apiData:
      data[mapFields[x]] = apiData[x]
    for field in fields["primary"]:
        if field not in data.keys():
            raise Exception(field + " not present")
    for field in fields["unique"]:
        if getattr(Guest, "check_" + field)(data[field]):
            raise Exception(field + " ought to be unique")
    guest = Guest(name = data["name"], email_id = data["email_id"], phone_no = data["phone_no"])
    for field in data.keys():
        if not field in fields["secondary"] and not field in fields["primary"]:
            print(field + " field is not necessary")
            continue
        print("Jasdeep setting " + field + " " + str(data[field]))
        setattr(guest, field, data[field])
    print("jasdeep guest made")
    return guest

def get_obj_from_Guest_info(data):
    apiData = {}
    for x in data:
        apiData[fieldToMap[x]] = data[x]
    return apiData 
