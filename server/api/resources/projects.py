import json
from flask import request
from flask_restful import Resource
from api.app import db
from api.models import User, user_schema, users_schema
from api.models import Mentor, mentor_schema, mentors_schema
from api.models import Project, project_schema, projects_schema
from api.models import Appointment, appointment_schema, appointments_schema
from rq42 import Api42
from response import Response as res


#   api/projects
class apiProjects(Resource):
    def get(self):
        data, error = Project.queryAll()
        if error:
            return res.internalServiceError(error)
        return res.getSuccess('found projects', data)

    def post(self):
        # add filter to find if project already exists
        data = Api42.allProjects()
        if data is None:
            return res.internalServiceError("unable to query the 42 API")

        newProjects = []
        for d in data:
            newProject = Project(d['id_project42'], d['name'], d['slug'], d['tier'])
            db.session.add(newProject)
            newProjects.append(newProject)

        db.session.commit()

        #   change return message if projects were updated
        retMessage = 'created new project' if newProjects else 'no new projects were updated'
        return res.postSuccess(retMessage, newProjects)
     