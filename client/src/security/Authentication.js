import React from 'react';
import { Redirect } from 'react-router-dom';
import axios from 'axios';
import { apiUserLogin } from '../apihandling/api';

// Query string will handle authorization codes
import queryString from 'query-string';

const ENABLE_FAKE_AUTH = true; // Turn this on if you just need fake authentication

class Authentication {
	constructor() {
		// FAKE AUTHENTICATION ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		if (ENABLE_FAKE_AUTH) {
			this.profile = {
				id: 12413,
				login: "nwang",
				first_name: 'nicky',
				last_name: 'boi',
				correction_point: 15000,
				cursus_users:[{cursus_id: 1, grade: 'HELL YEAH', level: '420BlazeIt'}],
			}
			let newDate = new Date().getTime;
			this.token = {
				created_at: newDate,
				expires_in: newDate + 10000000,
			}
		} // ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
		else {
			this.profile = JSON.parse(sessionStorage.getItem("profile"));
			this.token = JSON.parse(sessionStorage.getItem("token"));
		}
	}

	getProfile = () => {
		return this.profile;
	}

	getToken = () => {
		return this.token;
	}

	setCredentials = (profile, token) => {
		this.profile = profile;
		this.token = token;
		sessionStorage.setItem("profile", JSON.stringify(profile));
		sessionStorage.setItem("token", JSON.stringify(token));
	}

	clearCredentials = () => {
		this.profile = null;
		this.token = null;
		sessionStorage.removeItem("profile");
		sessionStorage.removeItem("token");
	}

	authenticate = (searchParameters) => {
		return new Promise((resolve, reject) => {
			// If user is already authenticated, resolve
			if (this.profile && this.token) {
				return resolve("User is already authenticated");
			}

			// Parse out the { state, code }
			let values = queryString.parse(searchParameters);

			// Check the state sent matches the state that was returned
			if (values.state != SENSEI_STATE) {
				this.clearCredentials();
				return reject("The state did not match");
			}

			// Send code to the Sensei server
			delete values['state'];
			apiUserLogin.post(values)
				.then(response => {
					// User successfully Logged in
					const { user, access } = response.data;
					this.setCredentials(user, access);
					return resolve(response);
				})
				.catch(err => {
					// An error occurred while logging in
					this.clearCredentials();
					return reject(err);
				});
		});
	}

	isAuthenticated = () => {
		// FAKE AUTHENTICATION ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		if (ENABLE_FAKE_AUTH) return true;
		// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		if (!this.token)
			return false;
		return new Date().getTime() < ((this.token.created_at + this.token.expires_in) * 1000) + 1000000000;
	}

}

const authClient = new Authentication();

export default authClient;
