from flask import Flask, jsonify, abort, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
import os

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
auth = HTTPBasicAuth()

import models
from ravelry_api_wrapper import *
from config import USERNAME, PASSWORD

def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'https://laurenfb.github.io'
    return response

@auth.get_password
def get_password(username):
    if username == USERNAME:
        return PASSWORD
    return None

@auth.error_handler
def unauthorized():
    response = make_response(jsonify({'error': 'unauthorized access'}), 401)
    return add_headers(response)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/api/get_projects/<username>', methods=['GET'])
# @auth.login_required
def get_projects(username):
    projects = APIWrapper.import_user(username)
    if type(projects) is int:
        # will return error code if there is one, so we'll use the flask error handler here.
        abort(projects)
    response = make_response(jsonify(projects))
    return add_headers(response)

@app.errorhandler(404)
def not_found(error):
    response = make_response(jsonify({'error': 'Not Found'}), 404)
    return add_headers(response)

#
# if __name__ == '__main__':
#     app.run(debug=True) # this will be false on production
