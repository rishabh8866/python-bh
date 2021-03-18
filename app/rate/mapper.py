from app.rate.model import Rate
from app.group.model import Group

fields = {
    "primary": ["week_days", "daily_rate", "minimum_stay_requirement"],
    "secondary": ["guest_per_night", "usd_per_guest", "allow_discount", "weekly_discount","monthly_discount","allow_fixed_rate","week_price","monthly_price"],
    "unique": []
}


mapFields = {
    "rentalId":"rental_id",
    "dateRange": "date_range",
    "minimumStayRequirement": "minimum_stay_requirement",
    "weekDays": "week_days",
    "dailyRate": "daily_rate",
    "guestPerNight": "guest_per_night",
    "allowDiscount": "allow_discount",
    "weeklyDiscount": "weekly_discount",
    "monthlyDiscount":"allow_fixed_rate",
    "allowFixedRate":"allowFixedRate",
    "weekPrice":"week_price",
    "monthlyPrice":"monthly_price",
    "groupId": "group_id",
}

fieldToMap= {
    "rental_id":"rentalId",
    "date_range": "dateRange",
    "minimum_stay_requirement": "minimumStayRequirement",
    "week_days": "weekDays",
    "daily_rate": "dailyRate",
    "guest_per_night": "guestPerNight",
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
    rate = Rate(week_days = data["week_days"], daily_rate = data["daily_rate"], minimum_stay_requirement = "minimum_stay_requirement")
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
    print("jasdeep rental made")
    return rate

def update_obj_from_request(apiData):
    data = {}
    for x in apiData:
      data[mapFields[x]] = apiData[x]
    for field in fields["unique"]:
        if getattr(Rental, "check_" + field)(data[field]):
            raise Exception(field + " ought to be unique")
    rental = Rental.query.get(int(data["rental_id"]))
    for field in data.keys():
        if not field in fields["secondary"] and not field in fields["primary"]:
            print(field + " field is not necessary")
            continue
        print("Jasdeep setting " + field + " " + str(data[field]))
        setattr(rental, field, data[field])
    if "group_id" in data:
        gp_id = int(data["group_id"])
        gp = Group.query.get(gp_id)
        if gp:
            rental.group_id = gp_id
    return rental

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
    
