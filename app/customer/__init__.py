from flask import Blueprint

customer = Blueprint("customer_blueprint", __name__)

import app.customer.model, app.customer.views
