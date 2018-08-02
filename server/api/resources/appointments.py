from flask_restful import Resource
from api.models import User, Project, Mentor, Appointment

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

