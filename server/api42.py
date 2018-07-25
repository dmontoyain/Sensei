from datetime import datetime
import sys
import time
import json
import requests
import itertools
import apikeys
from terminalcolors import *


class Api42:

	_currentMilliTime	= lambda: int(round(time.time() * 1000))
	_dataList			= lambda data: [data] if type(data) is dict else data
	_chainToList		= lambda chainData: [d for d in chainData]

	def __init__(self, uid, secret):
		self.token = None
		self.tokenExpires = 0
		self.apiLimit = int(0.5 * 1000)
		self.lastCall = 0
		self.totalRequests = 0
		self.endpoint = 'https://api.intra.42.fr'
		self.headers = {
			'Authorization': 'Bearer',
			'content-type': 'application/x-www-form-urlencoded'
		}
		self.authData = {
			'client_id': uid,
			'client_secret': secret,
			'grant_type': 'client_credentials'
		}


	def updateToken(self):	# Returns True if token was updated, otherwise returns False

		#	Check to see if token needs to be updated
		if Api42._currentMilliTime() >= self.tokenExpires:
			print(IPURPLE + "Token needs refreshing..." + ENDCOLOR)
			tokenData = self.post('/oauth/token', self.authData, None)
			if tokenData is None:
				return

			#	Update token, expiry time, and authorization header
			self.token = tokenData[0]['access_token']
			self.tokenExpires = (tokenData[0]['expires_in'] * 1000) + Api42._currentMilliTime()
			self.headers['Authorization'] = 'Bearer ' + self.token
			print(IGREEN + "Token Updated!" + ENDCOLOR)
			return True
		return False


	def makeRequest(self, endpoint):	# For general GET requests that require a single endpoint

		#	If a new token is needed, update it
		self.updateToken()

		#	Make get request
		returnData = self.get(endpoint, None, self.headers)

		#	If the request failed, but it had to update the token,
		#	try and perform the request again
		if returnData is None and self.updateToken():
			returnData = self.get(endpoint, None, self.headers)

		#	return is a list of items or None
		return returnData


	def get(self, url, data, headers):	# Calls send with the GET method
		return self._send('GET', url, data, headers);


	def post(self, url, data, headers):	# Calls send with the POST method
		return self._send('POST', url, data, headers);


	def _send(self, method, url, data, headers):	# In-between method for the get and post methods

		#	Make request
		rsp, returnData = self._request(method, self.endpoint + url, data, headers)
		if rsp is None:
			return None

		#	Loop to get all data
		while 'next' in rsp.links:
			rsp, tmpData = self._request(method, rsp.links['next']['url'], data, headers)
			if rsp is None:
				return None
			returnData = itertools.chain(returnData, tmpData)
		return Api42._chainToList(returnData)


	#	First it waits,
	#	thne makes an actual request,
	#	returns the response and list of data
	def _request(self, method, url, data, headers):

		#	Pausing for the api request limit (500 milliseconds)
		while (Api42._currentMilliTime() - self.apiLimit) < self.lastCall:
			pass
		self.lastCall = Api42._currentMilliTime()

		#	Making the request - only handles get and post requests for now
		print(IYELLOW + "Requesting data from... " + ICYAN + url + ENDCOLOR + ' ', end='')
		sys.stdout.flush()
		rsp = requests.request(method, url=url, data=data, headers=headers)
		self.totalRequests += 1;

		#	Error handling
		if (rsp is None) or rsp.status_code != 200:
			print(BRED + "...Failed!" + ENDCOLOR)
			return None, None

		#	Returning the response object AND a list of data
		print(BGREEN + "...Success!" + ENDCOLOR)
		return rsp, Api42._dataList(rsp.json())


	#	A few predefined requests
	#	-------------------------------------------------------------------------------------------

	def onlineStudents(self):
		data = self.makeRequest('/v2/campus/7/locations?filter[active]=true')
		return [ { 'login': i['user']['login'], 'id': i['user']['id'], 'host': i['host'] } for i in data] # Example list comprehension	

	def onlineStudentsAtCampus(self, campusID):
		return self.makeRequest('/v2/campus/' + str(campusID) + '/locations?filter[active]=true')

	def passingProjectsForUser(self, userID):
		return self.makeRequest('/v2/users/' + str(userID) + '/projects_users?range[final_mark]=80,125')

	def projectsForUserInFinalMarkRange(self, userID, minScore, maxScore):
		data = self.makeRequest('/v2/users/' + str(userID) + '/projects_users?range[final_mark]=' + str(minScore) + ',' + str(maxScore))
		return [i['project']['name'] for i in data]	# An example list comprehension return format - just returns the names of the projects

	def allProjects(self):
		return self.makeRequest('/v2/cursus/1/projects')


# Example output / usage

# myapi = Api42(apikeys.uid, apikeys.secret)

# print(myapi.onlineStudents())

# print(myapi.projectsForUserInFinalMarkRange(apikeys.twaltonID, 105, 125))	# Returns just the names of projects that Theo Walton has passed between 105-125

# p = myapi.makeRequest('/v2/project_data/30')	# Returns rush data
# print(p)

# p = myapi.makeRequest('/v2/me/messages')		# Should return null
# print(p)

# p = myapi.makeRequest('/v2/languages')		# Returns languages
# print(p)

