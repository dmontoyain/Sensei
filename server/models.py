import sqlalchemy as sa
from sqlalchemy import Column, String, Text, Integer, DateTime, Boolean, Numeric, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()

#   `appointments` table
class Appointment(base):
	__tablename__ = 'appointments'

	id = Column(Integer, primary_key=True)
	id_mentor = Column(Integer, ForeignKey('mentors.id'), nullable=False) 
	id_user = Column(Integer, ForeignKey('users.id'), nullable=False)
	start_time = Column(DateTime)
	feedback = Column(Text)
	rating = Column(Numeric(10, 2), nullable=False, server_default='0.00')
	status = Column(Integer, nullable=False, server_default='2')

#   `mentors` table
class Mentor(base):
	__tablename__ = 'mentors'

	id = Column(Integer, primary_key=True)
	id_project42 = Column(Integer, ForeignKey('projects.id_project42'), nullable=False)
	id_user42 = Column(Integer, ForeignKey('users.id_user42'), nullable=False)
	finalmark = Column(Integer, nullable=False, server_default='0')
	abletomentor = Column(Boolean, nullable=False, server_default=sa.sql.expression.false())
	active = Column(Boolean, nullable=False, server_default=sa.sql.expression.false())
	started_at = Column(DateTime(timezone=True), nullable=False, server_default=sa.func.now())

#   `projects` table
class Project(base):
	__tablename__ = 'projects'

	id = Column(Integer, primary_key=True)
	id_project42 = Column(Integer, unique=True, nullable=False)
	name = Column(String(100), nullable=False)
	slug = Column(String(100), nullable=False)
	tier = Column(Integer, nullable=False)
	active = Column(Boolean, nullable=False, server_default=sa.sql.expression.true())

#   `users` table
class User(base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True)
	id_user42 = Column(Integer, unique=True, nullable=False)
	login = Column(String(45), nullable=False)
	last_seen = Column(DateTime(timezone=True), nullable=False, server_default=sa.func.now())
	active = Column(Boolean, nullable=False, server_default=sa.sql.expression.true())
