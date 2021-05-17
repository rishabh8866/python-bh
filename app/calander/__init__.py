from flask import Blueprint

calander = Blueprint("calander", __name__)

import app.calander.views
