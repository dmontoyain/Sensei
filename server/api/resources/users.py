from flask import request, jsonify
from flask_restful import Resource
from api.models import Mentor, MentorSchema, User, UserSchema, Project
from rq42 import Api42
from api.app import db

#   queries sensei database for user specified by userId
def queryUser(userId=None, login=None):
    if login is None:
        query = User.query.filter_by(id_user42=userId).first()
    else:
       query = User.query.filter_by(login=login).first() 
    print("query sqlalchemy")
    if (query is None):
        return None, "No User Found for userid42"
    user_schema = UserSchema()
    return user_schema.dump(query)

def formatError(err, errorMessage):
    if errorMessage is not '':
        return '{}. {}'.format(err, errorMessage)
    return err

def internalServiceError(errorMessage=''):
    return {'error': formatError('Internal API Service Error', errorMessage)}, 500

def badRequestError(errorMessage=''):
    return {'error': formatError('Bad Request for API Service', errorMessage)}, 400

def resourceExistsError(errorMessage=''):
    return {'error': formatError('Resource already exists', errorMessage)}, 418

#   /api/users
class apiUsers(Resource):
    #   Returns all users in the database
    def get(self):
        query = User.query.all()
        return [u.serialize for u in query], 200

#   /api/user/:userId/init
class ApiUserInit(Resource):
    def post(self, userId):
        data = Api42.userProjects(userId)
        if data is None:
            return formatError('Error', 'No projects found for user')
        for d in data:
            query = Project.query.filter_by(id_project42 = d.id_project42).first()
            if query is not None:
                db.session.add(d)
        print('Added mentors to session...going to commit')
        db.session.commit()
        return {"status":"user initialization successful"}, 201

#   /api/user/:userid
class apiUser(Resource):

    def get(self, userId):
        user, errors = queryUser(userId)
        print(errors)
        if errors:
            return {"status":"error", "data":errors}, 422
        return jsonify(user), 200
    
    def post(self, userId):
        #   grab the incomming data
        data = request.get_json()
        print(type(data))
        print(data)
        if not data:
            return badRequestError()

        #   check if the user already exists in the database
        user, errors = queryUser(userId=data.get("id_user42"))
        if user is not None:
            return resourceExistsError()
        user, errors = queryUser(login=data.get("login"))
        if user is not None:
            return resourceExistsError()

        #   load and validate the given data
        user_schema = UserSchema()
        newUser, errors = user_schema.load(data)
        if errors:
            return internalServiceError(errors)
        
        #   add new user to the database
        db.session.add(newUser)
        db.session.commit()

        #   check if user was added
        user, errors = queryUser(userId)
        if (errors):
            return internalServiceError("Unable to return saved error")

        #   return new user
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