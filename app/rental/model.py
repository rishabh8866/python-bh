from app import app, db
from app.rental.enums import CountryEnum
import json


class Rental(db.Model):
    __tablename__ = "rental"
    id                   =db.Column      (db.Integer, primary_key = True)
    _name                =db.Column      (db.Text, nullable = False)
    _address_line1       =db.Column      (db.Text, nullable = False)
    _address_line2       =db.Column      (db.Text)
    _postal_code         =db.Column      (db.String(10), nullable = True)
    _city                =db.Column      (db.String(10))
    _country             =db.Column      (db.String(30))
    _currency            =db.Column      (db.String(10))
    _checkin_time       =db.Column      (db.String(30), nullable = False)
    _checkout_time      =db.Column      (db.String(30), nullable = False)
    _max_guests          =db.Column      (db.Integer)
    _customer_id         =db.Column      (db.Integer, db.ForeignKey('customer.id'), nullable = False)
    _group_id            =db.Column      (db.Integer, db.ForeignKey('group.id', ondelete='CASCADE'))

    def __init__(self, **kwargs):
        self._name = kwargs["name"]
        self._address_line1 = kwargs["address_line1"]
        self._postal_code = kwargs["postal_code"]

    @property
    def address_line1(self):
        return self._address_line1

    @address_line1.setter
    def address_line1(self, val):
        self._address_line1 = val

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name = val

    @property
    def address_line2(self):
        return self._address_line2

    @address_line2.setter
    def address_line2(self, val):
        self._address_line2 = val

    @property
    def postal_code(self):
        return self._postal_code

    @postal_code.setter
    def postal_code(self, val):
        self._postal_code = val

    @property
    def city(self):
        return self._city

    @city.setter
    def city(self, val):
        self._city = val

    @property
    def country(self):
        return self._country

    @country.setter
    def country(self, val):
        self._country = val

    @property
    def currency(self):
        return self._currency

    @currency.setter
    def currency(self, val):
        self._currency = val

    @property
    def checkin_time(self):
        return self._checkin_time

    @checkin_time.setter
    def checkin_time(self, val):
        self._checkin_time = val

    @property
    def checkout_time(self):
        return self._checkout_time

    @checkout_time.setter
    def checkout_time(self, val):
        self._checkout_time = val

    @property
    def customer_id(self):
        return self._customer_id

    @customer_id.setter
    def customer_id(self, val):
        self._customer_id = val

    @property
    def group_id(self):
        return self._group_id

    @group_id.setter
    def group_id(self, val):
        self._group_id = val

    @property
    def max_guests(self):
        return self._max_guests

    @max_guests.setter
    def max_guests(self, val):
        self._max_guests = val

    def half_serialize(self):
        return {
            "id": self.id,
            "address_line1": self.address_line1,
            "name": self.name,
            "group_id": self.group_id
        }

    def full_serialize(self):
        return dict(self.half_serialize(), **{
            "address_line2": self.address_line2,
            "postal_code": self.postal_code,
            "checkin_time": self.checkin_time,
            "checkout_time": self.checkout_time,
            "max_guests": self.max_guests,
            "currency": self.currency,
            "country": self.country
        })
