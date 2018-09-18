import json
from flask import request, jsonify
from flask_restful import Resource
from api.app import db
from api.models import User, user_schema, users_schema
from api.models import Mentor, mentor_schema, mentors_schema
from api.models import Project, project_schema, projects_schema
from api.models import Status, Appointment, appointment_schema, appointments_schema
from api.models import MentorStat, mentorstatschema, mentorstatsshema
from response import Response as res

#class apiUserStats(Resource):


class apiProjectStandings(Resource):
    def get(self, projectId):

        #   Validating project exists
        queryProject = Project.query.filter_by(id_project42=projectId).first()
        if not queryProject:
            return res.resourceMissing("Project {} not found.".format(projectId))
        
        standingsList = []
        
        #   * Querying by order DESCENDING to retrieve top mentors for the specified project in each category *
        #   Top 5 ordering by rating
        topByRating = MentorStat.query \
            .join(Mentor) \
            .filter(Mentor.id_project42==projectId, Mentor.abletomentor==True) \
            .order_by(MentorStat.rating.desc(), MentorStat.totalappointments.desc()) \
            .limit(5)
        
        standingsList.append(str('topByRating'))
        standingsList.append(topByRating)

        #   Top 5 ordering by totalappointments
        topByAppointments = MentorStat.query \
            .join(Mentor) \
            .filter(Mentor.id_project42==projectId, Mentor.abletomentor==True) \
            .order_by(MentorStat.totalappointments.desc()) \
            .limit(5)
        standingsList.append(str('topByAppointments'))
        standingsList.append(topByAppointments)
        
        #   Top 5 ordering by cancelled appointments
        topByCancelledAppointments = MentorStat.query \
            .join(Mentor) \
            .filter(Mentor.id_project42==projectId, Mentor.abletomentor==True) \
            .order_by(MentorStat.cancelledappointments.desc()) \
            .limit(5)
        standingsList.append(str('topByCancelledAppointments'))
        standingsList.append(topByCancelledAppointments)

        standings = {}
        for st in standingsList:
            if type(st) is str:
                name = st
            else:
                objList = []
                for m in st:
                    mentor = mentor_schema.dump(getattr(m, 'mentor')).data
                    user = user_schema.dump(getattr(getattr(m, 'mentor'), 'user')).data
                    stats = mentorstatschema.dump(m).data
                    obj = {
                        'mentor': mentor,
                        'user': user,
                        'stats': stats
                    }
                    objList.append(obj)
                standings[name] = objList
        
        return res.getSuccess('Top 5 standings for project {}'.format(queryProject.name), standings)