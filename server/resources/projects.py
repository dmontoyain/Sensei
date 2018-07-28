from flask_restful import Resource
from models import User, Project, Mentor, Appointment

#   api/projects
class allProjects(Resource):
    def get(self):
        projects = Project.query.all()
        return [project.serialize for project in projects], 201
    
    def post(self):
        Project.commit()
        return Project.save.all()