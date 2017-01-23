from config import *
from app import db
from models import *

class DBInterfacer:
    @staticmethod
    def take_in_projects(request):
        return {'hi': 'this is totally a json'}

    @staticmethod
    def archive_project(project):
        # find the project
        project = Project.query.filter_by(id = project['id']).first()
        # 404 if it's not there
        if project is None:
            response = 404
        else:
            project.archived = True
            db.session.add(project)
            db.session.commit()
            response = {'success': project.name + ' archived'}
        return response
