from app.booking.model import Booking

fields = {
    "primary": ["no_of_adults", "price", "tax", "rental_id"],
    "secondary": ["no_of_guests","no_of_children", "check_in_time", "check_out_time", "payment_status", "source", "arrive", "depart","booking_type","title","status","color","nights","notes"],
    "unique": []
}


mapFields = {
    "noOfAdults": "no_of_adults",
    "noOfGuests": "no_of_guests",
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
    "bookingType":"booking_type",
    "title":"title",
    "status":"status",
    "color":"color",
    "nights":"nights",
    "notes":"notes"
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
            print("exceptionssssss")
            raise Exception(field + " ought to be unique")
    booking = Booking()
    for field in data.keys():
        if not field in fields["secondary"] and not field in fields["primary"]:
            print(field + " field is not necessary")
            continue
        setattr(booking, field, data[field])
    booking.customer_id = customer.id
    print(booking)
    return booking



def get_response_object(data):
    return data

# def get_obj_from_request(apiData,current_email):
#     print("GET",current_email)
#     # assume data is json
#     data = {}
#     for x in apiData:
#       data[mapFields[x]] = apiData[x]
#     for field in fields["primary"]:
#         if field not in data.keys():
#             raise Exception(field + " not present")
#     for field in fields["unique"]:
#         if getattr(Booking, "check_" + field)(data[field]):
#             raise Exception(field + " ought to be unique")
#     customer = Booking(current_email, name = data["name"])
#     for field in data.keys():
#         if not field in fields["secondary"] and not field in fields["primary"]:
#             print(field + " field is not necessary")
#             continue
#         print("Jasdeep setting " + field + " " + str(data[field]))
#         setattr(customer, field, data[field])
#     print("jasdeep booking made")
#     return customer
