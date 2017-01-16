from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
project = Table('project', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('photo_url', String),
    Column('time_in_days', Integer),
    Column('rav_id', Integer),
    Column('user_id', Integer),
    Column('cluster_id', Integer),
    Column('pattern_id', Integer),
)

pattern = Table('pattern', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=64)),
    Column('category', VARCHAR(length=100)),
    Column('photo_url', VARCHAR),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['project'].columns['photo_url'].create()
    pre_meta.tables['pattern'].columns['photo_url'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['project'].columns['photo_url'].drop()
    pre_meta.tables['pattern'].columns['photo_url'].create()
