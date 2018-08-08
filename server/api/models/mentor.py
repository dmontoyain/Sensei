from api.app import db, ma
from datetime import datetime
import sqlalchemy as sa

class Mentor(db.Model):
	__tablename__ = 'mentors'

	id = db.Column(db.Integer, primary_key=True)
	id_project42 = db.Column(db.Integer, db.ForeignKey('projects.id_project42'), nullable=False)
	id_user42 = db.Column(db.Integer, db.ForeignKey('users.id_user42'), nullable=False)
	finalmark = db.Column(db.Integer, nullable=False, server_default='0')
	totalappointments = db.Column(db.Integer, nullable=False, server_default='0')
	weeklyappointments = db.Column(db.Integer, nullable=False, server_default='0')
	dailyappointments = db.Column(db.Integer, nullable=False, server_default='0')
	slot_start = db.Column(db.DateTime)
	slot_end = db.Column(db.DateTime)
	abletomentor = db.Column(db.Boolean, nullable=False, server_default=sa.sql.expression.false())
	active = db.Column(db.Boolean, nullable=False, server_default=sa.sql.expression.false())
	started_at = db.Column(db.DateTime, nullable=False, server_default=sa.func.now())

	def __init__(self, id_project42, id_user42, finalmark):
		self.id_project42 = id_project42
		self.id_user42 = id_user42
		self.finalmark = 0 if finalmark is None else finalmark

	@classmethod
	def queryAll(cls):
		query = cls.query.all()
		if query is None:
			return None, "No mentors exist"
		return mentors_schema.dump(query).data, None

	@classmethod
	def queryById(cls, mentorId):
		query = cls.query.filter_by(id=mentorId).first()
		if query is None:
			return None, "No mentor with id {} was found".format(mentorId)
		return mentor_schema.dump(query).data, None

	@classmethod
	def queryManyByProject(cls, id):
		query = cls.query.filter_by(id_project42=id).all()
		if query is None:
			return None, "No mentors for project {}".format(id)
		return mentors_schema.dump(query).data, None

	@classmethod
	def queryManyByUser(cls, id):
		query = cls.query.filter_by(id_user42=id).all()
		if query is None:
			return None, "No mentors for project {}".format(id)
		return mentors_schema.dump(query).data, None

	@classmethod
	def queryByFilter(cls, **kwargs):
		query = cls.query.filter_by(**kwargs).first()
		if query is None:
			return None, "No mentor found"
		return mentor_schema.dump(query).data, None

	@classmethod
	def queryManyByFilter(cls, **kwargs):
		query = cls.query.filter_by(**kwargs).all()
		if query is None:
			return None, "No mentors found"
		return mentors_schema.dump(query).data, None


class MentorSchema(ma.ModelSchema):
	class Meta:
		model = Mentor
		include_fk = True

mentor_schema = MentorSchema()
mentors_schema = MentorSchema(many=True)