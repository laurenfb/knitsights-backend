from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
project = Table('project', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=64)),
    Column('photo_url', VARCHAR(length=100)),
    Column('time_in_days', INTEGER),
    Column('user_id', INTEGER),
    Column('cluster_id', INTEGER),
    Column('pattern_id', INTEGER),
    Column('rav_id', INTEGER),
)

user = Table('user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=64)),
    Column('email', VARCHAR),
    Column('photo_url', VARCHAR(length=100)),
    Column('imported', BOOLEAN),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['project'].columns['photo_url'].drop()
    pre_meta.tables['user'].columns['photo_url'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['project'].columns['photo_url'].create()
    pre_meta.tables['user'].columns['photo_url'].create()
