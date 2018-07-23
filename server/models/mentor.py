from sqlalchemy import ForeignKey, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import backref, relationship
from server.app import db

class Mentor(db.Model):
    __tablename__ = 'mentors'

    id = Column(Integer, primary_key=True, unique=True)
    id_project = Column(Integer, ForeignKey('projects.id'), nullable=False)
    id_user = Column(Integer, ForeignKey('users.id'), nullable=False)
    finalmark = Column(Integer, nullable=False)
    totalappointments = Column(Integer, nullable=False, server_default=0)
    weeklyappintments = Column(Integer, nullable=False, server_default=0)
    dailyappintments = Column(Integer, nullable=False, server_default=0)
    slot_start = Column(DateTime, nullable=False)
    slot_end = Column(DateTime, nullable=False)
    available = Column(Boolean, nullable=False, server_default=False)
    active = Column(Boolean, nullable=False, server_default=True)

    project = relationship("Project", backref-backref('mentors'))
    user = relationship("User", backref-backref('mentors'))