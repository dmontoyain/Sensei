from flask_restful import Resource
from models import User, Project, Mentor, Appointment

#   api/projects
class apiProjects(Resource):
    def get(self):
        projects = Project.query.all()
        return [project.serialize for project in projects], 200

    def post(self):
        Project.commit()
        return Project.save.all(), 201