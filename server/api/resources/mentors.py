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


#   api/mentors
class apiMentors(Resource):
	def get(self):
		query = Mentor.query.all()
        if not query
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
		return None, 202

#   api/mentor/:mentorId/subscribeunsubscribe
class apiSubscribeUnSubscribeMentor(Resource):

	#   Subscribes or unsibscribes mentor to a specific project.
	#   Updates 'available' to true in DB to give permission.
	#   Contraint: mentor's 'abletomentor' in DB needs to be True.
	def put(self, mentorId):
		#   get mentor record
		mentor = Mentor.query.filter_by(id=mentorId).first()

		#   check if mentor exists in database
		if not mentor:
			return res.badRequestError("No mentor with id {} was found".format(mentorId))

		#   check if mentor CAN mentor a project
		if mentor.abletomentor is False:
			errMessage = 'Subscribe Error for mentor record id {}. User {} does not qualify for mentoring project {}'.format(mentor.id, mentor.id_user42, mentor.id_project42)
			return res.badRequestError(errMessage)

		#   Swap active state
		mentor.active = not mentor.active
		db.session.commit()
		return res.putSuccess('Updated mentor {} to \'active\' state of {}'.format(mentorId, mentor.active))

#   api/mentor/:mentorId/subscribe
class apiSubscribeMentor(Resource):

	#   Subscribes or unsibscribes mentor to a specific project.
	#   Updates 'active' to true in DB to give permission.
	#   Contraint: mentor's 'abletomentor' in DB needs to be True.
	def put(self, mentorId):
		#   get mentor record
		mentor = Mentor.query.filter_by(id=mentorId).first()

		#   check if mentor exists in database
		if mentor is None:
			return res.badRequestError("No mentor with id {} was found".format(mentorId))

		#   check if mentor CAN mentor a project
		if mentor.abletomentor is False:
			errMessage = 'Subscribe Error for mentor record id {}. User {} does not qualify for mentoring project {}'.format(mentor.id, mentor.id_user42, mentor.id_project42)
			return res.badRequestError(errMessage)

		#	check if mentor is already subscribed
		if mentor.active is True:
			errMessage = 'Mentor with id {} is already subscribed to 42 project id {}'.format(mentor.id, mentor.project.id_project42)
			return res.badRequestError(errMessage)

		#   subscribe mentor to project
		mentor.active = True
		db.session.commit()
		mentorData = mentor_schema.dump(mentor).data
		return res.putSuccess('Mentor {} has successfully subscribed to project {}'.format(mentorId, mentor.project.id_project42), mentorData)

#   api/mentor/:mentorId/unsubscribe
class apiUnsubscribeMentor(Resource):

	#   Updates 'active' to true in DB to give permission.
	#   Contraint: mentor's 'abletomentor' in DB needs to be True.
	def put(self, mentorId):
		#   get mentor record
		mentor = Mentor.query.filter_by(id=mentorId).first()

		#   check if mentor exists in database
		if mentor is None:
			return res.badRequestError("No mentor with id {} was found".format(mentorId))

		#   check if mentor CAN mentor a project
		if mentor.abletomentor is False:
			errMessage = 'Subscribe Error for mentor record id {}. User {} does not qualify for mentoring project {}'.format(mentor.id, mentor.id_user42, mentor.id_project42)
			return res.badRequestError(errMessage)

		#	check if mentor is already unsubscribed
		if mentor.active is False:
			errMessage = 'Mentor with id {} is already unsubscribed to 42 project id {}'.format(mentor.id, mentor.project.id_project42)
			return res.badRequestError(errMessage)

		#   unsubscribe mentor to project
		mentor.active = False
		db.session.commit()
		mentorData = mentor_schema.dump(mentor).data
		successMessage = 'Mentor {} has successfully unsubscribed to project {}'.format(mentorId, mentor.project.id_project42)
		return res.putSuccess(successMessage, mentorData)

#   api/mentors/project/:projectId
class apiMentorsProject(Resource):

	#   Gets all mentors for the specified project
	def get(self, projectId):
		#   get mentors that exist for that project
		query = Mentor.query.filter_by(id_project42=projectId, active=True).all()
		if not query:
			return res.badRequestError('No Projects with id {} exist'.format(projectId))

		#   get mentors
		mentors = mentors_schema.dump(query).data

		#	grab the current online students at 42
		onlineUsers = Api42.onlineUsers()

		#	find intersection between online students and active mentors
		result = [mentor for mentor in mentors for x in onlineUsers if mentor['id_user42'] == x['id']]
		return res.getSuccess('mentors available for project {}'.format(projectId), result)

	#   Creates a new mentor for the specified project
	def post(self, projectId):
		return Mentor, 201


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
