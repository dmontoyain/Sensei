from api.app import db, ma
from datetime import datetime
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
    
    @classmethod
    def queryProject(cls, id42=0, name=""):
        if id42 is not 0:
            query = cls.query.filter_by(id_project42=id42).first()
            if query is None:
                return None, "No project with 42 id {}".format(id42)
        elif len(name) > 0:
            query = cls.query.filter_by(name=name).first()
            if query is None:
                return None, "No project named {}".format(name)
        else:
            return None, "No data provided to query"
        return project_schema.dump(query).data, None

    @classmethod
	def queryAll(cls):
		query = cls.query.all()
		if query is None:
			return None, "No projects exist"
		return projects_schema.dump(query).data, None

class ProjectSchema(ma.ModelSchema):
    class Meta:
        model = Project
        include_fk = True

project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)