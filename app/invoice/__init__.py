from flask import Blueprint

invoice = Blueprint("invoice", __name__)

import app.invoice.views,app.invoice.model
