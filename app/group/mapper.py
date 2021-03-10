from app.group.model import Group


mapFields = {
    "id": "group_id",
    "groupName": "groupName",
    "color": "color",
}

def get_obj_from_request(apiData, customer):
    data = {}
    for x in apiData:
      data[mapFields[x]] = apiData[x]
    print("Jasdeep in mapping: " + str(data) + " " + str(customer.id))
    group = Group(name = data["groupName"], color = data["color"], customer_id = customer.id)
    return group

def update_obj_from_request(apiData):
    data = {}
    for x in apiData:
      data[mapFields[x]] = apiData[x]
    print(data["group_id"])
    group = Group.query.get(int(data["group_id"]))
    print(group)
    if "name" in data:
        group.name = data["groupName"]
    if "color" in data:
        group.color = data["color"]
    return group
