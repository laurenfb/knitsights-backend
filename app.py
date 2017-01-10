from flask import Flask, jsonify
from ravelry_api_wrapper import *


app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/api/get_projects/<username>', methods=['GET'])
def get_projects(username):
    projects = APIWrapper.get_current_user_projects(username)
    return jsonify(projects)

if __name__ == '__main__':
    app.run(debug=True) # this will be false on production
