from models import db

class Project(db.Model):
    __tablename__ = 'Projects'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    project_id42 = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), nullable=False)
    tier = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)

    #   relationship with 'Mentors' table, Mentor Model Class
    mentors = db.relationship('Mentor', backref='project', lazy=True)

    def serialize(self):
        return {'id' : self.id,
                'project_id42' : self.project_id42,
                'name' : self.name,
                'slug' : self.slug,
                'tier' : self.tier,
                'active' : self.active}