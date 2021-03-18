from flask import Blueprint

rate = Blueprint("rate", __name__)

import app.rate.model, app.rate.views
