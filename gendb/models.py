"""Models for GenDB database."""

from gendb.extensions import db


groups = db.Table(
    'groups',
    db.Column('user_email', db.String(64), db.ForeignKey('user.email')),
    db.Column('project_id', db.Integer, db.ForeignKey('project.project_id'))
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))

    # Relationships
    project_owner = db.relationship(
        'Project',
        backref='owner_of',
        lazy='dynamic'
    )

    project_member = db.relationship(
        'Project',
        secondary=groups,
        primaryjoin=(groups.c.user_email == email),
        backref=db.backref('projects', lazy='dynamic'),
        lazy='dynamic'
    )

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


class Project(db.Model):
    project_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(500))
    owner = db.Column(db.String(45), db.ForeignKey('user.email'))
    contributors = db.relationship(
        'User',
        secondary=groups,
        primaryjoin=(groups.c.project_id == project_id),
        backref=db.backref('contributors', lazy='dynamic'),
        lazy='dynamic'
    )
