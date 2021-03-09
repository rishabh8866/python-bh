from app.guest.model import Guest

fields = {
    "primary": ["name", "email_id", "phone_no", "customer_id"],
    "secondary": ["secondary_email_id", "country", "address", "postal_code", "state", "nationality", "language", "notes"],
    "unique": []
}

def get_obj_from_request(data, customer):
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
