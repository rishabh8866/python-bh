from app import app, db
import json
from datetime import date


class Subscriber(db.Model):
    __tablename__ = "subscriber"
    id                          =db.Column(db.Integer, primary_key = True)
    _first_name                 =db.Column(db.String(150))
    _email_id                   =db.Column(db.String(250), unique = True, index = True, nullable = False)
    _status                     =db.Column(db.String(150))
    _date                       =db.Column(db.String(150),default=date.today())

    def __init__(self,**kwargs):
        self._email_id = kwargs['_email_id']
        self._first_name = kwargs['_first_name']
        self._status = "Active"

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, val):
        self._first_name = val
    
    @property
    def email_id(self):
        return self._email_id

    @email_id.setter
    def email_id(self, val):
        self._email_id = val


    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, val):
        self._status = val

    def full_serialize(self):
        return {
            "id":self.id,
            "email_id": self._email_id,                
            "firstName": self._first_name,                   
            "status":self._status            
        }