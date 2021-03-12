from flask import Blueprint

rental = Blueprint("rental", __name__)

import app.rental.model, app.rental.views
