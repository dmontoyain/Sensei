import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';
import { OauthSender } from 'react-oauth-flow';

import authClient from '../../security/Authentication';

class SendToIntra extends Component {
	render() {
		return (
			<OauthSender
				authorizeUrl="https://api.intra.42.fr/oauth/authorize"
				clientId={SENSEI_UUID}
				redirectUri={`${WEBSITE}/auth`}
				state={{ from: '/settings', string: 'thebestshakesareatdennysbecarefulthoughsomeonemightsmashyourcarwindow' }}
				render={({ url }) => <a href={url}>Connect to Intra</a>}
			/>
		);
	}
}

class ReceiveFromIntra extends Component {
	handleSuccess = async (accessToken, { response, state }) => {
		console.log('Successfully authorized');
		// await setProfileFromDropbox(accessToken);
		// await redirect(state.from);
	};

	handleError = error => {
		console.error('An error occured');
		console.error(error.message);
	};
 
	render() {
		return (
			<OauthReceiver
				tokenUrl="https://api.intra.42.fr/oauth/token"
				clientId={SENSEI_UUID}
				clientSecret={SENSEI_SECRET}
				redirectUri={`${WEBSITE}/auth`}
				onAuthSuccess={this.handleSuccess}
				onAuthError={this.handleError}
				render={({ processing, state, error }) => (
					<div>
						{processing && <p>Authorizing now...</p>}
						{error && <p className="error">An error occured: {error.message}</p>}
					</div>
				)}
			/>
		);
	}
}

// Redirect uri when coming from Intra's OAuth

class Auth extends Component {
	constructor(props) {
		super(props);
		this.state = {
			authenticated: authClient.isAuthenticated(),
		}
	}

	handleAuthentication = (searchParameters) => {
		// If there is something to query
		if (searchParameters.length) {
			// Sends the ?code= query to the authenticate method
			authClient.authenticate(searchParameters)
				.then(response => {
					console.log("success", authClient.isAuthenticated());
					this.setState({ authenticated: authClient.isAuthenticated() });
				})
				.catch(err => {
					console.log("failed", authClient.isAuthenticated());
					this.setState({ authenticated: authClient.isAuthenticated() });
				});
		}
	}

	componentWillMount() {
		const { location } = this.props;
		// Check authentication
		this.handleAuthentication(location.search);
	}

	render() {
		const { authenticated } = this.state;

		console.log("HEY", authenticated);
		if (authenticated) {
			return (<Redirect to="/home" />);
		}

		return (<div>Pending...</div>);
	}
}

export {
	Auth,
	SendToIntra,
	ReceiveFromIntra,
}
