import requests, requests_oauthlib
from api.app import db
from api.models import User, user_schema, users_schema
from api.models import Mentor, mentor_schema, mentors_schema
from api.models import Project, project_schema, projects_schema
from api.models import MentorStat, mentorstatschema, mentorstatsshema
from rq42 import Api42

finalMarkMin = 90

#	Initialize mentor stats for the specified mentor
def InitializeMentorStats(mentorId):
	mentorstatDetails = { 'id_mentor': mentorId }
	newMentorStat, err = mentorstatschema.load(mentorstatDetails)
	if err:
		print('rolling in stats..')
		db.session.rollback()
		return None, err
	db.session.add(newMentorStat)
	return newMentorStat, None

#	Joins a project and user data by saving as a mentor record in the Sensei database
def createMentorRecord(id_user42, project):
	mentorDetails = { 'id_project42': project['id_project42'], 'id_user42': id_user42, 'finalmark': project['finalmark'] }
	newMentor, err = mentor_schema.load(mentorDetails)
	if err:
		db.session.rollback()
		return None, err
	db.session.add(newMentor)
	if project['finalmark'] >= finalMarkMin:
		newMentor.abletomentor = True

	db.session.commit()

	#	Initialize mentor stats
	mentorStats, err = InitializeMentorStats(newMentor.id)
	if err:
		db.session.rollback()
		return None, err
	return newMentor, None

def loadUserProjects(id_user42):
	if not id_user42 or id_user42 < 1:
		return None, "Invalid 42 user ID !"

	#	Retrieving all projects of user been registered to Sensei for the first time
	userProjects = Api42.userProjects(id_user42)
	if not userProjects:
		return None, "No projects under user {}".format(id_user42)
	
	projectsAdded = []
	for proj in userProjects:
		queryProject = Project.query.filter_by(id_project42=proj['id_project42']).first()
		if not queryProject:
			continue
		newMentor, err = createMentorRecord(id_user42, proj)
		projectsAdded.append(newMentor)
	db.session.commit()
	return "success", None

def UpdateUserProjects(id_user42):
	if not id_user42 or id_user42 < 1:
		return None, "Invalid 42 user ID !"
	
	#	Retrieving all projects of user been registered to Sensei for the first time
	userProjects = Api42.userProjects(id_user42)
	if not userProjects:
		return "No projects under user {}".format(id_user42), None
	
	projectsUpdated = []
	projectAdded = []
	for proj in userProjects:
		#	Verifies project exists in Sensei database
		#	If it doesn't exist and it should exist, add project to database with ProjectsUpdater function in projects endpoint
		queryProject = Project.query.filter_by(id_project42=proj['id_project42']).first()
		if not queryProject:
			continue
		queryMentor = Mentor.query.filter_by(id_project42=proj['id_project42'], id_user42=id_user42).first()
		
		#	Adds project to user in Sensei database
		if not queryMentor:
			newMentor, err = createMentorRecord(id_user42, proj)
			projectAdded.append(newMentor)
			continue
		if proj['finalmark'] >= finalMarkMin and queryMentor==False:
			queryMentor.abletomentor = True
		projectsUpdated.append(queryMentor)
	db.session.commit()
	return "Successful update of user {} projects.".format(id_user42), None