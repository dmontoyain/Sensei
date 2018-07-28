from models import db

class Appointment(db.Model):
    __tablename__ = 'Appointments'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    id_mentor = db.Column(db.Integer, db.ForeignKey('Mentors.id'), nullable=False) 
    id_user = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    feedback = db.Column(db.Text, nullable=False)