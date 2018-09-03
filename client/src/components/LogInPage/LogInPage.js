import React, { Fragment } from 'react';
import { Redirect } from 'react-router-dom';

import authClient from '../../security/Authentication';


const LogInPage = () => {
	if (authClient.isAuthenticated()) {
		return (<Redirect to="/home" />);
	}

	return (
		<Fragment>
			<div className="flex flex-column">
				<div className="sm-flex">
					<div className="m1 flex flex-center justify-center logInSenseiBox bg-purple">
						<p className="flex logInSenseiText">Become a Sensei</p>
					</div>
					<div className="m1 flex flex-center justify-center logInSenseiBox bg-blue">
						<p className="flex logInSenseiText">Get Sensei'd</p>
					</div>
				</div>
				<div className="m1 flex flex-center justify-center bg-green">
					<h1>Sign In</h1>
				</div>
			</div>
		</Fragment>
	);
}

export default LogInPage;
