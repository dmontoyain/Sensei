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

	#	updates the projects that exist in the projects table
	def post(self):
		#	Check if any projects exist
		existingProjects, error = Project.queryAll()
		if error:
			return res.internalServiceError(error)

		#	get existing projects from 42 API
		data = Api42.allProjects()
		if data is None:
			return res.internalServiceError("unable to query the 42 API")

		#	only add new projects that are not in the projects table
		newProjects = []
		existingProjects = []
		for d in data:
			#	check if project exists
			projectCheck = Project.query.filter_by(id_project42=d['id_project42'])

			#	validate and create new project record
			newProject, error = project_schema.load(d) #Project(d['id_project42'], d['name'], d['slug'], d['tier'])
			if error:
				db.session.rollback()
				return res.internalServiceError('bad data')

			#	only add the new projects that don't exist in the database
			if not projectCheck:
				db.session.add(newProject)
				newProjects.append(project_schema.dump(newProject).data)
			else:
				existingProjects.append(project_schema.dump(newProject).data)

		print("COMMITTING NEW PROJECTS")
		db.session.commit()

		#   change return message if projects were updated
		retMessage = 'created new project' if newProjects else 'no new projects needed to be updated'
		retData = {'newProjects': newProjects, 'existingProjects': existingProjects}
		return res.postSuccess(retMessage, retData)


#	LOAD takes a python DICTIONARY of data and will return a new CLASS object (the 'record')
#	DUMP takes a CLASS object (the 'record') and returns a tuple of data and something else