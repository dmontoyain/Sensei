from flask_restful import Resource
from models import User, Project
from resources import api42Requester


#   /api/users
class apiUsers(Resource):
    def get(self):
        query = User.query.all()
        return [u.serialize for u in query], 200


#	/api/user/:userid
class apiUser(Resource):
	def get(self, userId):
		query = User.query.filter_by(id=userId).serialize
		data = apiRequester.makeRequest("/")	
		return [d['af'] for d in data], 200


#   /api/user/:userid/projects
class apiUserProjects(Resource):
    def get(self, userId):
        return User.query.all(), 200


#   /api/users/online
class apiUsersOnline(Resource):
    def get(self):
        allUsers = User.query.all().serialize
        globalOnlineUsers.lock()
        onlineUsers = globalOnlineUsers._onlineUsersList
        result = [u.serialize for u in allUsers for x in onlineUsers if u.id_user42 == x['id']]
        globalOnlineUsers.unlock()
        return result, 200
