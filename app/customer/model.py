from app import app, db
from datetime import datetime
from app.customer.enums import PropertyEnum, CurrencyEnum, TimeDisplayEnum, DateDisplayEnum, TypeEnum, NumberDisplayEnum
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
import constants
import enum

class Customer(db.Model):
    __tablename__ = "customer"
    id                  =db.Column      (db.Integer, primary_key = True)
    _email_id           =db.Column      (db.String(250), unique = True, index = True, nullable = False)
    _first_name         =db.Column      (db.String(150))
    _last_name          =db.Column      (db.String(150))
    _property_type      =db.Column      (db.String(150))
    _number_of_rooms    =db.Column      (db.Integer)
    _name               =db.Column      (db.Text)
    _website            =db.Column      (db.Text)
    _created_at         =db.Column      (db.DateTime())
    _currency           =db.Column      (db.String(25))
    _time_display       =db.Column      (db.Enum(TimeDisplayEnum))
    _date_display       =db.Column      (db.Enum(DateDisplayEnum))
    _customer_type      =db.Column      (db.Enum(TypeEnum))
    _number_display     =db.Column      (db.Enum(NumberDisplayEnum))
    _language           =db.Column      (db.String(250))
    _permissions        =db.Column      (db.String(250),default="user")
    _is_future_booking  =db.Column      (db.Boolean,default=False)
    _allow_booking_for  =db.Column     (db.String(250))
    _account_type       =db.Column     (db.String(250))
    rentals             =db.relationship('Rental', backref='customer', lazy=True)


    def __init__(self, email_id, **kwargs):
        self._email_id = email_id
        if "name" in kwargs:
            self._name = kwargs["name"]
        self._created_at = datetime.utcnow()

    @property
    def email_id(self):
        return self._email_id

    @email_id.setter
    def email_id(self, val):
        self._email_id = val
    
    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, val):
        self._first_name = val
    
    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, val):
        self._last_name = val

    @property
    def property_type(self):
        return self._property_type

    @property_type.setter
    def property_type(self, val):
        self._property_type = val

    @property
    def number_of_rooms(self):
        return self._number_of_rooms

    @number_of_rooms.setter
    def number_of_rooms(self, val):
        self._number_of_rooms = val

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name = val

    @property
    def website(self):
        return self._website

    @website.setter
    def website(self, val):
        self._website = val

    @property
    def currency(self):
        return self._currency

    @currency.setter
    def currency(self, val):
        self._currency = val

    @property
    def time_display(self):
        return self._time_display

    @time_display.setter
    def time_display(self, val):
        self._time_display = val

    @property
    def date_display(self):
        return self._date_display

    @date_display.setter
    def date_display(self, val):
        self._date_display = val

    @property
    def customer_type(self):
        return self._customer_type

    @customer_type.setter
    def customer_type(self, val):
        self._customer_type = val

    @property
    def number_display(self):
        return self._number_display

    @number_display.setter
    def number_display(self, val):
        self._number_display = val


    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, val):
        self._language = val

    @property
    def permissions(self):
        return self._permissions

    @permissions.setter
    def permissions(self, val):
        self._permissions = val

    @property
    def is_future_booking(self):
        return self._is_future_booking

    @permissions.setter
    def is_future_booking(self, val):
        self._is_future_booking = val

    @property
    def allow_booking_for(self):
        return self._allow_booking_for

    @allow_booking_for.setter
    def allow_booking_for(self, val):
        self._allow_booking_for = val

    @property
    def account_type(self):
        return self._account_type

    @account_type.setter
    def account_type(self, val):
        self._account_type = val
    
    def generate_auth_token(self):
        serial_token = Serializer(app.config[constants.SECRET_KEY], expires_in = constants.MS.MONTH)
        return serial_token.dumps({"id": self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config[constants.SECRET_KEY])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        customer = Customer.query.get(data["id"])
        return customer

    @staticmethod
    def check_email_id(val):
        return Customer.query.filter(Customer.email_id == val).count() != 0

    def half_serialize(self):
        return {
            "email_id": self.email_id,
            "name": self.name,
            "number_of_rooms": self.number_of_rooms,
            "customer_type": self.customer_type,
            "created_at": self._created_at,
            "language": self.language,
            "permissions":self.permissions,
            "is_future_booking":self._is_future_booking,
            "allow_booking_for":self.allow_booking_for,
            "account_type":self.account_type
        }

    def full_serialize(self):
        return dict(self.half_serialize(), **{
            "number_display": self.number_display,
            "date_display": self.date_display,
            "time_display": self.time_display,
            "website": self.website,
            "currency": self.currency
        })

    def __repr__(self):
        return "Customer: %s %s"%(self._email_id, self._name)
