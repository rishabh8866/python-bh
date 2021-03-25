from flask import Blueprint

inquiry = Blueprint("inquiry", __name__)

import app.inquiry.views
