from flask_restful import Resource
from models import User, Project, Mentor, Appointment

#   api/mentors/
class onlineMentors(Resource):
    def get(self):
        return Mentor.query.all()

#   api/mentors/:projectId
class projectMentors(Resource):

    #   Gets all mentors for the specified project
    def get(self, projectId):
        return Mentor.query.all()
    
    #   Creates a new mentor for the specified project 
    def post(self, projectId):
        return Mentor

#   api/mentors/:mentorId
class projectMentor(Resource):

    #   Gets specified mentor data
    def get(self, mentorId):
        return Mentor(mentorId)

    #   Updates any mentor data for the specified project
    def put(self, mentorId):
        #update
        return Mentor(mentorId)

#   api/mentors/:mentorId/projects
class mentorProjects(Resource):

    #   Gets all projects mentor is subscribed
    def get(self, mentorId):
        return 

#   api/mentor/:projectId/projects/:userId/users
class newMentor(Resource):

    def post(self, projectId, userId):
        return Mentor
