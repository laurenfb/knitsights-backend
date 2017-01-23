from config import *
from app import db
from models import *

class DBInterfacer:
    @staticmethod
    def take_in_projects(request):
        return {'hi': 'this is totally a json'}

    @staticmethod
    def archive_project(project):
        print project['name']
        project = Project.query.filter_by(id = project['id']).first()
        if project is None:
            response = 404
        else:
            return {'hi': 'success!'}
        return response
