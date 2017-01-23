from config import *
from app import db
from models import *

class DBInterfacer:
    @staticmethod
    def take_in_projects(request):
        return {'hi': 'this is totally a json'}

    @staticmethod
    def archive_project(project):
        return {'hi': 'success!'}
