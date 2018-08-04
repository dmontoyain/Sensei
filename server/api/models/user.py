from flask_marshmallow import Marshmallow
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
    #appointments = db.relationship('Appointment', backref='user', lazy=True)

    def __init__(self, id_user42, login):
        self.id_user42 = id_user42
        self.login = login
    
class UserSchema(ma.ModelSchema):
    class Meta:
        model = User

'''
    @property
    def serialize(self):
        return {
            'id': self.id,
            'id_user42': self.id_user42,
            'login': self.login}
'''
