import React, { Component, Fragment } from 'react';
import { Redirect } from 'react-router-dom';
import { OauthSender, OauthReceiver } from 'react-oauth-flow';

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
			initialUser: false,
		}
	}

	handleAuthentication = (searchParameters) => {
		// If there is something to query
		if (searchParameters.length) {
			// Sends the ?code= query to the authenticate method
			authClient.authenticate(searchParameters)
				.then(response => {
					this.setState({ authenticated: authClient.isAuthenticated() });
				})
				.catch(err => {
					this.setState({ authenticated: authClient.isAuthenticated() });
				});
		}
	}

	componentWillMount() {
		// Check authentication
		this.handleAuthentication(this.props.location.search);
		this.initialUserTimeout = setTimeout(() => this.setState({ initialUser: true }), 7000);
	}

	componentWillUnmount() {
		clearTimeout(this.initialUserTimeout);
	}

	render() {
		const { authenticated, initialUser } = this.state;

		if (authenticated) {
			return (<Redirect to="/home" />);
		}

		return (
			<Fragment>
				<div style={{ position: 'fixed',
								width: '100%',
								height: '100%',
								backgroundColor: 'white',
								textAlign: 'center' }}
				>
					<img src="https://www.demilked.com/magazine/wp-content/uploads/2016/06/gif-animations-replace-loading-screen-14.gif" alt="loading..." /><br/>
					Logging in... <br/>
					{initialUser ? "Your first login might take a quick minute!" : ""}
				</div>
			</Fragment>
		);
	}
}

export {
	Auth,
	SendToIntra,
	ReceiveFromIntra,
}
