from .resources import *

#   routes configuration
def init_routes(api):

    #   projects endpoints
    api.add_resource(apiProjects, '/projects')

    #   users endpoints
    api.add_resource(apiUsers, '/users')
    api.add_resource(apiUser, '/user/<int:userId>')
    api.add_resource(apiUserUpdate, '/user/<int:userId>/update')

    #   mentors endpoints
    api.add_resource(apiMentors, '/mentors')
    api.add_resource(apiMentor, '/mentor/<int:mentorId>')
    api.add_resource(apiSubscribeUnSubscribeMentor, '/mentor/<int:mentorId>/subscribeunsubscribe')
    api.add_resource(apiSubscribeMentor, '/mentor/<int:mentorId>/subscribe')
    api.add_resource(apiUnsubscribeMentor, '/mentor/<int:mentorId>/unsubscribe')
    api.add_resource(apiMentorsProject, '/mentors/project/<int:projectId>')
    api.add_resource(apiUserMentoring, '/mentors/user/<int:id_user42>/active')
    api.add_resource(apiUserCapabletoMentor, '/mentors/user/<int:id_user42>/capable')

    #   appointments endpoints
    api.add_resource(apiAppointments, '/appointments')
    api.add_resource(apiAppointment, '/appointment/<int:appointmentId>')
    api.add_resource(apiAppointmentsAsUser, '/appointments/user/<login>')
    api.add_resource(apiAppointmentsAsMentor, '/appointments/mentor/<login>')

    api.add_resource(apiPendingAppointmentsAsMentor, '/appointments/pending/mentor/<login>')
    api.add_resource(apiPendingAppointmentsAsUser, '/appointments/pending/user/<login>')
