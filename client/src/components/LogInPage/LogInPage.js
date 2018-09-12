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

	// Clear credentials if fail, just in case.
	authClient.clearCredentials();

	return (
		<div className="login-root">
			<div className="logInFull">
				<div className="logInSenseiBox">
					<p className="logInSenseiText">Let's Do It!</p>
				</div>
				<div className="logInSenseiSignInBox">
					<SendToIntra />
					<a className="sign-submit" href={intraAuth}>
						<div className="sign-text">Sign In</div>
					</a>
				</div>
			</div>
		</div>
	);
}

export default LogInPage;