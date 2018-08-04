from datetime import datetime
import sqlalchemy as sa
from api.app import db, ma

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

class MentorSchema(ma.ModelSchema):
    class Meta:
        model = Mentor
        include_fk = True
