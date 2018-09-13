from api.app import db, ma
from datetime import datetime, timedelta
import sqlalchemy as sa

class Appointment(db.Model):
	__tablename__ = 'appointments'

	id = db.Column(db.Integer, primary_key=True)
	id_mentor = db.Column(db.Integer, db.ForeignKey('mentors.id'), nullable=False) 
	id_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	start_time = db.Column(db.DateTime)
	feedback = db.Column(db.Text)
	status = db.Column(db.Integer, nullable=False, server_default='2')

	def __init__(self, id_mentor, id_user, feedback=""):
		self.id_mentor = id_mentor
		self.id_user = id_user
		self.feedback = feedback

	#   Creates an appointment for given user and mentor
	#   Sets up an appointment 15 minutes from actual date
	@classmethod
	def createAppointment(cls, mentorId, userId):
		data = {"id_mentor": mentorId, "id_user": userId}
		newappointment, error = appointment_schema.load(data)
		if error:
			return None, error
		#creates an appointment 15 minutes ahead from creation
		newappointment.start_time = datetime.now() + timedelta(minutes=15)
		db.session.add(newappointment)
		db.session.commit()
		return appointment_schema.dump(newappointment).data, None

	@classmethod
	def queryCountProjectAppointmentsbyUser(cls, projectId, userId):
		from api.models import Mentor
		dateObject = datetime.now().date()
		today = datetime(dateObject.year, dateObject.month, dateObject.day)
		appointmentCount = cls.query.join(Mentor, cls.id_mentor == Mentor.id).filter(Mentor.id_project42 == projectId, cls.id_user == userId, cls.start_time > today).count()
		return appointmentCount

	 #   Query one appointment with the given 'id' parameter
	@classmethod
	def queryById(cls, appointmentId):
		query = cls.query.filter_by(id=appointmentId).first()
		if not query:
			return None, "No appointment with id {} was found".format(appointmentId)
		return appointment_schema.dump(query).data, None

	#   Query all appointments with the given parameters for a user (mentee) perspective
	@classmethod
	def queryManyAsUser(cls, userId):
		query = cls.query.filter(cls.id_user==userId).all()
		if not query:
			return None, "No appointments for user {}".format(userId)
		return appointments_schema.dump(query).data, None

	#   Query all appointments with the given parameters from a mentor perspective
	@classmethod
	def queryManyAsMentor(cls, userId):
		from api.models import Mentor
		query = cls.query.join(Mentor, cls.id_mentor == Mentor.id).filter(Mentor.id_user42 == userId).all()
		if not query:
			return None, "No appointments to mentor for user {}".format(userId)
		return appointments_schema.dump(query).data, None

	#   Query multiple *PENDING* appointments with the given parameters from a user perspective
	@classmethod
	def queryManyPendingAsUser(cls, userId):
		query = cls.query.filter(cls.id_user==userId, cls.status == 2).all()
		if not query:
			return None, "No pending appointments requested by user {}".format(userId)
		return appointments_schema.dump(query).data, None

	#   Query multiple *PENDING* appointments with the given parameters from a mentor perspective
	@classmethod
	def queryManyPendingAsMentor(cls, userId):
		from api.models import Mentor, User
		query = cls.query.join(Mentor).join(User, Mentor.id_user42==User.id_user42).filter(Mentor.id_user42 == userId, cls.status == 2).all()
		#query = cls.query.join(Mentor, cls.id_mentor == Mentor.id).filter(Mentor.id_user42 == userId, cls.status == 2).all()
		query = cls.query.join(Mentor)
		if not query:
			return None, "No pending appointments to mentor for user {}".format(userId)
		return appointments_schema.dump(query).data, None

class AppointmentSchema(ma.ModelSchema):
	class Meta:
		model = Appointment
		include_fk = True

appointment_schema = AppointmentSchema()
appointments_schema = AppointmentSchema(many=True)