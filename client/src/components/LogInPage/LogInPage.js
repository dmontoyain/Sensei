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
		<div className="login-root">
			<div className="logInFull">
				<div className="logInSenseiBox">
					<p className="logInSenseiText">Let's Do It!</p>
				</div>
				<div className="logInSenseiSignInBox">
					<input type="submit" name="Sign-In" value="Sign In" class="sign-submit" />
				</div>
			</div>
		</div>
	);
}

{/* <div className="logInFull">
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
</div> */}

export default LogInPage;