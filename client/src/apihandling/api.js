import React from 'react';
import axios from 'axios';

const AxiosHandler = function() {
	this._onSuccess = function(response) {
		console.log('Request Successful!', response);
		return Promise.resolve(response.data);
	}

	this._onError = function(error) {
		console.error('Request Failed...', error.config);

		if (error.response) {
			// Request was made, but server responded with !2XX
			console.error('Status:',	error.response.status);
			console.error('Data:',		error.response.data);
			console.error('Headers:',	error.response.headers);
		} else {
			// Something else happened while setting up the request
			console.error('Server Error:', error.message);
		}
		return Promise.reject(error.response || error.message);
	}

	this._get = function(endpoint, data, headers) {
		console.log(endpoint, data, headers);
		return axios.get(endpoint, data, headers)
			.then(this._onSuccess)
			.catch(this._onError); // Token re-authentication check will go here
	}

	this._post = function(endpoint, data, headers) {
		return axios.post(endpoint, data, headers)
			.then(this._onSuccess)
			.catch(this._onError);
	}

	this._put = function(endpoint, data, headers) {
		return axios.put(endpoint, data, headers)
			.then(this._onSuccess)
			.catch(this._onError);
	}

	this._delete = function(endpoint, data, headers) {
		return axios.delete(endpoint, data, headers)
			.then(this._onSuccess)
			.catch(this._onError);
	}

}

// ----------------------------------------------------------------------------

const axHandler = new AxiosHandler();

const headers = {
	'content-type': 'application/json',
	'x-access-token': '',
}

// USER
// ----------------------------------------------------------------------------

const apiUsers = function() {
	this.endpoint = `${API_URL}/api/users`;

	this.newEndpoint = (id) => {
		return `${this.endpoint}/${id}`;
	}

	this.get = () => {
		return axHandler._get(this.endpoint, null, headers);
	}

	this.post = () => {
		return axHandler._post(this.endpoint, null, headers);
	}
}

const apiUsersOnline = function() {
	this.endpoint = `${API_URL}/api/users/online`;

	this.get = (data) => {
		return axHandler._get(this.endpoint, data, headers);
	}
}

const apiUserProjectsAvailableMentors = function() {
	this.endpoint = `${API_URL}/api/user`;

	this.newEndpoint = (login) => {
		return `${this.endpoint}/${login}/projects/availablementors`;
	}

	this.get = (login) => {
		return axHandler._get(this.newEndpoint(login), null, headers);
	}
}

const apiUserUpdate = function () {
	this.endpoint = `${API_URL}/api/user`;

	this.newEndpoint = (login) => {
		return `${this.endpoint}/${login}/update`;
	}

	this.post = (login) => {
		return axHandler._post(this.newEndpoint(login), null, headers);
	}
}

const apiUser = function() {
	this.endpoint = `${API_URL}/api/user`;

	this.newEndpoint = (login) => {
		return `${this.endpoint}/${login}`;
	}

	this.get = (login) => {
		return axHandler._get(this.newEndpoint(login), null, headers);
	}

	this.post = (login, data) => {
		return axHandler._post(this.newEndpoint(login), data, headers);
	}
}

const apiUserLogin = function() {
	this.endpoint = `${API_URL}/api/user/login`;

	this.post = (data) => {
		return axHandler._post(this.endpoint, data, headers);
	}
}

const apiUserPendingAppointments = function() {
	this.endpoint = `${API_URL}/api/users`

	this.newEndpoint = (userId) => {
		return `${this.endpoint}/${userId}/pendingappointments`;
	}

	this.get = (userId) => {
		return axHandler._get(this.newEndpoint(userId), null, headers);
	}
}


// APPOINTMENTS
// ----------------------------------------------------------------------------

const apiAppointments = function() {
	this.endpoint = `${API_URL}/api/appointments`;

	this.get = () => {
		return axHandler._get(this.endpoint, null, headers);
	}

	this.post = (data) => {
		return axHandler._post(this.endpoint, data, headers);
	}
}

const apiAppointment = function() {
	this.endpoint = `${API_URL}/api/appointment`;

	this.newEndpoint = (id) => {
		return `${this.endpoint}/${id}`;
	}

	this.get = (id) => {
		return axHandler._get(this.newEndpoint(id), null, headers);
	}

	this.put = (id, data) => {
		return axHandler._put(this.newEndpoint(id), data, headers);
	}

	this.delete = (id) => {
		return axHandler._delete(this.newEndpoint(id), null, headers);
	}
}

const apiAppointmentsAsUser = function() {
	this.endpoint = `${API_URL}/api/appointments/user`;

	this.newEndpoint = (id) => {
		return `${this.endpoint}/${id}`;
	}

	this.get = (id) => {
	return axHandler._get(this.newEndpoint(id), null, headers);
	}
}

