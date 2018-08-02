from datetime import datetime
from api.db import db

class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    id_mentor = db.Column(db.Integer, db.ForeignKey('mentors.id'), nullable=False) 
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    feedback = db.Column(db.Text, nullable=False)

    def __init__(self, mentorid, userid, starttime, feedback):
        self.id_mentor = mentorid
        self.id_user = userid
        self.start_time = starttime
        self.feedback = feedback