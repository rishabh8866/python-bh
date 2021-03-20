from app import app, db
from app.rate.enums import WeekdaysEnum
import json


class Rate(db.Model):
    __tablename__ = "rate"
    id                         =db.Column      (db.Integer, primary_key = True)
    _date_range                =db.Column      (db.String(150))
    _minimum_stay_requirement  =db.Column      (db.Integer)     
    _week_days                 =db.Column      (db.Enum(WeekdaysEnum))
    _daily_rate                =db.Column      (db.Integer)
    _guest_per_night           =db.Column      (db.Integer)
    _usd_per_guest             =db.Column      (db.Integer)
    _allow_discount            =db.Column      (db.Boolean,default=False)
    _weekly_discount           =db.Column      (db.Integer)
    _monthly_discount          =db.Column      (db.Integer)
    _allow_fixed_rate          =db.Column      (db.Boolean,default=False)
    _week_price                =db.Column      (db.Integer)
    _monthly_price             =db.Column      (db.Integer)
    _customer_id               =db.Column      (db.Integer, db.ForeignKey('customer.id'), nullable = False)
    _rental_id                 =db.Column      (db.Integer, db.ForeignKey('rental.id'),nullable=True)
    _group_id                  =db.Column      (db.Integer, db.ForeignKey('group.id'),nullable=True)

    def __init__(self, **kwargs):
        self._week_days = kwargs["week_days"]
        self._daily_rate = kwargs["daily_rate"]
        self._minimum_stay_requirement = kwargs["minimum_stay_requirement"]

    @property
    def date_range(self):
        return self._date_range

    @date_range.setter
    def date_range(self, val):
        self._date_range = val

    @property
    def minimum_stay_requirement(self):
        return self._minimum_stay_requirement

    @minimum_stay_requirement.setter
    def minimum_stay_requirement(self, val):
        self._minimum_stay_requirement = val

    @property
    def week_days(self):
        return self._week_days

    @week_days.setter
    def week_days(self, val):
        self._week_days = val

    @property
    def daily_rate(self):
        return self._daily_rate

    @daily_rate.setter
    def daily_rate(self, val):
        self._daily_rate = val

    @property
    def guest_per_night(self):
        return self._guest_per_night

    @guest_per_night.setter
    def guest_per_night(self, val):
        self._guest_per_night = val

    @property
    def usd_per_guest(self):
        return self._usd_per_guest

    @usd_per_guest.setter
    def usd_per_guest(self, val):
        self._usd_per_guest = val

    @property
    def allow_discount(self):
        return self._allow_discount

    @allow_discount.setter
    def allow_discount(self, val):
        self._allow_discount = val

    @property
    def weekly_discount(self):
        return self._weekly_discount

    @weekly_discount.setter
    def weekly_discount(self, val):
        self._weekly_discount = val

    @property
    def monthly_discount(self):
        return self._monthly_discount

    @monthly_discount.setter
    def monthly_discount(self, val):
        self._monthly_discount = val

    @property
    def allow_fixed_rate(self):
        return self._allow_fixed_rate

    @allow_fixed_rate.setter
    def allow_fixed_rate(self, val):
        self._allow_fixed_rate = val

    @property
    def week_price(self):
        return self._week_price

    @week_price.setter
    def week_price(self, val):
        self._week_price = val

    @property
    def monthly_price(self):
        return self._monthly_price

    @monthly_price.setter
    def monthly_price(self, val):
        self._monthly_price = val

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
            "date_range": self.date_range,
            "minimum_stay_requirement": self.minimum_stay_requirement,
            # "week_days": self.week_days,
            "daily_rate": self.daily_rate,
            "guest_per_night": self.guest_per_night,
            "usd_per_guest": self.usd_per_guest,
            "allow_discount": self.allow_discount,
            "weekly_discount": self.weekly_discount,
            "monthly_discount": self.monthly_discount,
            "week_price": self.week_price
        }