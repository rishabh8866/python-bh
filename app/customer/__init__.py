from flask import Blueprint

customer = Blueprint("customer", __name__)

import app.customer.model, app.customer.views
