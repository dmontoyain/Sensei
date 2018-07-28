from datetime import datetime
from models import db

class Mentor(db.Model):
    __tablename__ = 'Mentors'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    id_project = db.Column(db.Integer, db.ForeignKey('Projects.id'), nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    finalmark = db.Column(db.Integer, nullable=False)
    totalappointments = db.Column(db.Integer, nullable=False, default=0)
    weeklyappointments = db.Column(db.Integer, nullable=False, default=0)
    dailyappointments = db.Column(db.Integer, nullable=False, default=0)
    slot_start = db.Column(db.DateTime, nullable=False)
    slot_end = db.Column(db.DateTime, nullable=False)
    available = db.Column(db.Boolean, nullable=False, default=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    started_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    #   relationship with 'Appointments' table, Appointment Model class
    #project = db.relationship("Project", foreign_keys=[id_project])
    #user = db.relationship("User", foreign_keys=[id_user])
    #appointments = db.relationship('Appointment', backref='mentor', lazy=True)