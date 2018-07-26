from datetime import datetime
import time
import json
import requests
import itertools
from config.apikeys import uid, secret
from terminalcolors import *

_current_milli_time = lambda: int(round(time.time() * 1000))

class Api42:

	def __init__(self, uid, secret):
		self.token = None
		self.tokenExpires = 0
		self.apiLimit = int(0.5 * 1000)								# API limit is in milliseconds (0.5 seconds times 1000)
		self.lastCall = 0
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
		self.methodDict = {
			'GET': requests.get,
			'POST': requests.post
		}
		#	Some extra information for debugging / upkeep
		self.numOfRequestsMade = 0


	#	For general GET requests that require a single endpoint
	def makeRequest(self, endpoint):
		#	If a new token is needed, update it
		self.updateToken()as

		#	Make the actual request
		returnData = self.get(endpoint, None, self.headers)

		#	If the request failed, but it had to update the token,
		#	try and perform the request again
		if returnData is None and self.updateToken():
			returnData = self.get(endpoint, None, self.headers)

		#	returnData is a list of items, or none if any error happened
		#	during the request
		return returnData


	#	Returns a True if token needed updating, otherwise False
	def updateToken(self):
		#	Check whether token needs updating
		if _current_milli_time() >= self.tokenExpires:
			tokenData = self.post('/oauth/token', self.authData, None)
			if tokenData is None:
				return

			#	Update token, expiry time, and authorization header
			self.token = tokenData[0]['access_token']
			self.tokenExpires = (tokenData[0]['expires_in'] * 1000) + _current_milli_time()
			self.headers['Authorization'] = 'Bearer ' + self.token
			print(IGREEN + "Token Updated!" + ENDCOLOR)
			return True
		return False


	#	Calls send with the POST method
	def post(self, uri, data, headers):
		return self._send(uri, 'POST', data, headers);


	#	Calls send with the GET method
	def get(self, uri, data, headers):
		return self._send(uri, 'GET', data, headers)


	#	In-between method for the get and post methods
	def _send(self, uri, method, data, headers):
		#	initializing send request
		url 		= self.endpoint + uri
		requestFunc	= self.methodDict.get(method, None)

		#	Making the request - only handles get and post requests for now
		rsp, returnData = self._request(url, data, headers, requestFunc)
		if rsp is None:
			return None

		#	Loop to get all data
		while 'next' in rsp.links:
			url = rsp.links['next']['url']
			rsp, tmpData = self._request(url, data, headers, requestFunc)
			if rsp is None:
				return None
			returnData += tmpData
		return returnData


	#	Waits, makes actual request, then returns the response and returnData list
	#	Should be a private function
	def _request(self, url, data, headers, requestFunc):
		#	Pausing for the api limiter
		self._waitForRequest()

		#	Making the request - only handles get and post requests for now
		print(IYELLOW + "Requesting data from... " + ICYAN + url + ENDCOLOR, end='')
		rsp = requestFunc(url, data=data, headers=headers)
		self.numOfRequestsMade += 1

		#	Error handling
		if (rsp is None) or rsp.status_code != 200:
			print(BRED + " ...Failed!" + ENDCOLOR)
			return None, None

		#	Returning the response object AND the list of returnData
		print(BGREEN + " ...Success!" + ENDCOLOR)
		returnData = rsp.json()
		returnData = [returnData] if type(returnData) is dict else returnData
		return rsp, returnData

	#	A helper function that waits until the next available time to make the api call
	def _waitForRequest(self):
		while (_current_milli_time() - self.apiLimit) < self.lastCall:
			pass
		self.lastCall = _current_milli_time()

# Example output / usage

myapi = Api42(uid, secret)
p = myapi.makeRequest('/v2/project_data/30')	# Returns rush data
print(p)
p = myapi.makeRequest('/v2/me/messages')		# Should return null
print(p)
p = myapi.makeRequest('/v2/languages')			# Returns languages
print(p)
