from app.fee.model import Fee
from app.group.model import Group
from app.rental.model import Rental

fields = {
    "primary": ["name", "fee_type",],
    "secondary": ["amount","modality",],
    "unique": []
}

mapFields = {
    "id":"fee_id",
    "rentalId":"rental_id",
    "groupId": "group_id",
    "name":"name",
    "feeType":"fee_type",
    "amount":"amount",
    "modality":"modality"
}

fieldToMap= {
    "id": "id",
    "fee_id":"feeId",
    "rental_id":"rentalId",
    "group_id": "groupId",
    "name":"name",
    "fee_type":"feeType",
    "amount":"amount",
    "modality":"modality"
}


def get_obj_from_request(apiData, customer):
    data = {}
    for x in apiData:
      data[mapFields[x]] = apiData[x]
    for field in fields["primary"]:
        if field not in data.keys():
            raise Exception(field + " not present")
    for field in fields["unique"]:
        if getattr(Fee, "check_" + field)(data[field]):
            raise Exception(field + " ought to be unique")
    fee = Fee(name = data["name"], fee_type = data["fee_type"])
    for field in data.keys():
        if not field in fields["secondary"] and not field in fields["primary"]:
            print(field + " field is not necessary")
            continue
        print("Jasdeep setting " + field + " " + str(data[field]))
        setattr(fee, field, data[field])
    fee.customer_id = customer.id
    if "group_id" in data:
        gp_id = int(data["group_id"])
        gp = Group.query.get(gp_id)
        if gp:
            fee.group_id = gp_id
    if "rental_id" in data:
        r_id = int(data["rental_id"])
        rid = Rental.query.get(r_id)
        if rid:
            fee.rental_id = r_id
    return fee

def update_obj_from_request(apiData):
    data = {}
    for x in apiData:
      data[mapFields[x]] = apiData[x]
    for field in fields["unique"]:
        if getattr(Fee, "check_" + field)(data[field]):
            raise Exception(field + " ought to be unique")
    fee = Fee.query.get(int(data["fee_id"]))
    for field in data.keys():
        if not field in fields["secondary"] and not field in fields["primary"]:
            print(field + " field is not necessary")
            continue
        print("Jasdeep setting " + field + " " + str(data[field]))
        setattr(fee, field, data[field])
    if "group_id" in data:
        gp_id = int(data["group_id"])
        gp = Group.query.get(gp_id)
        if gp:
            fee.group_id = gp_id
    if "rental_id" in data:
        r_id = int(data["rental_id"])
        rid = Fee.query.get(r_id)
        if rid:
            fee.rental_id = r_id
    return fee

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
    
