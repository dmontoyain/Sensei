from api.app import db, ma
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.orm import backref

class MentorStat(db.Model):
    __tablename__ = 'mentorstats'

    id = db.Column(db.Integer, primary_key=True)
    id_mentor = db.Column(db.Integer, db.ForeignKey('mentors.id'), nullable=False)
    rating = db.Column(db.Numeric(10, 2, asdecimal=False), nullable=False, server_default='0.00')
    totalappointments = db.Column(db.Integer, nullable=False, server_default='0')
    cancelledappointments = db.Column(db.Integer, nullable=False, server_default='0')

    #   relationship with 'mentors' table, Mentor Model Class
    mentor = db.relationship('Mentor', backref= backref('mentorstat', lazy='joined'), lazy=True)

    def __init__(self, id_mentor):
        self.id_mentor = id_mentor

class MentorStatSchema(ma.ModelSchema):
    class Meta:
        model=MentorStat
        include_fk=True

mentorstatschema = MentorStatSchema()
mentorstatsshema = MentorStatSchema(many=True)