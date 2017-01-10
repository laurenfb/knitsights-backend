from flask import Flask, jsonify, abort, make_response
from ravelry_api_wrapper import *
from config import USERNAME, PASSWORD
from flask.ext.httpauth import HTTPBasicAuth


app = Flask(__name__)
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == USERNAME:
        return PASSWORD
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'unauthorized access'}), 401)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/api/get_projects/<username>', methods=['GET'])
@auth.login_required
def get_projects(username):
    projects = APIWrapper.get_current_user_projects(username)
    if type(projects) is int:
        # will return error code if there is one, so we'll use the flask error handler here.
        abort(projects)
    return jsonify(projects)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)


if __name__ == '__main__':
    app.run(debug=True) # this will be false on production
