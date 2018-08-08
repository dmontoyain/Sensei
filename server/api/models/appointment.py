from api.app import db, ma
from datetime import datetime, timedelta

class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    id_mentor = db.Column(db.Integer, db.ForeignKey('mentors.id'), nullable=False) 
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_time = db.Column(db.DateTime)
    feedback = db.Column(db.Text)

    def __init__(self, mentorid, userid, feedback=""):
        self.id_mentor = mentorid
        self.id_user = userid
        self.feedback = feedback
    
    @classmethod
	def queryAll(cls):
		query = cls.query.all()
		if query is None:
			return None, "No appointments exist"
		return appointments_schema.dump(query).data, None
    
    @classmethod
	def queryById(cls, appId):
		query = cls.query.filter_by(id=appId).first()
		if query is None:
			return None, "Appointment with id {} does not exist".format(appId)
		return appointment_schema.dump(query).data, None

class AppointmentSchema(ma.ModelSchema):
    class Meta:
        model = Appointment
        include_fk = True

appointment_schema = AppointmentSchema()
appointments_schema = AppointmentSchema(many=True)