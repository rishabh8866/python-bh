from flask import Blueprint

booking = Blueprint("booking", __name__)

import app.booking.model, app.booking.views
