import React from 'react';
import { Route } from 'react-router-dom';
import authClient from './Authentication';

// Accepts 'component' and 'path' as properties
// Only renders the Component if the user is logged in

function PrivateRoute(props) {

	const { component: Component, path} = props;

	return (
		<Route path={path} render={() => {
			// if (!authClient.isAuthenticated()) {
			// 	return authClient.signIn();
			// }
			return <Component />
		}} />
	);
}

export default PrivateRoute;
