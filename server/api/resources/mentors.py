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


#   api/mentors
class apiMentors(Resource):
	def get(self):
		query = Mentor.query.all()
		if not query:
			return res.badRequestError("No mentors")
		data = mentors_schema.dump(query).data
		return res.getSuccess('all mentors', data)


#   api/mentor/:mentorId
class apiMentor(Resource):

	#   Gets specified mentor data
	def	get(self, mentorId):
		query = Mentor.query.filter_by(id=mentorId).first()
		if not query:
			return res.badRequestError('no mentor record with id {} exists'.format(mentorId))

		data = mentor_schema.dump(query).data
		if not data:
			return res.internalServiceError('failed to build mentor data')

		return res.getSuccess('mentor data retrieved for user {} on project {}'.format(query.user.login, query.project.name), data)

	#   Updates any mentor data for the specified project
	def	put(self, mentorId):
		data = request.get_json()
		if not data:
			return res.badRequestError("No data provided. Please read API documentation")
		
		queryMentor = Mentor.query \
			.filter_by(id=mentorId) \
			.first()
		if not queryMentor:
			return res.badRequestError("No mentor with id {} was found".format(mentorId))

		if 'active' in data:
			queryMentor.active = data.get('active')

		db.session.commit()
		return res.putSuccess('Mentor {} updated'.format(mentorId))

#   api/mentors/project/:projectId
class apiMentorsProject(Resource):

	#   Gets all active mentors for the specified project
	def get(self, projectId):
		#   get mentors that exist for that project
		query = Mentor.query \
			.filter_by(id_project42=projectId, active=True) \
			.all()
		if not query:
			return res.badRequestError('No Projects with id {} exist'.format(projectId))

		mentors = mentors_schema.dump(query).data
		return res.getSuccess('mentors available for project {}'.format(projectId), result)


#   api/mentors/user/:login/active
class apiUserMentoring(Resource):

	#   Gets projects user is subscribed to mentor
	def get(self, login):
		user, error = User.queryByLogin(login)
		if error:
			return res.resourceMissing(error)

		#   get the mentor records for that user on which projects they can mentor
		query = Mentor.query.filter_by(id_user42=user['id_user42'], active=True)
		if not query:
			return res.internalServiceError('no mentor records for user {}'.format(login))

		#   return the mentor data
		mentors = mentors_schema.dump(query).data
		return res.getSuccess(data=mentors)

#   api/mentors/user/:login/capable
class apiUserCapabletoMentor(Resource):

	#   Gets projects the user is not subscribed and is capable of subscribing to be a mentor
	def get(self, login):
		user, error = User.queryByLogin(login)
		if error:
			return res.resourceMissing(error)

		#   get the mentor records for that user on which projects they can mentor
		query = Mentor.query.filter_by(id_user42=user['id_user42'], abletomentor=True, active=False)
		if not query:
			return res.internalServiceError('no mentor records for user {}'.format(login))

		#   return the mentor data
		mentors = mentors_schema.dump(query).data
		return res.getSuccess(data=mentors)

#	/api//mentors/<int:userId>/pendingappointments
class apiMentorPendingAppointments(Resource):
	def get(self, userId):
		#	Appointments Table query for the specified user as mentor
		queryAppointments = Appointment.query \
			.join(Mentor) \
			.filter(Appointment.status==Status['Pending']) \
			.filter(Mentor.id_user42==userId) \
			.all()
		if not queryAppointments:
			return res.resourceMissing("No appointments found")
		pendingAppointments = []
		for a in queryAppointments:
			obj = {
				'appointment': appointment_schema.dump(a).data,
				'user': user_schema.dump(getattr(a, 'user')).data,
				'project': project_schema.dump(getattr(getattr(a, 'mentor'), 'project')).data
			}
			pendingAppointments.append(obj)
		return res.getSuccess("Appointments for mentor", pendingAppointments)
