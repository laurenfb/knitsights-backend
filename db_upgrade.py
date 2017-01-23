#!flask/bin/python
from migrate.versioning import api
from app.config import SQLALCHEMY_DATABASE_URI
from app.config import SQLALCHEMY_MIGRATE_REPO
api.upgrade(DATABASE_URL, SQLALCHEMY_MIGRATE_REPO)
v = api.db_version(DATABASE_URL, SQLALCHEMY_MIGRATE_REPO)
print('Current database version: ' + str(v))
