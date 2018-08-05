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


#	/api/users
class apiUsers(Resource):
	#	Returns all users in the database
	def get(self):
		query = User.query.all()
		data = users_schema.dump(query).data
		return res.getSuccess('all users', data)


#	/api/user/:userId/update
class apiUserUpdate(Resource):
	def post(self, userId):
		#	check if user exists
		user, errors = User.queryById_user42(userId)
		if errors:
			return res.badRequestError(errors)
		data = Api42.userProjects(userId)
		if data is None:
			return res.internalServiceError('No projects found for user in 42 Database')
		print('adding to session..')
		failedProjectIds = []
		projectsThatAlreadyExistInMentors = []
		projectsAddedToMentorTable = []
		for d in data:
			print(d)

			#	Check that the project id exists in the projects database
			query = Project.query.filter_by(id_project42=d['id_project42']).first()
			if query is None:
				failedProjectIds.append(d['id_project42'])
				continue

			#	Check that the project-user combination does not already exist in the mentors database
			# query = Mentor.query.filter_by(id_project42=d['id_project42'], id_user42=d['id_user42']).first()
			# query = Mentor.queryByFilter(id_project42=d['id_project42'], id_user42=d['id_user42'])
			if query is not None:
				projectsThatAlreadyExistInMentors.append(d['id_project42'])
				continue

			#	Validate using mentor schema
			newMentor, error = mentor_schema.load(d)
			if error:
				db.session.rollback()
				return res.badRequestError(error)

			#	Add new mentor to the transactional session
			db.session.add(newMentor)
			projectsAddedToMentorTable.append(newMentor)

		#	Success was achieved, so commit new records
		print('Initializing user {}. Committing to database'.format(userId))
		db.session.commit()

		#	Debugging - print out project ids that failed
		print('These were the projects that do not exist in the projects database:')
		for i in failedProjectIds:
			print(i)

		#	Debugging - print out project ids that already exist for user in mentor table
		print('These were the projects that ALREADY exist for the user in the mentors database:')
		for i in projectsThatAlreadyExistInMentors:
			print(i)

		message = 'updated user {}'.format(userId)
		if not projectsAddedToMentorTable:
			message = message + ', however no new projects needed to be added to mentor table'
		return res.postSuccess(message, projectsAddedToMentorTable)


#	/api/user/:userid
class apiUser(Resource):

	def get(self, userId):
		user, errors = User.queryById_user42(userId)
		if errors:
			return res.badRequestError(errors)
		return res.getSuccess('user exists in database', user)

	def post(self, userId):
		#	grab the incomming data
		data = request.get_json()
		if not data:
			return res.badRequestError("no data was provided")

		#	check if the user already exists in the database
		user, error = queryUser(userId=data.get("id_user42"))
		if user is not None:
			return res.resourceExistsError(error)

		#	load and validate the given data
		newUser, errors = user_schema.load(data)
		if errors:
			return res.badRequestError(errors)

		#	add new user to the database
		db.session.add(newUser)
		db.session.commit()

		#	check if user was added
		user, errors = User.queryById_user42(userId)
		if errors:
			return res.internalServiceError(errors)

		#	return new user
		return res.postSuccess('new user created', user)
