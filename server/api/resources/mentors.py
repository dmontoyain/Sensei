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
		print(data)
		if not data or 'active' not in data:
			return res.badRequestError("No data provided")
		
		mentor = Mentor.query.filter_by(id=mentorId).first()
		#   check if mentor exists in database
		if not mentor:
			return res.badRequestError("No mentor with id {} was found".format(mentorId))

		if 'active' in data:
			mentor.active = data.get('active')

		db.session.commit()
		return res.putSuccess('Updated mentor to active {}'.format(data.get('active')))

# #   api/mentor/:mentorId/subscribeunsubscribe
# class apiSubscribeUnSubscribeMentor(Resource):

# 	#   Subscribes or unsibscribes mentor to a specific project.
# 	#   Updates 'available' to true in DB to give permission.
# 	#   Contraint: mentor's 'abletomentor' in DB needs to be True.
# 	def put(self, mentorId):
# 		#   get mentor record
# 		mentor = Mentor.query.filter_by(id=mentorId).first()

# 		#   check if mentor exists in database
# 		if not mentor:
# 			return res.badRequestError("No mentor with id {} was found".format(mentorId))

# 		#   check if mentor CAN mentor a project
# 		if mentor.abletomentor is False:
# 			errMessage = 'Subscribe Error for mentor record id {}. User {} does not qualify for mentoring project {}'.format(mentor.id, mentor.id_user42, mentor.id_project42)
# 			return res.badRequestError(errMessage)

# 		#   Swap active state
# 		mentor.active = not mentor.active
# 		db.session.commit()
# 		return res.putSuccess('Updated mentor {} to \'active\' state of {}'.format(mentorId, mentor.active))

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

class apiMentorPendingAppointments(Resource):
	def get(self, userId):
		queryMentor = Mentor.query.join(Appointment, Appointment.id_mentor==Mentor.id).filter(Appointment.status==Status['Pending']).filter(Mentor.id_user42==userId).all()
		if not queryMentor:
			return res.resourceMissing("No appointments")
		pendingAppointments = []
		allmentors = mentors_schema.dump(queryMentor).data
		for mentor in allmentors:
			for a in mentor['appointments']:
				queryAppnt = Appointment.query.filter_by(id=a).first()
				queryUser = User.query.filter_by(id=queryAppnt.id_user).first()
				queryProject = Project.query.filter_by(id_project42=mentor["id_project42"]).first()
				pendingAppointments.append({
					'appointment' : appointment_schema.dump(queryAppnt).data,
					'user' : user_schema.dump(queryUser).data,
					'project' : project_schema.dump(queryProject).data
					})
		#print(pendingAppointments)
		return res.getSuccess(message="Appointments as mentor for user {}".format(userId), data=pendingAppointments)
