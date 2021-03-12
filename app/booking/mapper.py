from app.booking.model import Booking

fields = {
    "primary": ["no_of_adults", "price", "tax", "rental_id"],
    "secondary": ["no_of_children", "check_in_time", "check_out_time", "payment_status", "source", "arrive", "depart"],
    "unique": []
}


mapFields = {
    "noOfGuests":"_no_of_guests",
    "noOfAdults": "no_of_adults",
    "price": "price",
    "tax": "tax",
    "rentalId": "rental_id",
    "noOfChildren": "no_of_children",
    "checkInTime": "check_in_time",
    "checkOutTime": "check_out_time",
    "paymentStatus": "payment_status",
    "source": "source",
    "arrive": "arrive",
    "depart": "depart",
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
    booking = Booking()
    for field in data.keys():
        if not field in fields["secondary"] and not field in fields["primary"]:
            print(field + " field is not necessary")
            continue
        print("Jasdeep setting " + field + " " + str(data[field]))
        setattr(booking, field, data[field])
    booking.customer_id = customer.id
    print("jasdeep booking made")
    print(booking)
    return booking
