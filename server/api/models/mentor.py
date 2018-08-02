from datetime import datetime
from api.app import db, ma

class Mentor(db.Model):
    __tablename__ = 'mentors'

    id = db.Column(db.Integer, primary_key=True)
    id_project = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
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

class MentorSchema(ma.ModelSchema):
    class Meta:
        model = Mentor

'''
@property
    def serialize(self):
        return {
            'id': self.id,
            'id_project': self.id_project,
            'id_user': self.id_user,
            'login': self.user.login,
            'finalmark': self.finalmark,
            'totalappointments': self.totalappointments,
            'weeklyappointments': self.weeklyappointments,
            'dailyappointments': self.dailyappointments,
            'slot_start': self.slot_start,
            'slot_end': self.slot_end,
            'available': self.available,
            'active': self.active,
            'started_at': self.started_at
        }
'''