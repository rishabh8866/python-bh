from flask import jsonify, render_template
from app import app, utils
import constants

@app.route("/")
def index():
    return render_template('index.html')
@app.errorhandler(404)   
def not_found(e):   
  return render_template('index.html')

@app.errorhandler(Exception)
def all_exception_handler(error):
    if not error:
        error = "empty"
    app.logger.error(error)
    utils.send_message_to_slack(error, "server_exception")
    return 'Error', 500
# @app.route("/", methods=["GET"])
# def index():
#     return render_template('index.html')

@app.route('/api/docs')
def get_docs():
    print('sending docs')
    return render_template('swaggerui.html')

@app.route("/raiseTestException", methods=["GET"])
def raiseTestException():
    raise Exception("exception")

@app.route('/api/world')
def get_world():
    return app.send_static_file('./world.json')

def bad_request(data):
    return jsonify({"msg": constants.view_constants.BAD_REQUEST, "data": data}), 400

def internal_error(data):
    return jsonify({"msg": constants.view_constants.INTERNAL_ERROR, "data": data}), 500

def as_success(data):
    return jsonify({"msg": constants.view_constants.SUCCESS, "data": data}), 200

def not_authenticated(data):
    return jsonify({"msg": constants.view_constants.NOT_AUTHENTICATED, "data": data}), 403
