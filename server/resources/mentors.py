from flask_restful import Resource
from models import User, Project, Mentor, Appointment
from resources import globalOnlineUsers
from flask import jsonify

#   api/mentors/
class Mentors(Resource):
    def get(self):
        globalOnlineUsers.lock()
        ret = str([mentor for mentor in globalOnlineUsers._onlineUsersList])
        globalOnlineUsers.unlock()
        return ret, 201

#   api/mentors/project/:projectId
class projectMentors(Resource):

    #   Gets all mentors for the specified project
    def get(self, projectId):
        mentors = Mentor.query.filter_by(id_project=projectId)
        globalOnlineUsers.lock()           
        globList = globalOnlineUsers._onlineUsersList
        ret = [mentor.serialize for mentor in mentors for x in globList if mentor.user.id_user42 == x['id']]
        globalOnlineUsers.unlock()
        return jsonify(ret), 201
    
    #   Creates a new mentor for the specified project 
    def post(self, projectId):
        return Mentor

#   api/mentors/mentor/:mentorId
class projectMentor(Resource):

    #   Gets specified mentor data
    def get(self, mentorId):
        return Mentor(mentorId)

    #   Updates any mentor data for the specified project
    def put(self, mentorId):
        #update
        return Mentor(mentorId)

#   ???? Is this necessary???????
#   api/mentors/:mentorId/projects
class mentorProjects(Resource):

    #   Gets all projects mentor is subscribed
    def get(self, mentorId):
        return 

#   api/mentor/:projectId/projects/:userId/users
class newMentor(Resource):

    def post(self, projectId, userId):
        return Mentor

#   api/mentors/user/:userId

class userMentors(Resource):

    #   Gets user projects he is subscribed to mentor
    def get(self, userId):
        mentors = Mentor.query.filter_by(id_user=userId)
        return str([{'project': mentor.project.name, 'finalmark': mentor.finalmark } for mentor in mentors]), 201
