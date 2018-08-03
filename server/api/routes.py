from .resources import *

#   routes configuration
def init_routes(api):

    #   projects endpoints
    api.add_resource(apiProjects, '/projects')

    #   users endpoints
    api.add_resource(apiUsers, '/users')
    api.add_resource(apiUser, '/user/<int:userId>')
    api.add_resource(apiUserProjects, '/user/<int:userId>/projects')
    api.add_resource(apiUsersOnline, '/users/online')
    api.add_resource(ApiUserInit, '/user/<int:userId>/init')

    #   mentors endpoints
    api.add_resource(apiMentors, '/mentors')
    api.add_resource(apiMentor, '/mentor/<int:mentorId>')
    api.add_resource(apiMentorsProject, '/mentors/project/<int:projectId>')
    api.add_resource(apiMentorsUser, '/mentors/user/<int:userId>')
    api.add_resource(apiMentorNew, '/mentors/project/<int:projectId>/user/<int:userId>')

    #   appointments endpoints
    api.add_resource(apiAppointments, '/appointments')
    api.add_resource(apiAppointment, '/appointment/<int:appointmentId>')
    api.add_resource(apiAppointmentsUser, '/appointments/user/<int:userId>')
    api.add_resource(apiAppointmentsMentor, '/appointments/mentor/<int:mentorId>')
