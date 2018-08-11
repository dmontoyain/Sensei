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
        data, err = Appointment.queryAll()
        if err:
            return res.internalServiceError(err)
        return res.getSuccess("Found appointments", data)
    
    #   Creates an appointment for a user in a specified project or topic
    #   Requires structuring of the request body:
    #   projectname = project name 'or' topic = specific topic ('linked lists', 'hashtables', etc.)
    #   login = user login ('dmontoya', 'bpierce')
    def post(self):
        data = request.get_json()

        #   Checks if required data to create an appointment was provided in request
        if not data:
            return res.badRequestError("No data provided")
        if data.get("topic") is None and data.get("project") is None:
            return res.badRequestError("Unable to create appointment. No topic/project provided to search for mentors")
        if data.get("login") is None:
            return res.badRequestError("Unable to create appointment. No user login provided")
        
        #   Checks if project name exists in database
        project, error = Project.queryProject(name=data.get("project"))
        if error:
            return res.resourceMissing(message=error)
        
        #   Checks if user with provided login exists in database
        user, error = User.queryByLogin(data.get("login"))
        if error:
            return res.resourceMissing(message=error)
        
        #   check appointments made by user for project
        projectAppointmentsCount = Appointment.queryCountProjectAppointmentsbyUser(project["id_project42"], user["id"])
        if projectAppointmentsCount > 1:
            return res.badRequestError("User reached limit appointments for project {}".format(data.get("project")))

        #   Retrieves availables mentors for such project
        mentors, error = Mentor.queryManyByFilter(id_project42=project["id_project42"], active=True)
        if error:
            res.internalServiceError(message=error)
        onlineUsers = Api42.onlineUsers()
        availablementors = [mentor for mentor in mentors for x in onlineUsers if mentor['id_user42'] == x['id']]

        #   Checks if there is avaliable online mentors for the project/topic
        if availablementors is None and len(availablementors) is 0:
            res.resourceMissing("No mentors online found for {}".format(data.get("project"))) 

        #--------------------------
        #   Calls funtion/service to select mentor from the availablementors.

        #   temporary for testing creation of appointment
        chosenmentor = availablementors[0]

        #--------------------------

        #   Creates and returns appointment if valid
        if chosenmentor is None:
            return res.internalServiceError(message="No mentor found/chosen")
        newappointment, error = Appointment.createAppointment(chosenmentor["id"], user["id"])
        if error:
            return res.internalServiceError, error
        return res.postSuccess("Appointment created successfully", newappointment)

#   /api/appointment/:appointmentId
class apiAppointment(Resource):
    #   retrieve appointment details
    def get(self, appointmentId):
        data, err = Appointment.queryById(appointmentId)
        if err:
            return res.badRequestError(err)
        return res.getSuccess(data)

    #   updates the specified appointment 
    #   (should be used after choosing mentor to assign mentor)
    def put(self, appointmentId):
        #   First check if the appointment record exists
        data, err = Appointment.queryById(appointmentId)
        if err:
            return res.badRequestError(err)

        #   check if put request contains appropriate data
        return res.postSuccess('appointment was updated', data)

    #   cancel an appointment
    def delete(self, appointmentId):
        #   first check if appointment record exists
        record = Appointment.query.filter_by(id=appointmentId).first()
        if record is None:
            return res.badRequestError('No appointment with id {} was found'.format(appointmentId))

        #   save return data
        data = appointment_schema.dump(record).data

        #   delete appointment
        db.session.delete(record)
        db.session.commit()
        return res.deleteSuccess('appointment was deleted', data)

#   /api/appointments/user/:login
class apiAppointmentsAsUser(Resource):

    #   gets all appointments from specified user as User
    def get(self, login):

        #   Validates user credentials received
        user, error = User.queryByLogin(login)
        if error:
            return res.resourceMissing(message=error)
        
        #   Retrieves appointments for found user
        appointments, error = Appointment.queryManyAsUser(user["id"])
        if error:
            return res.resourceMissing(error)
        return res.getSuccess("Appointments for user {}".format(user), appointments)

#   /api/appointments/mentor/:login
class apiAppointmentsAsMentor(Resource):

    #   gets all appointments from specified user as mentor
    def get(self, login):

        #   Validates user credentials received
        user, error = User.queryByLogin(login)
        if error:
            return res.resourceMissing(message=error)
        #   Retrieves appointments for found user
        print(user)
        appointments, error = Appointment.queryManyAsMentor(user["id_user42"])
        if error:
            return res.getSuccess(data=error)
        return res.getSuccess('Appointments for user {} as mentor'.format(user), appointments)

#   ------------------------------------------
#   Pending appointments endpoints
#   searches by **username** not userId as requested by Kmckee

#   /api/appointments/pending/mentor/:login
class apiPendingAppointmentsAsMentor(Resource):

    #   Gets all pending appointments from the user specified as Mentor
    def get(self, login):
        user, error = User.queryByLogin(login)
        if error:
            return res.resourceMissing(message=error)
        appointments, error = Appointment.queryManyPendingAsMentor(user["id_user42"])
        if error:
            return res.getSuccess(data=error)
        return res.getSuccess('Pending appointments for user {} to mentor'.format(user), data=appointments)

#   /api/appointments/pending/user/:login
class apiPendingAppointmentsAsUser(Resource):

    #   gets all pending appointments from the user specified as User (Mentee)
    
    def get(self, login):
        user, error = User.queryByLogin(login)
        if error:
            return res.resourceMissing(message=error)
        appointments, error = Appointment.queryManyPendingAsUser(user["id"])
        retMessage = "appointments for user {}".format(login)
        keyword = 'No ' if error else 'Pending '
        retMessage = keyword + retMessage
        return res.getSuccess(retMessage, appointments)

#   ----------------------------------------


#   /api/appointments/:mentorId
class apiAppointmentsMentor(Resource):

    #   gets all appointments with the specified mentor
    def get(self, mentorId):
        return Appointment, 201
