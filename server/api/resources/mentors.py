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


#   api/mentors/
class apiMentors(Resource):
	def get(self):
		query = Mentor.query.all()
		data = mentors_schema.dump(query).data
		return res.getSuccess('all mentors', data)


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
		#   get mentor record
		mentor = Mentor.query.filter_by(id=mentorId).first()

		#   check if mentor exists in database
		if mentor is None:
			return res.badRequestError("No mentor with id {} was found".format(mentorId))

		#   check if mentor CAN mentor a project
		if mentor.abletomentor is False:
			errMessage = 'Subscribe Error for mentor record id {}. User {} does not qualify for mentoring project {}'.format(mentor.id, mentor.id_user42, mentor.id_project42)
			return res.badRequestError(errMessage)

		#   Swap active state
		mentor.active = not mentor.active
		db.session.commit()
		return res.putSuccess('Updated mentor {} to \'active\' state of {}'.format(mentorId, mentor.active))

#   api/mentors/project/:projectId
class apiMentorsProject(Resource):

	#   Gets all mentors for the specified project
	def get(self, projectId):
		mentors, error = Mentor.queryManyByFilter(id_project42=projectId, active=True)
		#	check if mentors exist for that project
		if error:
			res.badRequestError(error)

		#	grab the current online students at 42
		onlineUsers = Api42.onlineUsers()

		#	find intersection between online students and active mentors
		result = [mentor for mentor in mentors for x in onlineUsers if mentor['id_user42'] == x['id']]
		return res.getSuccess('mentors available for project {}'.format(projectId), result)

	#   Creates a new mentor for the specified project
	def post(self, projectId):
		return Mentor, 201


#   api/mentors/user/:id_user42/active
class apiUserMentoring(Resource):

	#   Gets projects user is subscribed to mentor
	def get(self, id_user42):
		mentors = Mentor.queryManyByFilter(id_user42=id_user42, active=True)
		return res.getSuccess(data=mentors)

#   api/mentors/user/:id_user42/capable
class apiUserCapabletoMentor(Resource):

	#   Gets projects the user is not subscribed and is capable of subscribing to be a mentor
	#   To be capable of mentoring user has to have passed project with a finalmark > 90
	def get(self, id_user42):
		mentors = Mentor.queryManyByFilter(id_user42=id_user42, abletomentor=True, active=False)
		return res.getSuccess(data=mentors)
