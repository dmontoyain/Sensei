import React, { Fragment, Component } from 'react';
import { Redirect, Route } from 'react-router-dom';

import authClient from '../../security/Authentication';

import { ErrorModal } from '../Extra/Modal';

// CSS
import './LogInPage.css';


class LogInPage extends Component {
	constructor(props) {
		super(props);
		this.state = {
			redirect: false,
		}
		this.redirect = `https://api.intra.42.fr/oauth/authorize?client_id=${SENSEI_UUID}&redirect_uri=${WEBSITE}/home&response_type=code&state=thebestshakesareatdennysbecarefulthoughsomeonemightsmashyourcarwindow`
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
		);
	}
}

export default LogInPage;