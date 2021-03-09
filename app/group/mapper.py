from app.group.model import Group

def get_obj_from_request(data, customer):
    print("Jasdeep in mapping: " + str(data) + " " + str(customer.id))
    group = Group(name = data["name"], color = data["color"], customer_id = customer.id)
    return group

def update_obj_from_request(data):
    group = Group.query.get(int(data["group_id"]))
    if "name" in data:
        group.name = data["name"]
    if "color" in data:
        group.color = data["color"]
    return group
