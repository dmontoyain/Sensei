from datetime import datetime
import sys
import time
import requests
import itertools
import threading
import api42config
import gc
from terminalcolors import *

class Api42:

	#	Lambda helper funcs
	_currentMilliTime	= lambda: int(round(time.time() * 1000))
	_dataList			= lambda data: [data] if type(data) is dict else data
	_chainToList		= lambda chainData: [d for d in chainData]

	#	Online User handling
	_onlineUsers		= []
	_onlineUsersLock	= threading.Lock()
	_timeBetweenUpdates = 0
	_activeUpdater		= False

	#	Api 
	_token				= None
	_tokenExpires		= 0
	_apiLimit			= int(0.5 * 1000)
	_lastCall			= 0
	_totalRequests		= 0

	#	Api constants
	_endpoint			= 'https://api.intra.42.fr'
	_headers			= { 'Authorization': 'Bearer',
							'content-type': 'application/x-www-form-urlencoded' }
	_authData			= { 'client_id': api42config._uid,
							'client_secret': api42config._secret,
							'grant_type': 'client_credentials' }

	#	Static Methods that control the online users list
	#	-------------------------------------------------------------------------------------------

	@staticmethod
	def updateOnlineUsers(runForever=False):
		#	Only lock on the first request
		Api42.lock()
		data = Api42.makeRequest('/v2/campus/7/locations?filter[active]=true')
		Api42._onlineUsers = [{'login': i['user']['login'], 'id': i['user']['id'], 'host': i['host'] } for i in data]
		Api42.unlock()
		del data[:]
		#	If a user calls this function directly, default to only making the single request. Else, run forever.
		while runForever:
			#	Sleep. Default 120 secs
			time.sleep(Api42._timeBetweenUpdates)

			#	Request in unlocked state
			data = Api42.makeRequest('/v2/campus/7/locations?filter[active]=true')

			#	Lock when Api42._onlineUsers list itself is being modified
			Api42.lock()
			del Api42._onlineUsers[:]
			Api42._onlineUsers = [{'login': i['user']['login'], 'id': i['user']['id'], 'host': i['host'] } for i in data]
			Api42.unlock()

			#	Free some memory for funsies
			del data[:]
			gc.collect()

		#	Return if user simply wants to call the update function once
		return Api42._onlineUsers

	@staticmethod
	def lock():
		Api42._onlineUsersLock.acquire()

	@staticmethod
	def unlock():
		Api42._onlineUsersLock.release()

	@staticmethod
	def runActiveUserUpdater(timeBetweenUpdates=120):
		Api42._activeUpdater = True
		Api42._timeBetweenUpdates = timeBetweenUpdates
		threading.Thread(target=Api42.updateOnlineUsers, args=[True]).start()

	#	Api Functionality begins here
	#	-----------------------------------------------------------------------------------------

	@staticmethod
	def makeRequest(endpoint):	# For general GET requests that require a single endpoint

		#	If a new token is needed, update it
		Api42._updateToken()

		#	Make get request
		returnData = Api42.get(endpoint, None, Api42._headers)

		#	If the request failed, but it had to update the token, perform request again
		if returnData is None and Api42._updateToken():
			returnData = Api42.get(endpoint, None, Api42._headers)

		#	Returns a list of request data, or None if it failed
		return returnData

	@staticmethod
	def get(url, data, headers):	# Calls send with the GET method
		return Api42._send('GET', url, data, headers)


	@staticmethod
	def post(url, data, headers):	# Calls send with the POST method
		return Api42._send('POST', url, data, headers)


	@staticmethod
	def _send(method, url, data, headers):	# In-between method for the get and post methods

		#	Make request
		rsp, returnData = Api42._request(method, Api42._endpoint + url, data, headers)
		if rsp is None:
			return None

		#	Loop to get all data
		while 'next' in rsp.links:
			rsp, tmpData = Api42._request(method, rsp.links['next']['url'], data, headers)
			if rsp is None:
				return None
			returnData = itertools.chain(returnData, tmpData)
		return Api42._chainToList(returnData)


	#	First it waits,
	#	then makes an actual request,
	#	returns the response and list of data
	@staticmethod
	def _request(method, url, data, headers):

		#	Pausing for the api request limit (500 milliseconds)
		while (Api42._currentMilliTime() - Api42._apiLimit) < Api42._lastCall:
			pass
		Api42._lastCall = Api42._currentMilliTime()

		#	Making the request - only handles get and post requests for now
		print(IYELLOW + "Requesting data from... " + ICYAN + url + ENDCOLOR + ' ', end='')
		sys.stdout.flush()
		rsp = requests.request(method, url=url, data=data, headers=headers)
		Api42._totalRequests += 1

		#	Error handling
		if (rsp is None) or rsp.status_code != 200:
			print(BRED + "...Failed!" + ENDCOLOR)
			return None, None

		#	Returning the response object AND a list of data
		print(BGREEN + "...Success!" + ENDCOLOR)
		return rsp, Api42._dataList(rsp.json())


	@staticmethod
	def _updateToken():	# Returns True if token was updated, otherwise returns False

		#	Check to see if token needs to be updated
		if Api42._currentMilliTime() >= Api42._tokenExpires:
			print(IPURPLE + "Token needs refreshing..." + ENDCOLOR)
			tokenData = Api42.post('/oauth/token', Api42._authData, None)
			if tokenData is None:
				print(IRED + "Failed to refresh the 42 api token" + ENDCOLOR)
				return False

			#	Update token, expiry time, and authorization header
			Api42._token = tokenData[0]['access_token']
			Api42._tokenExpires = (tokenData[0]['expires_in'] * 1000) + Api42._currentMilliTime()
			Api42._headers['Authorization'] = 'Bearer ' + Api42._token
			print(IGREEN + "Token Updated!" + ENDCOLOR)
			return True
		return False


	#	A few predefined requests with parsed responses
	#	-------------------------------------------------------------------------------------------

	@staticmethod
	def onlineStudents():
		#	If the active updater is not running, then update the internal list
		if not Api42._activeUpdater:
			Api42.updateOnlineUsers()
		#	Lock, then deepcopy the internal list
		Api42.lock()
		onlineUsersCopy = copy.deepcopy(Api42._onlineUsers)
		Api42.unlock()
		return onlineUsersCopy

	@staticmethod
	def onlineStudentsAtCampus(campusID):
		return Api42.makeRequest('/v2/campus/' + str(campusID) + '/locations?filter[active]=true')

	@staticmethod
	def passingProjectsForUser(userID):
		return Api42.makeRequest('/v2/users/' + str(userID) + '/projects_users?range[final_mark]=80,125&filter[cursus]=1')

	@staticmethod
	def projectsForUserInFinalMarkRange(userID, minScore, maxScore):
		data = Api42.makeRequest('/v2/users/' + str(userID) + '/projects_users?range[final_mark]=' + str(minScore) + ',' + str(maxScore))
		return [i['project']['name'] for i in data]

	@staticmethod
	def allProjects():
		return Api42.makeRequest('/v2/cursus/1/projects')
	
	#	For grabbing the list of open projects a user has.  For the purposes of assignment and all that good stuff
	@staticmethod
	def	openProjectsForUser(userID):
		data = Api42.makeRequest('/v2/users/' + str(userID) + '/projects_users')
		return ([i['project']['name'] for i in data if i['status'] == 'in_progress'])
