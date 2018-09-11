import React, { Component } from 'react';
import { Route, Redirect } from 'react-router-dom';

import authClient from './Authentication';

import { apiUserLogin } from '../apihandling/api';

// Accepts 'component' and 'path' as properties
// Only renders the Component if the user is logged in

class PrivateRoute extends Component {

	constructor(props) {
		super(props);
		this.state = {
			authenticated: authClient.isAuthenticated(),
		}
		console.log("CONSTRUCTOR", authClient.isAuthenticated());
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
		const { component: C, path, location } = this.props;
		const { authenticated } = this.state;

		// If the Authorization code has been passed through,
		// that means we are coming from a redirect through the 42 Intra API
		if (location.search.includes("?code=") && authenticated != true) {
			return <div>Pending...</div>
		}

		// Return the user to the log in page.
		if (!authenticated) {
			return <Redirect to="/" />;
		}

		// Immediately render page if client is authenticated
		if (authenticated) {
			return <Route path={path} render={() => <C />} />
		}
	}
}

export default PrivateRoute;
