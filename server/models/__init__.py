from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

import models
from models import *
from models.user import User
from models.project import Project
from models.mentor import Mentor
from models.appointment import Appointment