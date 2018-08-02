from datetime import datetime
from api.app import db, ma

class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    project_id42 = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), nullable=False)
    tier = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)

    #   relationship with 'Mentors' table, Mentor Model Class
    mentors = db.relationship('Mentor', backref='project', lazy=True)

    def __init__(self, projectid42, name, slug, tier, active=True):
        self.project_id42 = projectid42
        self.name = name
        self.slug = slug
        self.tier = tier
        self.active = active

    @property
    def serialize(self):
        return {
            "id": self.id,
            "project_id42": self.project_id42,
            "name": self.name,
            "slug": self.slug,
            "tier": self.tier,
            "active" : self.active
        }

class ProjectSchema(ma.ModelSchema):
    class Meta:
        model = Project