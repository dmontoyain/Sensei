import React from 'react';
import axios from 'axios';

const AxiosHandler = function() {

	this._onSuccess = function(response) {
		console.log('Request Successful!', response);
		return response.data;
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
		return axios.get(endpoint, data, headers)
			.then(this._onSuccess)
			.catch(this._onError);
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

// --------------------------------------------------------------------------------------

console.log(API_URL)
const axHandler = new AxiosHandler();

const headers = {
	'content-type': 'application/json',
}

// USER
const apiUsers = function() {
	this.endpoint = `${API_URL}/api/users`;

	this.newEndpoint = (id) => {
		return `${this.endpoint}/${id}`;
	}

	this.get = () => {
		return axHandler._get(this.endpoint, null, headers);
	}

	this.post = () => {
		return axHandler._post(this.endpoint)
	}

}


// APPOINTMENTS

const apiAppointment = function() {
	this.endpoint = `${API_URL}/api/appointment`
	
	this.newEndpoint = (id) => {
		return `${this.endpoint}/${id}`;
	}

	this.put = (id, data) => {
		return axHandler._put(this.newEndpoint(id), data, headers);
	}

}

// MENTORS

// PROJECTS


// EXPORTS ------------------------------------------------------------------------------

module.exports = {
	apiUsers: new apiUsers(),
}
