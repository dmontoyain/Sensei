import json
from flask import request
from flask_restful import Resource
from api.app import db
from api.models import User, user_schema, users_schema
from api.models import Mentor, mentor_schema, mentors_schema
from api.models import Project, project_schema, projects_schema
from api.models import  Status, Appointment, appointment_schema, appointments_schema
from rq42 import Api42
from response import Response as res
from .mentorAlgo import mentorAlgorithm

_maxAppointmentsPerDay = 2

#   /api/appointments
class apiAppointments(Resource):

	#   Gets all pending appointments
	def get(self):
		queryAppointments = Appointment.query.filter_by(status=Status['Pending']).all()
		if not queryAppointments:
			return res.getSuccess("No appointments found.")
		appointments = appointments_schema.dump(queryAppointments).data
		if not appointments:
			return res.internalServiceError("Failed to create appointment schema.")
		return res.getSuccess(data=appointments)
	
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
		
		#   Limits appointments made by user for a specific project
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

	#   Updates the appointment data
	#	Request body can contain user feedback or status for this appointment
	#	{"feedback": "Great mentor, knew his stuff", "status", "1" }
	#	This endpoint should not be used to cancel the appointment
	def put(self, appointmentId):
		data = request.get_json()
		if not data:
			return res.badRequestError("No data provided")

		#   Checks appointment record exists
		appointment = Appointment.query.filter_by(id=appointmentId).first()
		if not appointment:
			return res.resourceMissing("Appointment {} not found.".format(appointmentId))
		
		if 'feedback' in data:
			if len((data.get('feedback')).strip()) <= 4:
				return res.badRequestError('Feedback needs to be longer.')
			appointment.feedback = data.get('feedback')
		
		if 'status' in data:
			if data.get('status') != Status['Cancelled']:
				appointment.status = data.get('status')

		db.session.commit()
		return res.putSuccess("Appointment {} updated.".format(appointmentId), appointment_schema.dump(appointment).data)

	#	Cancels appointment only if the status is 'Pending'
	def delete(self, appointmentId):

		#   Checks appointment record exists
		appointment = Appointment.query.filter_by(id=appointmentId).first()
		if not appointment:
			return res.resourceMissing("Appointment {} not found.".format(appointmentId))
		
		#	Verifies appointment status is 'Pending'
		if appointment.status == Status['Finished']:
			return res.badRequestError("Appoint has already been marked as finished.")
		if appointment.status == Status['Cancelled']:
			return res.badRequestError("Appointment already cancelled.")

		#	Cancel appointment by setting status = 3
		appointment.status = Status['Cancelled']

		db.session.commit()
		return res.putSuccess("Appointment {} cancelled.".format(appointmentId), appointment_schema.dump(appointment).data)