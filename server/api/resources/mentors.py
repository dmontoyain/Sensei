from flask_restful import Resource
from api.models import Mentor, MentorSchema, User, Project, Appointment
from rq42 import Api42
from flask import jsonify, request
import json

def formatError(err, errorMessage):
    if errorMessage is not '':
        return '{}. {}'.format(err, errorMessage)
    return err

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
        return None, 200

    #   Updates any mentor data for the specified project
    def put(self, mentorId):
        return None, 202


#   api/mentor/:mentorId/subscribeunsubscribe
class apiSubscribeUnSubscribeMentor(Resource):

    #   Subscribes or unsibscribes mentor to a specific project.
    #   Updates 'available' to true in DB to give permission.
    #   Contraint: mentor's 'abletomentor' in DB needs to be True.
    def put(self, mentorId):
        data = request.get_json()
        mentor = Mentor.query.filter_by(id=mentorId).first()
        if mentor.active is True:
            mentor.active = False
            return json.dumps(MentorSchema().dump(mentor)), 201
        if mentor.abletomentor is False:
            return formatError('Subscribing Error', 'User does not qualify for mentoring project'), 401
        mentor.active = True
        return json.dumps(MentorSchema().dump(mentor)), 201

#   api/mentors/project/:projectId
class apiMentorsProject(Resource):

    #   Gets all mentors for the specified project
    def get(self, projectId):
        query = Mentor.query.filter_by(id_project=projectId).all()
        mentor_schema = MentorSchema()
        mentors = mentor_schema.dump(query).data
        onlineUsers = Api42.onlineStudents()
        result = [mentor for mentor in mentors for x in onlineUsers if mentor.user.id_user42 == x['id']]
        return result, 200

    #   Creates a new mentor for the specified project
    def post(self, projectId):
        return Mentor, 201


#   api/mentors/user/:id_user42/active
class apiUserMentoring(Resource):

    #   Gets projects user is subscribed to mentor
    def get(self, id_user42):
        query = Mentor.query.filter_by(id_user42=id_user42, active=True).all()
        mentors = MentorSchema(many=True).dump(query).data
        return mentors, 200

#   api/mentors/user/:id_user42/capable
class apiUserCapabletoMentor(Resource):

    #   Gets projects the user is not subscribed and is capable of subscribing to be a mentor
    #   To be capable of mentoring user has to have passed project with a finalmark > 90
    def get(self, id_user42):
        query = Mentor.query.filter_by(id_user42=id_user42, abletomentor=True, active=False)
        mentors = MentorSchema(many=True).dump(query).data
        return mentors, 200
