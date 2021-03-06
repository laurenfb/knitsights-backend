from app import db
from as_dict import AsDict


class User(db.Model, AsDict):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(), unique = True)
    photo_url = db.Column(db.String())
    imported = db.Column(db.Boolean, default = False)

    projects = db.relationship('Project', backref='user', lazy='dynamic')
    clusters = db.relationship('Cluster', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % (self.name)

class Cluster(db.Model, AsDict):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    avg_days = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    projects = db.relationship('Project', backref='cluster', lazy='dynamic')

    def __repr__(self):
        return '<Cluster %r>' % (self.name)

class Pattern(db.Model, AsDict):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    category = db.Column(db.String(100))
    rav_id = db.Column(db.Integer)

    projects = db.relationship('Project', backref='pattern', lazy='dynamic')

    def __repr__(self):
        return '<Pattern %r>' % (self.name)

class Project(db.Model, AsDict):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    photo_url = db.Column(db.String())
    time_in_days = db.Column(db.Integer)
    rav_id = db.Column(db.Integer)
    archived = db.Column(db.Boolean, default = False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    cluster_id = db.Column(db.Integer, db.ForeignKey('cluster.id'))
    pattern_id = db.Column(db.Integer, db.ForeignKey('pattern.id'))

    def __repr__(self):
        return '<Project %r>' % (self.name)
