from config import *
from app import db
from models import Project, Cluster
from flask import request

class DBInterfacer:
    @staticmethod
    def take_in_projects(request):
        clusters = request.get_json()['clusters']
        changed_projects = []
        for cluster in clusters:
            for p in cluster['projects']:
                project = Project.query.filter_by(id = p['id']).first()
                if project is not None:
                    project.cluster_id = cluster['id']
                    changed_projects.append({"name": project.name, "id": project.id, "cluster_id": project.cluster_id})
                    db.session.add(project)
        db.session.commit()
        return {'success': changed_projects}

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
