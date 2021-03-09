from flask import jsonify, render_template, Flask
from app import app
import constants

@app.route("/index", methods=["GET", "POST"])
def index():
    return jsonify({"msg": constants.view_constants.SUCCESS})

@app.route('/api/docs')
def get_docs():
    print('sending docs')
    return render_template('swaggerui.html')

def bad_request(data):
    return jsonify({"msg": constants.view_constants.BAD_REQUEST, "data": data}), 400

def internal_error(data):
    return jsonify({"msg": constants.view_constants.INTERNAL_ERROR, "data": data}), 500

def as_success(data):
    return jsonify({"msg": constants.view_constants.SUCCESS, "data": data}), 200

def not_authenticated(data):
    return jsonify({"msg": constants.view_constants.NOT_AUTHENTICATED, "data": data}), 403
