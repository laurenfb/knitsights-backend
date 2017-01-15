#!flask/bin/python
# from __future__ import absolute_import
from migrate.versioning import api
from app.config import DATABASE_URL
from app.config import SQLALCHEMY_MIGRATE_REPO
from app.app import db
import os.path
db.create_all()
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(DATABASE_URL, SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(DATABASE_URL, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))
