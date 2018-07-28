import threading, time
from config.settings import apikeys
from .api42 import *

api42Requester = Api42(apikeys.uid, apikeys.secret)

class globalOnlineUsers():

    _onlineUsersList = []
    onlineMentorLock = threading.Lock() 

    @staticmethod
    def updateOnlineUsers():
        while True:
            globalOnlineUsers.onlineMentorLock.acquire()
            globalOnlineUsers._onlineUsersList = api42Requester.onlineStudents()
            globalOnlineUsers.onlineMentorLock.release()
            time.sleep(120)

    @staticmethod
    def getOnlineUsersList():
        globalOnlineUsers.onlineMentorLock.acquire()
        returnList = globalOnlineUsers._onlineUsersList
        globalOnlineUsers.onlineMentorLock.release()
        return returnList

    @staticmethod
    def run():
        threading.Thread(target=globalOnlineUsers.updateOnlineUsers).start()

from .users import *
from .projects import *
from .appointments import *
from .mentors import *

def init_routes(api):
    #   routes configuration
    #   users endpoints
    api.add_resource(userProjects, '/user/:userId/projects')
    api.add_resource(onlineUsers, '/users/online')
    api.add_resource(Users, '/users')

    #   mentors endpoints
    api.add_resource(Mentors, '/mentors')
    api.add_resource(projectMentors, '/mentors/project/<int:projectId>')
    api.add_resource(projectMentor, '/mentors/mentor/<int:mentorId>')
    api.add_resource(newMentor, '/mentor/:projectId/projects/:userId/users')
    api.add_resource(userMentors, '/mentors/user/<int:userId>')

    #   appointments endpoints
    api.add_resource(Appointments, '/appointments')

    api.add_resource(userAppointments, '/appointments/<int:userId>')
    api.add_resource(mentorAppointments, '/appointments/<int:mentorId>')
    api.add_resource(detailedAppointment, '/appointments/:appointmentId')
