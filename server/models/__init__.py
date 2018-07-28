from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from models.user import User
from models.mentor import Mentor
from models.project import Project
from models.appointment import Appointment