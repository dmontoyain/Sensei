from flask import Blueprint
from flask_restful import Api
from resources import *
import database


api_bp = Blueprint('api', __name__)
api = Api(api_bp)

#   routes configuration

#   users endpoints
api.add_resource(userProjects, '/user/:userId/projects')
api.add_resource(onlineUsers, '/users/online')
api.add_resource(Users, '/users')

#   mentors endpoints
api.add_resource(onlineMentors, '/mentors')
api.add_resource(projectMentors, '/mentors/:projectId')
api.add_resource(projectMentor, '/mentors/:mentorId')
api.add_resource(newMentor, 'mentor/:projectId/projects/:userId/users')

#   appointments endpoints
api.add_resource(Appointments, '/appointments')
api.add_resource(userAppointments, '/appointments/:userId')
api.add_resource(mentorAppointments, '/appointments/:mentorId')
api.add_resource(detailedAppointment, '/appointments/:appointmentId')
