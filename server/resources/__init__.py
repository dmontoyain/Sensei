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
            globalOnlineUsers.lock()
            globalOnlineUsers._onlineUsersList = api42Requester.onlineStudents()
            globalOnlineUsers.unlock()
            time.sleep(120)
    
    #   Locks access to the _onlineMentorList
    @staticmethod
    def lock():
        globalOnlineUsers.onlineMentorLock.acquire()
    
    #   Unlocks access to the _onlineMentorList    
    @staticmethod
    def unlock():
        globalOnlineUsers.onlineMentorLock.release()

    @staticmethod
    def run():
        threading.Thread(target=globalOnlineUsers.updateOnlineUsers).start()

from .users import *
from .projects import *
from .appointments import *
from .mentors import *