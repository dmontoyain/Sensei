from .resources import *
from api.authentication import token_required

#   routes configuration
def init_routes(api):

    #   projects endpoints
    api.add_resource(apiProjects, '/projects')

    #   users endpoints
    #@token_required
    api.add_resource(apiUserPendingAppointments, '/users/<int:userId>/pendingappointments')
    api.add_resource(apiUsers, '/users')
    api.add_resource(apiUsersOnline, '/users/online')
    api.add_resource(apiUser, '/user/<login>')
    api.add_resource(apiUserLogin, '/user/login')
    api.add_resource(apiUserProjectsAvailableMentors, '/user/<login>/projects/availablementors')

    #   mentors endpoints
    api.add_resource(apiMentorPendingAppointments, '/mentors/<int:userId>/pendingappointments')
    api.add_resource(apiMentors, '/mentors')
    api.add_resource(apiMentor, '/mentor/<int:mentorId>')
    
    api.add_resource(apiMentorsProject, '/mentors/project/<int:projectId>')
    api.add_resource(apiUserMentoring, '/mentors/user/<login>/active')
    api.add_resource(apiUserCapabletoMentor, '/mentors/user/<login>/capable')

    #   appointments endpoints
    api.add_resource(apiAppointments, '/appointments')
    api.add_resource(apiAppointment, '/appointment/<int:appointmentId>')

    #   stats endpoint
    api.add_resource(apiUserStats, '/stats/<int:id_user42>/user')
    api.add_resource(apiProjectStandings, '/stats/<int:projectId>/project')
