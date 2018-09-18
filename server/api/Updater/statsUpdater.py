from api.app import db
from api.models import User, user_schema, users_schema
from api.models import Mentor, mentor_schema, mentors_schema
from api.models import Project, project_schema, projects_schema
from api.models import MentorStat, mentorstatschema, mentorstatsshema
from api.models import Status, Appointment, appointment_schema, appointments_schema
from sqlalchemy import inspect

def UpdateMentorRating(mentorId):
    queryMentor = Mentor.query.filter_by(id=mentorId, abletomentor=True, active=True).first()
    if not queryMentor:
        return None, "Mentor {} not found".format(mentorId)
    