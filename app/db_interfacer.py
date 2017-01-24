from config import *
from app import db
from models import Project, Cluster
from flask import request

class DBInterfacer:
    @staticmethod
    def take_in_projects(request):
        projects = request.get_json()['projects']
        changed_projects = []
        for project in projects:
            p = Project.query.filter_by(id = project['id']).first()
            if p is not None:
                p.cluster_id = project['clusterID']
                changed_projects.append(p)
                db.session.add(p)
        db.session.commit()
        # print changed_projects
        return {'success': [project.as_dict() for project in changed_projects]}

    @staticmethod
    def archive_project(project):
        project_object = Project.query.filter_by(id = project['id']).first()
        # 404 if it's not there
        if project_object is None:
            response = 404
        else:
            project_object.archived = True
            db.session.add(project_object)
            db.session.commit()
            response = {'success': project_object.name + ' archived'}
        return response

    @staticmethod
    def mark_imported(user):
        user.imported = True
        db.session.add(user)
        db.session.commit()
        return {'success': user.name + ' imported'}
