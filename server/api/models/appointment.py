from datetime import datetime, timedelta
from api.app import db, ma

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

class AppointmentSchema(ma.ModelSchema):
    class Meta:
        model = Appointment