from flask import Blueprint

tax = Blueprint("tax", __name__)

import app.tax.model, app.tax.views
