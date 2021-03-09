from app.booking.model import Booking

fields = {
    "primary": ["no_of_adults", "price", "tax", "rental_id"],
    "secondary": ["no_of_children", "check_in_time", "check_out_time", "payment_status", "source"],
    "unique": []
}

def get_obj_from_request(data, customer):
    for field in fields["primary"]:
        if field not in data.keys():
            raise Exception(field + " not present")
    for field in fields["unique"]:
        if getattr(Rental, "check_" + field)(data[field]):
            raise Exception(field + " ought to be unique")
    booking = Booking()
    for field in data.keys():
        if not field in fields["secondary"] and not field in fields["primary"]:
            print(field + " field is not necessary")
            continue
        print("Jasdeep setting " + field + " " + str(data[field]))
        setattr(booking, field, data[field])
    booking.customer_id = customer.id
    print("jasdeep booking made")
    return booking
