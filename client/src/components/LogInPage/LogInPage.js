
import React, { Fragment, Component } from 'react';
import { Redirect, Route } from 'react-router-dom';
import queryString from 'query-string';

import authClient from '../../security/Authentication';

// Components
import { SendToIntra } from '../Authentication/Auth';

// CSS
import './LogInPage.css';


// Main render for the login page
const LogInPage = () =>  {
	const intraAuth = 'https://api.intra.42.fr/oauth/authorize?' +
						queryString.stringify({
							client_id: SENSEI_UUID,
							redirect_uri: `${WEBSITE}/auth`,
							response_type: 'code',
							state: 'thebestshakesareatdennysbecarefulthoughsomeonemightsmashyourcarwindow',
						});

	// If user is already logged in, redirect to Home
	if (authClient.isAuthenticated()) {
		return <Redirect to="/home" />;
	}

	// If they aren't authenticated, clear cached credentials, just in case.
	authClient.clearCredentials();

	return (
		<div className="login-root">
			<div className="logInFull">
				<div className="logInSenseiBox">
					<p className="logInSenseiText">Let's Do It!</p>
				</div>
				<div className="logInSenseiSignInBox">
					<a className="sign-submit" href={intraAuth}>
						<div className="sign-text">Sign In</div>
					</a>
				</div>
			</div>
		</div>
	);
}
export default LogInPage;
