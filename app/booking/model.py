from app import app, db
from app.booking.enum import PaymentEnum, SourceEnum
import datetime

class Booking(db.Model):
    __tablename__ = "booking"
    id                   =db.Column      (db.Integer, primary_key = True)
    _title               =db.Column      (db.String(50), nullable = True)
    _no_of_adults        =db.Column      (db.Integer, nullable = False)
    _no_of_children      =db.Column      (db.Integer, nullable = False)
    _no_of_guests        =db.Column      (db.Integer, nullable = False)
    _arrive              =db.Column      (db.String(50), nullable = True)
    _depart              =db.Column      (db.String(50), nullable = True)
    _check_in_time       =db.Column      (db.String(150))
    _check_out_time      =db.Column      (db.String(150))
    _payment_status      =db.Column      (db.Enum(PaymentEnum), nullable = False)
    _source              =db.Column      (db.Enum(SourceEnum), nullable = False)
    _price               =db.Column      (db.Integer, nullable = False)
    _booking_type        =db.Column      (db.String(150))
    _status              =db.Column      (db.String(150))
    _color               =db.Column      (db.String(150))
    _tax                 =db.Column      (db.Integer, nullable = False)
    _rental_id           =db.Column      (db.Integer, db.ForeignKey('rental.id',ondelete='CASCADE'))
    _customer_id         =db.Column      (db.Integer, db.ForeignKey('customer.id', ondelete='CASCADE'))
    

    def __init__(self):
        self._payment_status = PaymentEnum.PARTIALLY_PAID
        self._no_of_children = 0
        self._source = SourceEnum.BEEHAZ

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, val):
        self._title = val

    @property
    def no_of_guests(self):
        return self._no_of_guests

    @no_of_guests.setter
    def no_of_guests(self, val):
        self._no_of_guests = val

    @property
    def booking_type(self):
        return self._booking_type

    @booking_type.setter
    def booking_type(self, val):
        self._booking_type = val

    @property
    def no_of_adults(self):
        return self._no_of_adults

    @no_of_adults.setter
    def no_of_adults(self, val):
        self._no_of_adults = val

    @property
    def no_of_children(self):
        return self._no_of_children

    @no_of_children.setter
    def no_of_children(self, val):
        self._no_of_children = val

    @property
    def check_in_time(self):
        return self._check_in_time

    @check_in_time.setter
    def check_in_time(self, val):
        self._check_in_time = val

    @property
    def check_out_time(self):
        return self._check_out_time

    @check_out_time.setter
    def check_out_time(self, val):
        self._check_out_time = val

    @property
    def payment_status(self):
        return self._payment_status

    @payment_status.setter
    def payment_status(self, val):
        self._payment_status = val

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, val):
        self._status = val

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, val):
        self._color = val

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, val):
        self._source = val

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, val):
        self._price = val

    @property
    def tax(self):
        return self._tax

    @tax.setter
    def tax(self, val):
        self._tax = val

    @property
    def arrive(self):
        return self._arrive

    @arrive.setter
    def arrive(self, val):
        self._arrive = val
    
    @property
    def depart(self):
        return self._depart

    @depart.setter
    def depart(self, val):
        self._depart = val

    @property
    def rental_id(self):
        return self._rental_id

    @rental_id.setter
    def rental_id(self, val):
        self._rental_id = val

    @property
    def customer_id(self):
        return self._customer_id

    @customer_id.setter
    def customer_id(self, val):
        self._customer_id = val

    def half_serialize(self):
        return {
            "noOfAdults": self.no_of_adults,
            "noOfChildren": self.no_of_children,
        }

    def full_serialize(self):
        return dict(self.half_serialize(), **{
            "title":self.title,
            "bookingType":self.booking_type,
            "price": self.price,
            "tax": self.tax,
            "checkInTime":self.check_in_time,
            "checkOutTime":self.check_out_time,
            "source":self.source,
            "rentalId":self.rental_id,
            "arrive":self.arrive,
            "depart":self.depart,
            "id":self.id,
            "color":self.color,
            "status":self.status
        })
