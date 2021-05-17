from app import app, db

class Invoice(db.Model):
    __tablename__ = "invoice"
    id                         =db.Column      (db.Integer, primary_key = True)
    _customer_id               =db.Column      (db.Integer, db.ForeignKey('customer.id', ondelete='CASCADE'), nullable = False)
    _name                      =db.Column      (db.String(150))
    _address1                  =db.Column      (db.String(250))
    _address2                  =db.Column      (db.String(250))
    _country_label             =db.Column      (db.String(250))
    _country_value             =db.Column      (db.String(250))
    _invoice_text              =db.Column      (db.String(250))
    _invoice_footer            =db.Column      (db.String(250))


    def __init__(self, **kwargs):
        self._customer_id = kwargs["customer_id"]
        self._name = kwargs["name"]
        
        
    @property
    def name(self):
        return self._name

    @name.setter 
    def name(self, val):
        self._address1 = val
        
    @property
    def address1(self):
        return self._address1

    @address1.setter
    def address1(self, val):
        self._address1 = val
    
    
    @property
    def address2(self):
        return self._address2

    @address2.setter
    def address2(self, val):
        self._address2 = val
    
    @property
    def country_label(self):
        return self._country_label

    @country_label.setter
    def country_label(self, val):
        self._country_label = val

    @property
    def country_value(self):
        return self._country_value

    @country_value.setter
    def country_value(self, val):
        self._country_value = val

    @property
    def invoice_text(self):
        return self._invoice_text

    @invoice_text.setter
    def invoice_text(self, val):
        self._invoice_text = val
    
    @property
    def invoice_footer(self):
        return self._invoice_footer

    @invoice_footer.setter
    def invoice_footer(self, val):
        self._invoice_footer = val

    @property
    def customer_id(self):
        return self._customer_id

    @customer_id.setter
    def customer_id(self, val):
        self._customer_id = val


    def full_serialize(self):
        return {
            "customer_id"   : self._customer_id, 
            "name"  : self.name,                      
            "address1"     : self.address1,                   
            "address2" : self.address2,
            "country_label"     : self.country_label,                            
            "country_value"     : self.country_value,                            
            "invoice_text"     : self.invoice_text,                            
            "invoice_footer"     : self.invoice_footer,                            
        }
		