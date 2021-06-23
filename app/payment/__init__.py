from flask import Blueprint

payment_blueprint = Blueprint("payment_blueprint", __name__)

import app.payment.views
