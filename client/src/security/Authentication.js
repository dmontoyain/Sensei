import React from 'react';
import { Redirect } from 'react-router-dom';
import axios from 'axios';

class Authentication {
	constructor() {
		this.profile = null;
		this.token = null;
		this.expiresAt = null;
	}

	getProfile = () => {
		return this.profile;
	}

	getToken = () => {
		return this.token;
	}

	authenticate = () => {
		// return new Promise((resolve, reject) => {
		// 	this.auth0.parseHash((err, authResult) => {
		// 		if (err) return reject(err);
		// 		if (!authResult || !authResult.token) {
		// 			return reject(err);
		// 		}
		// 		this.token = authResult.token;
		// 		this.profile = authResult.tokenPayload;
		// 		// set the time that the id token will expire at
		// 		this.expiresAt = authResult.expiresIn * 1000 + new Date().getTime();
		// 		resolve();
		// 	});
		// })
		// LOG IN GOES HERE
	}

	isAuthenticated = () => {
		return false; // DELETE LATER -------------------------------------------------
		return new Date().getTime() < this.expiresAt;
	}

	signIn = () => {
		this.authenticate();
		return (<Redirect to="https://signin.intra.42.fr/users/sign_in" />);
	}

	signOut = () => {
		// clear id token, profile, and expiration
		this.token = null;
		this.profile = null;
		this.expiresAt = null;
	}
}

const authClient = new Authentication();

console.log("CLIENTTTTTTTTTT")

export default authClient;
