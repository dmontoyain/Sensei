import json
from flask import request
from flask_restful import Resource
from api.app import db, app
from api.models import User, user_schema, users_schema
from api.models import Mentor, mentor_schema, mentors_schema
from api.models import Project, project_schema, projects_schema
from api.models import Status, Appointment, appointment_schema, appointments_schema
from rq42 import Api42
from response import Response as res
from api.authentication import token_required
import requests
from api.Updater import userUpdater
from requests_oauthlib import OAuth2Session

#	Registers user to sensei database
def registerUser(LoggedUser):
	userDetails = { 'id_user42' : LoggedUser['id'], 'login': LoggedUser['login'] }
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
		if not accessReq or 'error' in accessReq:
			return res.badRequestError(message=accessReq['error_description'])
		LoggedUser = requests.get('https://api.intra.42.fr/v2/me', headers= { 'Authorization' : 'Bearer {}'.format(accessReq['access_token'])}).json()
		
		queryUser = User.query.filter_by(id_user42=LoggedUser['id']).first()
		err = None
		#	Registers user if record doesn't exist in Sensei database
		if not queryUser:
			data, err = registerUser(LoggedUser)
			
		#print(LoggedUser)
		return res.postSuccess(data={'access': accessReq, 'user': LoggedUser, 'error': err})


#	/api/user/:login
class apiUser(Resource):
	def get(self, login):
		user, err = User.queryByLogin(login)
		if err:
			return res.resourceMissing(err)
		return res.getSuccess('user exists in database', user)


#	api/users/:userId/pendingappointments	
class apiUserPendingAppointments(Resource):
	def get(self, userId):
		query = (db.session.query(Appointment).join(Mentor).join(User).filter(User.id_user42==userId, Appointment.status==Status.Pending)).all()
		for q in query:
			print(q.__dict__)
		print(appointments_schema.dump(query).data)
		queryUser = User.query.join(Appointment, Appointment.id_user==User.id).filter(User.id_user42==userId, Status.Pending).first()
		if not queryUser:
			return res.resourceMissing("No appointments")
		pendingappointments = []
		user = user_schema.dump(queryUser).data
		for a in user['appointments']:
			queryAppnt = Appointment.query.filter_by(id=a).first()
			queryMentor = Mentor.query.filter_by(id=queryAppnt.id_mentor).first()
			queryUserMentoring = User.query.filter_by(id_user42=queryMentor.id_user42).first()
			queryProject = Project.query.filter_by(id_project42=queryMentor.id_project42).first
			pendingappointments.append({
				'appointment' : appointment_schema.dump(queryAppnt).data,
				'userMentoring' : user_schema.dump(queryUserMentoring).data,
				'project' : project_schema.dump(queryProject).data
			})
		return res.getSuccess(message="Appointmensts as user for user {}".format(user['login']), data=pendingappointments)
