from flask import Blueprint

guest = Blueprint("Guest", __name__)

import app.guest.model, app.guest.views
