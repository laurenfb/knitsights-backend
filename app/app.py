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
from config import USERNAME, PASSWORD

def add_headers(referer, response):
    print referer
    if referer[-1] == "/":
        referer = referer[:-1]
        print referer
    if referer in ACCEPTABLE_REFERERS:
        response.headers['Access-Control-Allow-Origin'] = referer
    else:
        response = make_response(jsonify({'error': 'unauthorized access'}), 401)
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
    if 'HTTP_REFERER' in request.environ:
        print "it's in!"
        referer = request.environ['HTTP_REFERER']
    else:
        print "hi it's not in"
        referer = 'http://localhost:8081'
    projects = APIWrapper.import_user(username)
    if type(projects) is int:
        # will return error code if there is one, so we'll use the flask error handler here.
        abort(projects)
    response = make_response(jsonify(projects))
    return add_headers(referer, response)

@app.errorhandler(404)
def not_found(error):
    response = make_response(jsonify({'error': 'Not Found'}), 404)
    return add_headers(response)
