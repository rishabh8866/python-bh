from app.rate.model import Rate
from app.group.model import Group
from app.rental.model import Rental

fields = {
    "primary": ["week_days", "daily_rate", "minimum_stay_requirement"],
    "secondary": ["date_range","guest_per_night", "usd_per_guest", "allow_discount", "weekly_discount","monthly_discount","allow_fixed_rate","week_price","monthly_price"],
    "unique": []
}

mapFields = {
    "id":"rate_id",
    "rentalId":"rental_id",
    "dateRange": "date_range",
    "minimumStayRequirement": "minimum_stay_requirement",
    "weekDays": "week_days",
    "dailyRate": "daily_rate",
    "guestPerNight": "guest_per_night",
    "usdPerGuest": "usd_per_guest",
    "allowDiscount": "allow_discount",
    "weeklyDiscount": "weekly_discount",
    "monthlyDiscount":"monthly_discount",
    "allowFixedRate":"allow_fixed_rate",
    "weekPrice":"week_price",
    "monthlyPrice":"monthly_price",
    "groupId": "group_id",
}

fieldToMap= {
    "rate_id":"rateId",
    "rental_id":"rentalId",
    "group_id": "groupId",
    "date_range": "dateRange",
    "minimum_stay_requirement": "minimumStayRequirement",
    "week_days": "weekDays",
    "daily_rate": "dailyRate",
    "guest_per_night": "guestPerNight",
    "usd_per_guest":"usdPerGuest",
    "allow_discount": "allowDiscount",
    "weekly_discount": "weeklyDiscount",
    "monthly_discount": "monthlyDiscount",
    "allow_fixed_rate": "allowFixedRate",
    "week_price": "weekPrice",
    "monthly_price":"monthlyPrice",
    "id": "id",
}


def get_obj_from_request(apiData, customer):
    data = {}
    for x in apiData:
      data[mapFields[x]] = apiData[x]
    for field in fields["primary"]:
        if field not in data.keys():
            raise Exception(field + " not present")
    for field in fields["unique"]:
        if getattr(Rate, "check_" + field)(data[field]):
            raise Exception(field + " ought to be unique")
    rate = Rate(rental_id=data['rental_id'],usd_per_guest=1, date_range="", minimum_stay_requirement=10, week_days="MON", daily_rate="", guest_per_night=2,
                                    allow_discount=False, weekly_discount=0, monthly_discount=0, allow_fixed_rate=False, week_price=0, monthly_price=0, customer_id=customer.id,group_id=None)
    for field in data.keys():
        if not field in fields["secondary"] and not field in fields["primary"]:
            print(field + " field is not necessary")
            continue
        print("Jasdeep setting " + field + " " + str(data[field]))
        setattr(rate, field, data[field])
    rate.customer_id = customer.id
    if "group_id" in data:
        gp_id = int(data["group_id"])
        gp = Group.query.get(gp_id)
        if gp:
            rate.group_id = gp_id
    if "rental_id" in data:
        r_id = int(data["rental_id"])
        rid = Rental.query.get(r_id)
        if rid:
            rate.rental_id = r_id
    return rate

def update_obj_from_request(apiData):
    data = {}
    for x in apiData:
      data[mapFields[x]] = apiData[x]
    for field in fields["unique"]:
        if getattr(Rate, "check_" + field)(data[field]):
            raise Exception(field + " ought to be unique")
    rate = Rate.query.get(int(data["rate_id"]))
    for field in data.keys():
        if not field in fields["secondary"] and not field in fields["primary"]:
            print(field + " field is not necessary")
            continue
        print("Jasdeep setting " + field + " " + str(data[field]))
        setattr(rate, field, data[field])
    if "group_id" in data:
        gp_id = int(data["group_id"])
        gp = Group.query.get(gp_id)
        if gp:
            rate.group_id = gp_id
    if "rate_id" in data:
        r_id = int(data["rate_id"])
        rid = Rate.query.get(r_id)
        if rid:
            rate.rate_id = r_id
    return rate

def get_response_object(data):
    apiData = {}
    groupName = ""
    if "group_id" in data:
        if not (data["group_id"] is None):
            gp_id = int(data["group_id"])
            gp = Group.query.get(gp_id)
            if gp:
                groupName = gp.name
    for x in data:
        apiData[fieldToMap[x]] = data[x]
    apiData["groupName"]  = groupName   
    return apiData  
    
