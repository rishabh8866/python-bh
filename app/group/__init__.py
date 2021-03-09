from flask import Blueprint

group = Blueprint("group", __name__)

import app.group.model, app.group.views
