import json
from flask import request
from flask_restful import Resource
from api.app import db
from api.models import User, user_schema, users_schema
from api.models import Mentor, mentor_schema, mentors_schema
from api.models import Project, project_schema, projects_schema
from api.models import Appointment, appointment_schema, appointments_schema
from rq42 import Api42
from response import Response as res

#   /api/appointments
class apiAppointments(Resource):
    #   gets all active appointments
    def get(self):
        return Appointment.query.all(), 200


#   /api/appointment/:appointmentId
class apiAppointment(Resource):
    #   retrieve appointment details
    def get(self, appointmentId):
        return Appointment, 201

    #   updates the specified appointment 
    #   (should be used after choosing mentor to assign mentor)
    def put(self, appointmentId):
        return Appointment, 201
    
    #   cancel an appointment
    def delete(self, appointmentId):
        return Appointment, 204


#   /api/appointments/:userId
class apiAppointmentsUser(Resource):

    #   gets all the appintments from the specified user
    def get(self, userId):
        return Appointment, 200
    
    #   creates a new Appointment for the user specified
    def post(self, userId):
        return Appointment, 201


#   /api/appointments/:mentorId
class apiAppointmentsMentor(Resource):

    #   gets all appointments with the specified mentor
    def get(self, mentorId):
        return Appointment, 201

