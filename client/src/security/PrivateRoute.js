import React from 'react';
import { Route, Redirect } from 'react-router-dom';
import authClient from './Authentication';

// Accepts 'component' and 'path' as properties
// Only renders the Component if the user is logged in

const PrivateRoute = (props) => {

	const { component: Component, path} = props;

	return (
		<Route path={path} render={() => {
			if (!authClient.isAuthenticated()) {
				return <Redirect to="/" />;
			}
			return <Component />
		}} />
	);
}

export default PrivateRoute;
