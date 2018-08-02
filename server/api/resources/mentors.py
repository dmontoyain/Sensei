from flask_restful import Resource
from api.models import User, Project, Mentor, Appointment
from rq42 import Api42
from flask import jsonify

#   api/mentors/
class apiMentors(Resource):
    def get(self):
        Api42.lock()
        ret = str([mentor for mentor in Api42.onlineStudents()])
        Api42.unlock()
        return ret, 200


#   api/mentor/:mentorId
class apiMentor(Resource):

    #   Gets specified mentor data
    def get(self, mentorId):
        return Mentor(mentorId), 200

    #   Updates any mentor data for the specified project
    def put(self, mentorId):
        #   update something
        return Mentor(mentorId), 202


#   api/mentors/project/:projectId
class apiMentorsProject(Resource):

    #   Gets all mentors for the specified project
    def get(self, projectId):
        mentors = Mentor.query.filter_by(id_project=projectId)
        Api42.lock()
        onlineUsers = Api42.onlineStudents()
        result = [mentor.serialize for mentor in mentors for x in onlineUsers if mentor.user.id_user42 == x['id']]
        Api42.unlock()
        return result, 200

    #   Creates a new mentor for the specified project
    def post(self, projectId):
        return Mentor, 201


#   api/mentors/user/:userId
class apiMentorsUser(Resource):

    #   Gets user projects he is subscribed to mentor
    def get(self, userId):
        mentors = Mentor.query.filter_by(id_user=userId)
        return str([{'project': mentor.project.name, 'finalmark': mentor.finalmark } for mentor in mentors]), 200


#   api/mentors/project/:projectId/user/:userId
class apiMentorNew(Resource):

    def post(self, projectId, userId):
        return Mentor, 201
