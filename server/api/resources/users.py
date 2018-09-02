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

#	/api/user/:login/projects/availablementors
class apiUserProjectsAvailableMentors(Resource):
	def get(self, login):

		#	Validate User exists
		user, error = User.queryByLogin(login)
		if error:
			return res.resourceMissing(error)

		#	Retrieving user projects
		records = Mentor.query.filter_by(id_user42=user['id_user42']).all()
		if not records:
			res.resourceMissing("No projects found for user {}".format(login))
		
		#	Retrieving online users
		onlineUsers = Api42.onlineUsers()

		returnList = []
		for rec in records:
			data = mentor_schema.dump(rec).data

			#	Retrieve registered users for project in 'rec'
			query = Mentor.query.filter_by(id_project42=data['id_project42'], active=True).all()
			queryData = mentors_schema.dump(query).data

			#	Matching only online users and excluding self (user with login = login)
			tmpList = [q for q in queryData for o in onlineUsers if q['id_user42'] == o['id'] and o['login'] != login]
			data['project'] = {'name': rec.project.name, 'id': rec.project.id, 'onlineMentors': len(tmpList)}
			returnList.append(data)
		return res.getSuccess(data=returnList)


#	/api/user/:login/update
class apiUserUpdate(Resource):
	def post(self, login):
		#   set defaults
		minToMentor = 90

		#	check if user exists
		user, errors = User.queryByLogin(login)
		if errors:
			return res.badRequestError(errors)
		data = Api42.userProjects(user['id_user42'])
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
			mentorQuery = Mentor.query.filter_by(id_project42=d['id_project42'], id_user42=d['id_user42']).first()
			if mentorQuery is not None:
				#	update the final mark
				mentorQuery.finalmark = d['finalmark']				
				#   set the abletomentor field to true if final mark is higher than minToMentor
				if d['finalmark'] >= minToMentor:
					mentorQuery.abletomentor = True
				projectsThatAlreadyExistInMentors.append(d['id_project42'])
				continue	# do not create a new record, and skip to the next data item

			#	Validate using mentor schema
			newMentor, error = mentor_schema.load(d)
			if error:
				db.session.rollback()
				return res.badRequestError(error)

			#   set the abletomentor field to true if final mark is higher than minToMentor
			if newMentor.finalmark >= minToMentor:
				newMentor.abletomentor = True

			#	Add new mentor to the transactional session
			db.session.add(newMentor)
			projectsAddedToMentorTable.append(newMentor)

		#	Success was achieved, so commit new records
		print('Initializing user {}. Committing to database'.format(login))
		db.session.commit()

		#	Debugging - print out project ids that failed
		print('These were the projects that do not exist in the projects database:')
		for i in failedProjectIds:
			print(i)

		#	Debugging - print out project ids that already exist for user in mentor table
		print('These were the projects that ALREADY exist for the user in the mentors database:')
		for i in projectsThatAlreadyExistInMentors:
			print(i)

		message = 'updated user {}'.format(login)
		if not projectsAddedToMentorTable:
			message = message + ', however no new projects needed to be added to mentor table'
		return res.postSuccess(message, mentors_schema.dump(projectsAddedToMentorTable).data)


#	/api/user/:login
class apiUser(Resource):

	def get(self, login):
		user, errors = User.queryByLogin(login)
		if errors:
			return res.badRequestError(errors)
		return res.getSuccess('user exists in database', user)

	def post(self, login):
		#	grab the incomming data
		data = request.get_json()
		if not data:
			return res.badRequestError("Missing data to process request")

		#	check if the user already exists in the database
		user, error = User.queryByLogin(login=data.get("login"))
		if user is not None:
			return res.resourceExistsError(error)

		print(user)
		#	********************************************************
		#	For testing purposes only ***** Remove in production
		user42 = Api42.makeRequest('/v2/users?filter[login]={}'.format(login))
		print(user42)
		data = {"login":login, "id_user42":user42[0]["id"]}
		#	********************************************************
		print("*****")
		print(data)
		#	load and validate the given data
		newUser, errors = user_schema.load(data)
		if errors:
			return res.badRequestError(errors)

		#	add new user to the database
		db.session.add(newUser)
		db.session.commit()

		#	check if user was added
		user, errors = User.queryByLogin(login)
		if errors:
			return res.internalServiceError(errors)

		#	return new user
		return res.postSuccess('new user created', user)
