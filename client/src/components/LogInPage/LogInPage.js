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
					<div className="flex-auto logInSenseiBox bg-purple">
						<h1 className="becomeSensei">Become a Sensei</h1>
					</div>
					<div className="flex-auto logInSenseiBox bg-blue">
						<h1>Get Sensei'd</h1>
					</div>
				</div>
				<div className="">
					<h1>Sign In</h1>
				</div>
			</div>
		</Fragment>
	);
}

export default LogInPage;
