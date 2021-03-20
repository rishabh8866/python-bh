from flask import Blueprint

fee = Blueprint("fee", __name__)

import app.fee.model, app.fee.views
