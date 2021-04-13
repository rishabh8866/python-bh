from flask import Blueprint

subscribers = Blueprint("subscribers", __name__)

import app.subscribers.model, app.subscribers.views
