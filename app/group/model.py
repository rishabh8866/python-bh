from app import app, db

class Group(db.Model):
    __tablename__ = "group"
    id                  =db.Column      (db.Integer, primary_key = True)
    _name               =db.Column      (db.String(250), nullable = False)
    _color              =db.Column      (db.String(10), nullable = False)
    _customer_id        =db.Column      (db.Integer, db.ForeignKey('customer.id', ondelete='CASCADE'), nullable = False)

    def __init__(self, **kwargs):
        self._name = kwargs["name"]
        self._color = kwargs["color"]
        self._customer_id = kwargs["customer_id"]

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name = val

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, val):
        self._color = val

    def half_serialize(self):
        return {
                "id": self.id,
                "groupName": self.name,
                "color": self.color,
                "cusid":self._customer_id
                }

    def full_serialize(self):
        return self.half_serialize()
