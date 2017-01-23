from flask import Flask, jsonify, abort, make_response, request
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
import os

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
auth = HTTPBasicAuth()

import models
from ravelry_api_wrapper import *
from db_interfacer import *
from config import USERNAME, PASSWORD

def add_headers(origin, response):
    # print origin
    if origin[-1] == "/":
        origin = origin[:-1]
        # print origin
    if origin in ACCEPTABLE_ORIGINS:
        # if origin ==
        response.headers['Access-Control-Allow-Origin'] = origin
    else:
        response = make_response(jsonify({'error': 'unauthorized access'}), 401)
    return response

def get_origin(request):
    if 'HTTP_ORIGIN' in request.environ:
        origin = request.environ['HTTP_ORIGIN']
    else:
        origin = 'http://localhost:8081'
    return origin

@auth.get_password
def get_password(username):
    if username == USERNAME:
        return PASSWORD
    return None

@auth.error_handler
def unauthorized():
    origin = request.environ['HTTP_ORIGIN']
    response = make_response(jsonify({'error': 'unauthorized access'}), 401)
    return add_headers(origin, response)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/api/projects/<username>', methods=['GET'])
# @auth.login_required
def get_projects(username):
    origin = get_origin(request)
    projects = APIWrapper.import_user(username)
    if type(projects) is int:
        # will return error code if there is one, so we'll use the flask error handler here.
        abort(projects)
    response = make_response(jsonify(projects))
    return add_headers(origin, response)

@app.route('/api/projects/<username>', methods=['PUT'])
def update_projects(username):
    user = User.query.filter_by(name = username).first()
    origin = get_origin(request)
    if user is None:
        response = make_response(jsonify({'error': 'resource not found'}), 404)
    else:
        response = DBInterfacer.take_in_projects(request)
        response = make_response(jsonify(response), 200)
    return add_headers(origin, response)

@app.route('/api/project/<username>/delete', methods=['DELETE'])
def delete_project(username):
    user = User.query.filter_by(name = username).first()
    origin = get_origin(request)
    if user is None:
        response = make_response(jsonify({'error': 'resource not found'}), 404)
    else:
        response = DBInterfacer.archive_project(request.get_json())
    # again there's surely a better way to do this, but TOO LATE
    if isinstance(response, int):
        abort(response)
    else:
        response = make_response(jsonify(response), 200)
    return add_headers(origin, response)

@app.errorhandler(404)
def not_found(error):
    origin = get_origin(request)
    response = make_response(jsonify({'error': 'resource not found'}), 404)
    return add_headers(origin, response)
