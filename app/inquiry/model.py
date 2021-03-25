from app import app, db
from app.rate.enums import WeekdaysEnum
import json

class Tax(db.Model):
    __tablename__ = "tax"
    id                         =db.Column      (db.Integer, primary_key = True)
    _customer_id               =db.Column      (db.Integer, db.ForeignKey('customer.id'), nullable = False)
    _rental_id                 =db.Column      (db.Integer, db.ForeignKey('rental.id'),nullable=False)
    _group_id                  =db.Column      (db.Integer, db.ForeignKey('group.id'),nullable=True)
    _name                      =db.Column      (db.String(150))
    _fee_type                  =db.Column      (db.String(150))
    _amount                    =db.Column      (db.Integer)     
    

    def __init__(self, **kwargs):
        self._week_days = kwargs["name"]
        self._daily_rate = kwargs["fee_type"]

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name = val
        
    @property
    def fee_type(self):
        return self._fee_type

    @fee_type.setter
    def fee_type(self, val):
        self._fee_type = val
    
    
    @property
    def amount(self):
        return self._amount

    @fee_type.setter
    def amount(self, val):
        self._amount = val
    

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
    def rental_id(self):
        return self._rental_id

    @rental_id.setter
    def rental_id(self, val):
        self._rental_id = val


    def full_serialize(self):
        return {
            "customer_id"   : self._customer_id, 
            "rental_id"  : self._rental_id,                      
            "name"     : self._name,                   
            "fee_type" : self._fee_type,
            "amount"     : self._amount,                            
        }
		