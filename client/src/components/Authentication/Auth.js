import React, { Component, Fragment } from 'react';
import { Redirect } from 'react-router-dom';
import queryString from 'query-string';
// import { OauthSender, OauthReceiver } from 'react-oauth-flow';

// Components
import { ErrorModal } from '../Extra/Modal';

// Security
import authClient from '../../security/Authentication';



// class SendToIntra extends Component {
// 	render() {
// 		return (
// 			<OauthSender
// 				authorizeUrl="https://api.intra.42.fr/oauth/authorize"
// 				clientId={SENSEI_UUID}
// 				redirectUri={`${WEBSITE}/auth`}
// 				state={{ from: '/settings', string: 'thebestshakesareatdennysbecarefulthoughsomeonemightsmashyourcarwindow' }}
// 				render={({ url }) => <a href={url}>Connect to Intra</a>}
// 			/>
// 		);
// 	}
// }

// class ReceiveFromIntra extends Component {
// 	handleSuccess = async (accessToken, { response, state }) => {
// 		console.log('Successfully authorized');
// 		// await setProfileFromDropbox(accessToken);
// 		// await redirect(state.from);
// 	};

// 	handleError = error => {
// 		console.error('An error occured');
// 		console.error(error.message);
// 	};
 
// 	render() {
// 		return (
// 			<OauthReceiver
// 				tokenUrl="https://api.intra.42.fr/oauth/token"
// 				clientId={SENSEI_UUID}
// 				clientSecret={SENSEI_SECRET}
// 				redirectUri={`${WEBSITE}/auth`}
// 				onAuthSuccess={this.handleSuccess}
// 				onAuthError={this.handleError}
// 				render={({ processing, state, error }) => (
// 					<div>
// 						{processing && <p>Authorizing now...</p>}
// 						{error && <p className="error">An error occured: {error.message}</p>}
// 					</div>
// 				)}
// 			/>
// 		);
// 	}
// }


// Handles the redirect from Intra's Authorization Service

class Auth extends Component {
	constructor(props) {
		super(props);
		this.state = {
			authenticated: authClient.isAuthenticated(),
			redirectToLogin: queryString.parse(this.props.location.search).error === 'access_denied',
			initialUser: false,
			authError: false,
		}
		this.initialUserTimeout = null;
		this.authErrorTimeout = null;
	}

	componentWillMount() {
		// Check authentication if the user is not authenticated
		if (!this.state.authenticated) {
			this.handleAuthentication(this.props.location.search);
			this.initialUserTimeout = setTimeout(() => this.setState({ initialUser: true }), 8000);
		}
	}

	componentWillUnmount() {
		this.clearTimeouts();
	}

	clearTimeouts = () => {
		clearTimeout(this.initialUserTimeout);
		clearTimeout(this.authErrorTimeout);
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
					this.setState({ authenticated: false });
					// Display Auth Error for 3 seconds on Fail
					this.authErrorTimeout = setTimeout(() => this.setState({ authError: true }), 6000);
				});
		}
	}

	render() {
		const { authenticated, redirectToLogin, initialUser, authError } = this.state;

		if (redirectToLogin) {
			return (<Redirect to='/' />);
		}

		if (authenticated) {
			return (<Redirect to="/home" />);
		}

		return (
			<Fragment>
				<div style={{ position: 'fixed',
								width: '100%',
								height: '100%',
								backgroundColor: 'white',
								textAlign: 'center',
								cursor: 'wait' }}
				>
					<img src="https://www.demilked.com/magazine/wp-content/uploads/2016/06/gif-animations-replace-loading-screen-14.gif" alt="loading..." /><br/>
					Logging in... <br/>
					{initialUser ? "If this is your first time logging in, the database may need some time to update." : ""}
				</div>
				<ErrorModal show={authError}>Server appears to be having issues...</ErrorModal>
			</Fragment>
		);
	}
}

export {
	Auth,
	// SendToIntra,
	// ReceiveFromIntra,
}
