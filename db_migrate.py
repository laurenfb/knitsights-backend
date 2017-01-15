#!flask/bin/python
import imp
from migrate.versioning import api
from app.app import db
from app.config import DATABASE_URL
from app.config import SQLALCHEMY_MIGRATE_REPO
v = api.db_version(DATABASE_URL, SQLALCHEMY_MIGRATE_REPO)
migration = SQLALCHEMY_MIGRATE_REPO + ('/versions/%03d_migration.py' % (v+1))
tmp_module = imp.new_module('old_model')
old_model = api.create_model(DATABASE_URL, SQLALCHEMY_MIGRATE_REPO)
exec(old_model, tmp_module.__dict__)
script = api.make_update_script_for_model(DATABASE_URL, SQLALCHEMY_MIGRATE_REPO, tmp_module.meta, db.metadata)
open(migration, "wt").write(script)
api.upgrade(DATABASE_URL, SQLALCHEMY_MIGRATE_REPO)
v = api.db_version(DATABASE_URL, SQLALCHEMY_MIGRATE_REPO)
print('New migration saved as ' + migration)
print('Current database version: ' + str(v))
