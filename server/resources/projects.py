from flask_restful import Resource
from models import User, Project, Mentor, Appointment

#   api/projects
class allProjects(Resource):
    def get(self):
        return Project.query.all()
    
    def post(self):
        Project.commit()
        return Project.save.all()