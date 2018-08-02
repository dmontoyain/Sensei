from flask_restful import Resource
from api.models import User, Project
from rq42 import Api42
from flask import request

#   /api/users
class apiUsers(Resource):
    #   Returns all users in the database
    def get(self):
        query = User.query.all()
        return [u.serialize for u in query], 200

    #   Creates a new user
    def post(self):
        pass
        # json_data = request.get_json(force=True)
        # if not json_data:
        #     return {'message': 'No input data provided'}, 400
        # # Validate and deserialize input
        # data, errors = comment_schema.load(json_data)
        # if errors:
        #     return {"status": "error", "data": errors}, 422
        # category_id = Category.query.filter_by(id=data['category_id']).first()
        # if not category_id:
        #     return {'status': 'error', 'message': 'comment category not found'}, 400
        # comment = Comment(
        #     category_id=data['category_id'], 
        #     comment=data['comment']
        #     )
        # db.session.add(comment)
        # db.session.commit()

        # result = comment_schema.dump(comment).data

        # return {'status': "success", 'data': result}, 201



#	/api/user/:userid
class apiUser(Resource):
	def get(self, userId):
		query = User.query.filter_by(id=userId).serialize
		data = api42Requester.makeRequest("/")	
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
