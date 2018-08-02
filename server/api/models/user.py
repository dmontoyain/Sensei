from datetime import datetime
from api.db import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    id_user42 = db.Column(db.Integer, nullable=False)
    login = db.Column(db.String(45), nullable=False)

    #   relationship with 'Mentors' table, Mentor Model Class
    mentors = db.relationship('Mentor', backref='user', lazy=True)

    #   relationship with 'Appointments' table, Appointment Model Class
    #appointments = db.relationship('Appointment', backref='user', lazy=True)

    def __init__(self, id42, login):
        self.id_user42 = id42
        self.login = login

    @property
    def serialize(self):
        return {
            'id': self.id,
            'id_user42': self.id_user42,
            'login': self.login}