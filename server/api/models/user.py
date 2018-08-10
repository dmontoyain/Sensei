from api.app import db, ma
from datetime import datetime

class User(db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	id_user42 = db.Column(db.Integer, unique=True, nullable=False)
	login = db.Column(db.String(45), nullable=False)
	
	#   relationship with 'Mentors' table, Mentor Model Class
	mentors = db.relationship('Mentor', backref='user', lazy=True)

	#   relationship with 'Appointments' table, Appointment Model Class
	appointments = db.relationship('Appointment', backref='user', lazy=True)

	def __init__(self, id_user42, login):
		self.id_user42 = id_user42
		self.login = login

	@classmethod
	def queryByAll(cls):
		query = cls.query.all()
		if query is None:
			return None, "User table is empty"
		return users_schema.dump(query).data, None

	@classmethod
	def queryById(cls, userId):
		query = cls.query.filter_by(id=userId).first()
		if query is None:
			return None, "No user with id {} was found".format(id)
		return user_schema.dump(query).data, None

	@classmethod
	def queryById_user42(cls, userId):
		query = cls.query.filter_by(id_user42=userId).first()
		if query is None:
			return None, "No user with id_user42 {} was found".format(userId)
		return user_schema.dump(query).data, None

	@classmethod
	def queryByLogin(cls, login):
		query = cls.query.filter_by(login=login).first()
		if query is None:
			return None, "No user with login {} was found".format(login)
		return user_schema.dump(query).data, None

	@classmethod
	def queryByFilter(cls, **kwargs):
		query = cls.query.filter_by(**kwargs).first()
		if query is None:
			return None, "No user found"
		return user_schema.dump(query).data, None


class UserSchema(ma.ModelSchema):
	class Meta:
		model = User
		include_fk = True


user_schema = UserSchema()
users_schema = UserSchema(many=True)