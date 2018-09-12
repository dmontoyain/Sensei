import json
from flask import request
from flask_restful import Resource
from api.app import db, app
from api.models import User, user_schema, users_schema
from api.models import Mentor, mentor_schema, mentors_schema
from api.models import Project, project_schema, projects_schema
from api.models import Appointment, appointment_schema, appointments_schema
from rq42 import Api42
from response import Response as res
from api.authentication import token_required
import requests
from api.Updater import userUpdater
from requests_oauthlib import OAuth2Session

#	Registers user to sensei database
def registerUser(LoggedUser):
	userDetails = { 'id_user42' : LoggedUser.id, 'login': LoggedUser.login }
	newUser, err = user_schema.load(userDetails)
	if err:
		return res.internalServiceError("Error saving user")
	db.session.add(newUser)
	db.session.commit()
	data, err = userUpdater.loadUserProjects(newUser.id_user42)
	if err:
		return None, err
	return data, None

#	/api/users
class apiUsers(Resource):
	#	Returns all users in the database

	def get(self, currentuser):
		query = User.query.all()
		data = users_schema.dump(query).data
		return res.getSuccess('all users', data)

#	/api/users/online
class apiUsersOnline(Resource):

	#	Return all online users
	def get(self):
		queryUsers, error = User.queryByAll()
		if error:
			return res.internalServiceError(error)
		onlineStudents = Api42.onlineUsers()
		onlineSenseiUsers = [u for u in queryUsers for o in onlineStudents if u['id_user42'] == o['id']]
		return res.getSuccess(data=onlineSenseiUsers)
		

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

#	/api/user/login
class apiUserLogin(Resource):

	def get(self):
		print("REDIRECTTTTT")
		data = request.get_json()
		print(data)
		data = request.args
		print(data)

	#	
	def post(self):
		
		data = request.get_json()
		print(data.get('code'))

		if not data or not data.get("code"):
			return res.badRequestError(message="No authorizen token provided.")

		accessReq = requests.post('https://api.intra.42.fr/oauth/token', data= {
			'grant_type' : 'authorization_code',
			'client_id' : app.config['CLIENT_ID'],
			'client_secret' : app.config['CLIENT_SECRET'],
			'code' : data.get('code'),
			'redirect_uri' : "http://localhost:8080/auth"
		}).json()
		print(accessReq)
		if not accessReq or 'error' in accessReq:
			return res.badRequestError(message=accessReq['error_description'])
		LoggedUser = requests.get('https://api.intra.42.fr/v2/me', headers= { 'Authorization' : 'Bearer {}'.format(accessReq['access_token'])}).json()
		
		queryUser = User.query.filter_by(id_user42=LoggedUser.id).first()

		#	Registers user if record doesn't exist in Sensei database
		if not queryUser:
			data, err = registerUser(LoggedUser)
			
		print(LoggedUser)
		return res.postSuccess(data={'access': accessReq, 'user': LoggedUser, 'error': err})
		
#https://signin.intra.42.fr/users/sign_in?redirect_to=https%3A%2F%2Fapi.intra.42.fr%2Foauth%2Fauthorize%3Fclient_id%3Da740cef6c7a0415b1524701c5a9a2fce778879c90b77b0ab67b068858948677a%26redirect_uri%3Dhttp%253A%252F%252Fcantina.42.us.org%252Fusers%252Fauth%252Fmarvin%252Fcallback%26response_type%3Dcode%26state%3D187f5f897d776f69bf25443558eae6acedf4f18a4585f78f
#	/api/user/:login/update
class apiUserUpdate(Resource):
	def post(self, login):

		#	check if user exists
		user, err = User.queryByLogin(login)
		if err:
			return res.badRequestError(err)
			
		#	User records updating
		msg, err = userUpdater.UpdateUserProjects(user['id_user42'])
		if err:
			return res.internalServiceError(err)
		return res.postSuccess(msg)


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
