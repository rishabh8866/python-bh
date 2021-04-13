from app.subscribers.model import Subscriber



fields = {
    "primary": ["email_id"],
    "secondary": ["first_name"],
    "unique": []
}

mapFields = {
    "id":"id",
    "status":"status",
    "emailId": "email_id",
    "firstName":"first_name",
}

fieldToMap= {
    "id": "id",
    "status":"status",
    "email_id":"emailId",
    "first_name": "firstName",
}


def get_obj_from_request(apiData):
    data = {}
    print(apiData)
    for x in apiData:
      data[mapFields[x]] = apiData[x]
    for field in fields["primary"]:
        if field not in data.keys():
            print(field)
            raise Exception(field + " not present")
    for field in fields["unique"]:
        if getattr(Subscriber, "check_" + field)(data[field]):
            raise Exception(field + " ought to be unique")
    subscriber = Subscriber(_first_name = data["first_name"],_email_id=data['email_id'])
    for field in data.keys():
        if not field in fields["secondary"] and not field in fields["primary"]:
            print(field + " field is not necessary")
            continue
        print("Jasdeep setting " + field + " " + str(data[field]))
        setattr(subscriber, field, data[field])
  
    return subscriber


def get_response_object(data):
    return data  
    
