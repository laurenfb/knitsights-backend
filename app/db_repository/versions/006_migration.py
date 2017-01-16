from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
pattern = Table('pattern', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('category', String(length=100)),
    Column('photo_url', String),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('email', String),
    Column('photo_url', String),
    Column('imported', Boolean, default=ColumnDefault(False)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['pattern'].columns['photo_url'].create()
    post_meta.tables['user'].columns['photo_url'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['pattern'].columns['photo_url'].drop()
    post_meta.tables['user'].columns['photo_url'].drop()
