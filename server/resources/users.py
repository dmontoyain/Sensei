from flask_restful import Resource
from models import User, Project, Mentor, Appointment

#   /api/users/:userId/projects
class userProjects(Resource):
    def get(self, userId):
        return (Project.query.all())

#   /api/users/online
class onlineUsers(Resource):
    def get(self):
        return (User.query.all())

#   /api/users
class Users(Resource):
    def get(self):
        userQuery = User.query.all()
        print([{'login': user.login} for user in userQuery])
        return str([{'login': user.login } for user in userQuery])