const apiAppointmentsAsMentor = function() {
	this.endpoint = `${API_URL}/api/appointments/mentor`;

	this.newEndpoint = (id) => {
		return `${this.endpoint}/${id}`;
	}

	this.get = (id) => {
	return axHandler._get(this.newEndpoint(id), null, headers);
	}
}


// MENTORS
// ----------------------------------------------------------------------------

const apiMentors = function() {
	this.endpoint = `${API_URL}/api/mentors`;

	this.get = () => {
		return axHandler._get(this.endpoint, null, headers);
	}
}

const apiMentor = function() {
	this.endpoint = `${API_URL}/api/mentor`;

	this.newEndpoint = (id) => {
		return `${this.endpoint}/${id}`;
	}

	this.get = (id) => {
		return axHandler._get(this.newEndpoint(id), null, headers);
	}

	this.put = (id) => {
		return axHandler._put(this.newEndpoint(id), null, headers);
	}
}

const apiSubscribeUnSubscribeMentor = function() {
	this.endpoint = `${API_URL}/api/mentor`;

	this.newEndpoint = (id) => {
		return `${this.endpoint}/${id}/subscribeunsubscribe`;
	}

	this.put = (id) => {
		return axHandler._put(this.newEndpoint(id), null, headers);
	}
}

const apiSubscribeMentor = function() {
	this.endpoint = `${API_URL}/api/mentor`;

	this.newEndpoint = (id) => {
		return `${this.endpoint}/${id}/subscribe`;
	}

	this.put = (id) => {
		return axHandler._put(this.newEndpoint(id), null, headers);
	}
}

const apiUnsubscribeMentor = function() {
	this.endpoint = `${API_URL}/api/mentor`;

	this.newEndpoint = (id) => {
		return `${this.endpoint}/${id}/unsubscribe`;
	}

	this.put = (id) => {
		return axHandler._put(this.newEndpoint(id), null, headers);
	}
}

const apiMentorsProject = function() {
	this.endpoint = `${API_URL}/api/mentors/project`;

	this.newEndpoint = (id) => {
		return `${this.endpoint}/${id}`;
	}

	this.get = (id) => {
		return axHandler._get(this.newEndpoint(id), null, headers);
	}

	this.post = (id) => {
		return axHandler._post(this.newEndpoint(id), null, headers);
	}
}

const apiUserMentoring = function() {
	this.endpoint = `${API_URL}/mentors/user`;

	this.newEndpoint = (id) => {
		return `${this.endpoint}/${id}/active`;
	}

	this.get = (id) => {
		return axHandler._get(this.newEndpoint(id), null, headers);
	}
}

const apiUserCapableToMentor = function() {
	this.endpoint = `${API_URL}/mentors/user`;

	this.newEndpoint = (id) => {
		return `${this.endpoint}/${id}/capable`;
	}

	this.get = (id) => {
		return axHandler._get(this.newEndpoint(id), null, headers);
	}
}

const apiMentorPendingAppointments = function() {
	this.endpoint = `${API_URL}/api/mentors`

	this.newEndpoint = (id) => {
		return `${this.endpoint}/${id}/pendingappointments`;
	}

	this.get = (id) => {
		return axHandler._get(this.newEndpoint(id), null, headers);
	}
}

// PROJECTS
// ----------------------------------------------------------------------------

const apiProjects = function() {
	this.endpoint = `${API_URL}/api/projects`;

	this.get = () => {
		return axHandler._get(this.endpoint, null, headers);
	}

	this.post = () => {
		return axHandler._post(this.endpoint, null, headers);
	}
}

// EXPORTS ------------------------------------------------------------------------------

module.exports = {
	apiUsers: new apiUsers(),
	apiUsersOnline: new apiUsersOnline(),
	apiUserProjectsAvailableMentors: new apiUserProjectsAvailableMentors(),
	apiUserUpdate: new apiUserUpdate(),
	apiUser: new apiUser(),
	apiUserLogin: new apiUserLogin(),
	apiUserPendingAppointments: new apiUserPendingAppointments(),
	apiAppointments: new apiAppointments(),
	apiAppointment: new apiAppointment(),
	apiAppointmentsAsUser: new apiAppointmentsAsUser(),
	apiAppointmentsAsMentor: new apiAppointmentsAsMentor(),
	apiMentors: new apiMentors(),
	apiMentor: new apiMentor(),
	apiSubscribeUnSubscribeMentor: new apiSubscribeUnSubscribeMentor(),
	apiSubscribeMentor: new apiSubscribeMentor(),
	apiUnsubscribeMentor: new apiUnsubscribeMentor(),
	apiMentorsProject: new apiMentorsProject(),
	apiUserMentoring: new apiUserMentoring(),
	apiUserCapableToMentor: new apiUserCapableToMentor(),
	apiMentorPendingAppointments: new apiMentorPendingAppointments(),
	apiProjects: new apiProjects()
}
