import React, { Fragment } from 'react';
import { Redirect } from 'react-router-dom';

import authClient from '../../security/Authentication';

// CSS
import './LogInPage.css';


const LogInPage = () => {
	if (authClient.isAuthenticated()) {
		return (<Redirect to="/home" />);
	}

	return (
		<div className="logInFull">
			<div className="flex flex-column">
				<div className="flex flex-wrap logInFull">
					<div className="flex-auto logInSenseiBox">
						<p className="flex justify-center logInSenseiText">Become a Sensei</p>
					</div>
					<div className="flex-auto logInSenseiBox">
						<p className="flex justify-center logInSenseiText">Get Sensei'd</p>
					</div>
				</div>
				<div className="logInSenseiSignInBox">
					<p className="justify-center">Sign In</p>
				</div>
			</div>
		</div>
	);

	/*return (
		<Fragment>
			<div className="flex flex-column">
				<div className="sm-flex">
					<div className="flex flex-center justify-center logInSenseiBox bg-purple">
						<p className="flex logInSenseiText">Become a Sensei</p>
					</div>
					<div className="flex flex-center justify-center logInSenseiBox bg-blue">
						<p className="flex logInSenseiText">Get Sensei'd</p>
					</div>
				</div>
				<div className="flex flex-center justify-center logInSenseiSignInBox bg-intra-light">
					<h1>Sign In</h1>
				</div>
			</div>
		</Fragment>
	);*/
}

export default LogInPage;
