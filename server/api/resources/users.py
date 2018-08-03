from flask import request, jsonify
from flask_restful import Resource
from api.models import User, UserSchema, Project
from rq42 import Api42
from api.app import db

#   queries sensei database for user specified by userId
def queryUser(userId):
    query = User.query.filter_by(id_user42=userId).first()
    print("query sqlalchemy")
    if (query is None):
        return None, "No User Found for userid42"
    user_schema = UserSchema()
    return user_schema.dump(query)

def internalServiceError(errorMessage=""):
    return {"status":"Internal API Service Error. " + errorMessage}, 500

def badRequestError(errorMessage=""):
    return {"status":"Bad Request for API Service. " + errorMessage}, 400

#   /api/users
class apiUsers(Resource):
    #   Returns all users in the database
    def get(self):
        query = User.query.all()
        return [u.serialize for u in query], 200

#	/api/user/:userid
class apiUser(Resource):

    #   ON GET
    def get(self, userId):
        user, errors = queryUser(userId)
        print(errors)
        if errors:
            return {"status":"error", "data":errors}, 422
        return jsonify(user), 200
    
    #   ON POST
    def post(self, userId):
        data = request.get_json()
        if not data:
            return badRequestError()
        user, errors = queryUser(userId)
        if user is not None:
            return {"status":"User already created"}, 400
        print("here111")
        user_schema = UserSchema()
        newUser, errors = user_schema.load(data)
        print("finished loadhere")
        if errors:
            return {"status":"error", "data":errors}, 422
        #User(userId, request.form['login'])
        db.session.add(newUser)
        db.session.commit()
        print("saved")
        user, errors = queryUser(userId)
        print (user)
        if (errors):
            return internalServiceError("Unable to return saved error")
        return user, 201


#   /api/user/:userid/projects
class apiUserProjects(Resource):
    def get(self, userId):
        return User.query.all(), 200


#   /api/users/online
class apiUsersOnline(Resource):
    def get(self):
        allUsers = User.query.all().serialize
        onlineUsers = Api42._onlineUsers
        result = [u.serialize for u in allUsers for x in onlineUsers if u.id_user42 == x['id']]
        return result, 200
