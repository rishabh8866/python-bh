from app import app, db
from datetime import datetime
import constants
from app.rental.enums import CountryEnum, StateEnum
from app.guest.enum import NationalityEnum, LanguageEnum

class Guest(db.Model):
    __tablename__ = "guest"
    id                  =db.Column          (db.Integer, primary_key = True)
    _name               =db.Column          (db.String(250), nullable = False)
    _email_id           =db.Column          (db.String(250), nullable = False)
    _secondary_email_id =db.Column          (db.String(250))
    _phone_no           =db.Column          (db.String(20), nullable = False)
    _country            =db.Column          (db.String(150))
    _address            =db.Column          (db.Text)
    _postal_code        =db.Column          (db.String(20))
    _state              =db.Column          (db.String(150))
    _nationality        =db.Column          (db.String(150))
    _language           =db.Column          (db.String(150))
    _notes              =db.Column          (db.Text)
    _customer_id        =db.Column          (db.Integer, db.ForeignKey('customer.id'), nullable = False)
    _bookings           =db.relationship    ("Booking", secondary = "guest_bookings", backref = db.backref("guests", lazy = "dynamic"))

    def __init__(self, **kwargs):
        self._name = kwargs["name"]
        self._email_id  = kwargs["email_id"]
        self._phone_no  = kwargs["phone_no"]

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name = val

    @property
    def email_id(self):
        return self._email_id

    @email_id.setter
    def email_id(self, val):
        self._email_id = val

    @property
    def secondary_email_id(self):
        return self._secondary_email_id

    @secondary_email_id.setter
    def secondary_email_id(self, val):
        self._secondary_email_id = val

    @property
    def phone_no(self):
        return self._phone_no

    @phone_no.setter
    def phone_no(self, val):
        self._phone_no = val

    @property
    def country(self):
        return self._country

    @country.setter
    def country(self, val):
        self._country = val

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, val):
        self._address = val

    @property
    def postal_code(self):
        return self._postal_code

    @postal_code.setter
    def postal_code(self, val):
        self._postal_code = val

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, val):
        self._state = val

    @property
    def nationality(self):
        return self._nationality

    @nationality.setter
    def nationality(self, val):
        self._nationality = val

    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, val):
        self._language = val

    @property
    def notes(self):
        return self._notes

    @notes.setter
    def notes(self, val):
        self._notes = val

    @property
    def bookings(self):
        return self._bookings

    @bookings.setter
    def bookings(self, val):
        self._bookings = val

    @property
    def customer_id(self):
        return self._customer_id

    @customer_id.setter
    def customer_id(self, val):
        self._customer_id = val

    def half_serialize(self):
        return {
            "name": self._name,
            "email_id": self._email_id,
            "phone_no": self._phone_no,
        }

    def full_serialize(self):
        return dict(self.half_serialize(), **{
            "secondary_email_id": self.secondary_email_id,
            "address": self.address,
            "postal_code": self.postal_code,
            "notes": self.notes
        })

guest_bookings = db.Table("guest_bookings",
        db.Column("guest_id", db.Integer, db.ForeignKey("guest.id")),
        db.Column("booking_id", db.Integer, db.ForeignKey("booking.id"))
        )
