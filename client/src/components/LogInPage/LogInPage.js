import React, { Fragment, Component } from 'react';
import { Redirect, Route } from 'react-router-dom';
import queryString from 'query-string';

import authClient from '../../security/Authentication';

// Components
import { SendToIntra } from '../Authentication/Auth';

// CSS
import './LogInPage.css';

const LogInPage = () =>  {
	const intraAuth = 'https://api.intra.42.fr/oauth/authorize?' +
						queryString.stringify({
							client_id: SENSEI_UUID,
							redirect_uri: /*`${API_URL}/api/user/login`, */`${WEBSITE}/auth`,
							response_type: 'code',
							state: 'thebestshakesareatdennysbecarefulthoughsomeonemightsmashyourcarwindow',
						});

	if (authClient.isAuthenticated()) {
		return <Redirect to="/home" />;
	}

	render() {
		const { redirect } = this.state;

		if (authClient.isAuthenticated()) {
			console.log("login page redirect")
			return <Redirect to="/home" />;
		}

		return (
			<div className="login-root">
				<ErrorModal>FAILUREadfasdfasfafadsf</ErrorModal>
				<div className="logInFull">
					<div className="logInSenseiBox">
						<p className="logInSenseiText">Push Your Skills To a New Level</p>
					</div>
					<div className="logInSenseiSignInBox">
						<a className="sign-submit" href={this.redirect}>
							<div className="sign-text">Sign In</div>
						</a>
					</div>
				</div>
			</div>
		</div>
	);
}

export default LogInPage;