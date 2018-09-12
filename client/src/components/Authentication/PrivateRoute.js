import React, { Component } from 'react';
import { Route, Redirect } from 'react-router-dom';

import authClient from '../../security/Authentication';

// Only renders the Component if the user is logged in (authenticated)

const PrivateRoute = ({ component: Component, ...rest }) => (
	<Route { ...rest } render={props => (
		authClient.isAuthenticated() ?
			<Component { ...props } /> :
			<Redirect to="/" />
		)}
	/>
);

export default PrivateRoute;
