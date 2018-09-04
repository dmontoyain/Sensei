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
from .mentorAlgo import mentorAlgorithm

_maxAppointmentsPerDay = 2

#   /api/appointments
class apiAppointments(Resource):

	#   gets all active appointments
	def get(self):
		query = Appointment.query.all()
		if not query:
			return res.getSuccess("No appointments found.")
		appointments = appointments_schema.dump(query).data
		if not appointments:
			return res.internalServiceError("Failed to create appointment schema.")
		return res.getSuccess("Found appointments", appointments)
	
	#   Creates an appointment for a user in a specified project or topic
	#   Requires structuring of the request body:
	#   project = project name 'or' topic = specific topic ('linked lists', 'hashtables', etc.)
	#   login = user login ('dmontoya', 'bpierce')
	#   {"project":"fillit", "login":"bpierce"}
	def post(self):

		data = request.get_json()

		#   Checks if required data to create an appointment was provided in request
		if not data:
			return res.badRequestError("Missing data to process request.")
		if not data.get("topic") and not data.get("project"):
			return res.badRequestError("Missing data to process request. No topic or project provided to search for mentors")
		if not data.get("login"):
			return res.badRequestError("Missing data to process request. No user login provided")
		
		#   Checks if project name exists in database
		query = Project.query.filter_by(name=data.get("project")).first()
		if not query:
			return res.resourceMissing("No project {} found.".format(data.get("project")))
		project, error = project_schema.dump(query)
		if error:
			return res.internalServiceError(error)
		
		#   Checks if user with provided login exists in database
		user, error = User.queryByLogin(data.get("login"))
		if error:
			return res.resourceMissing(error)
		
		#   check appointments made by user for project
		projectAppointmentsCount = Appointment.queryCountProjectAppointmentsbyUser(project["id_project42"], user["id"])
		if projectAppointmentsCount > _maxAppointmentsPerDay:
			return res.badRequestError("User reached limit appointments for project {}".format(data.get("project")))
		
		#   Retrieves available mentors for the specified project
		queryMentor = Mentor.query.filter(Mentor.id_project42==project["id_project42"], Mentor.active==True, Mentor.id_user42!=user['id_user42'])
		if not queryMentor:
			res.resourceMissing('No mentors exist for project id {}'.format(data.get('project')))
		mentors = mentors_schema.dump(queryMentor).data
		onlineUsers = Api42.onlineUsers()

		#	Checks online students is not empty
		if len(onlineUsers) == 0:
			return res.resourceMissing("No mentors found on campus.")

		availablementors = [mentor for mentor in mentors for x in onlineUsers if mentor['id_user42'] == x['id']]
		
		#   Checks if there is avaliable online mentors for the project/topic
		if not availablementors:
			return res.resourceMissing("No mentors online found for {}.".format(data.get("project"))) 

		#   Calls 'mentor algorithm' to select a mentor from availablementors.
		chosenmentor = mentorAlgorithm(availablementors)

		#   Creates and returns appointment if valid
		if not chosenmentor:
			return res.internalServiceError("Error: mentor selection.")

		newappointment, error = Appointment.createAppointment(chosenmentor["id"], user["id"])
		if error:
			return res.internalServiceError(error)

		return res.postSuccess("Appointment created successfully.", newappointment)

#   /api/appointment/:appointmentId
class apiAppointment(Resource):
	#   retrieve appointment details
	def get(self, appointmentId):
		appointment, err = Appointment.queryById(appointmentId)
		if err:
			return res.badRequestError(err)
		return res.getSuccess(appointment)

	#   updates the specified appointment feedback
	#	request body should contain the user feedback for this appointment
	#	{"feedback": "Great mentor, knew his stuff"}
	def put(self, appointmentId):
		data = request.get_json()
		#   First check if the appointment record exists
		appointment = Appointment.query.filter_by(id=appointmentId)
		if not appointment:
			return res.resourceMissing("Appointment {} not found.".format(appointmentId))
		feedback = data.get('feedback')
		if len(feedback) == 0:
			return res.badRequestError("User must feedback mentor")
		#	Cancel appointment by setting status = 3
		appointment.feedback = feedback
		db.session.commit()
		return res.putSuccess("Appointment {} cancelled.".format(appointmentId), appointment_schema.dump(appointment).data)

	def delete(self, appointmentId):
		#   First check if the appointment record exists
		appointment = Appointment.query.filter_by(id=appointmentId)
		if not appointment:
			return res.resourceMissing("Appointment {} not found.".format(appointmentId))

		#	Cancel appointment by setting status = 3
		appointment.status = 3
		db.session.commit()
		return res.putSuccess("Appointment {} cancelled.".format(appointmentId), appointment_schema.dump(appointment).data)

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
			return res.getSuccess(error)
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
		appointments, error = Appointment.queryManyAsMentor(user["id_user42"])
		if error:
			return res.getSuccess(error)
		return res.getSuccess('All Appointments for user {} as mentor, ever'.format(user['login']), appointments)


#   ------------------------------------------
#   Pending appointments endpoints
#   searches by **username** not userId as requested by Kmckee

#   /api/appointments/pending/mentor/:login
class apiPendingAppointmentsAsMentor(Resource):

	#   Gets all pending appointments from the user specified as Mentor
	def get(self, login):
		user, error = User.queryByLogin(login)
		if error:
			return res.resourceMissing(error)
		appointments, error = Appointment.queryManyPendingAsMentor(user["id_user42"])
		if error:
			return res.getSuccess(error)
		retMessage = "appointments for mentor {}".format(login)
		keyword = 'No ' if error else 'Pending '
		retMessage = keyword + retMessage
		return res.getSuccess(retMessage, appointments)

#   /api/appointments/pending/user/:login
class apiPendingAppointmentsAsUser(Resource):

	#   gets all pending appointments from the user specified as User (Mentee)
	def get(self, login):
		user, error = User.queryByLogin(login)
		if error:
			return res.resourceMissing(message=error)
		appointments, error = Appointment.queryManyPendingAsUser(user["id"])
		if error:
			return res.getSuccess(error)
		retMessage = "appointments for user {}".format(login)
		keyword = 'No ' if error else 'Pending '
		retMessage = keyword + retMessage
		return res.getSuccess(retMessage, appointments)
