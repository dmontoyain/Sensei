from datetime import datetime
from api.app import db, ma
import sqlalchemy as sa

class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    id_project42 = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), nullable=False)
    tier = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, nullable=False, server_default=sa.sql.expression.true())

    #   relationship with 'Mentors' table, Mentor Model Class
    mentors = db.relationship('Mentor', backref='project', lazy=True)

    def __init__(self, id_project42, name, slug, tier, active=True):
        self.id_project42 = id_project42
        self.name = name
        self.slug = slug
        self.tier = tier
        self.active = active

class ProjectSchema(ma.ModelSchema):
    class Meta:
        model = Project