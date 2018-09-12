import React, { Component, Fragment } from 'react';

// Components

import {
	AppointmentsAsUser,
	AppointmentsAsMentor,
} from './Appointments';

import { apiUserUpdate, apiUser } from '../../apihandling/api';

import Profile from './Profile';
import Online from '../Online/Online';

// Security

import authClient from '../../security/Authentication';

// CSS

import './Home.css';

// Extra

import classNames from 'classnames';


// Accepts a component and bounds the given component within a Home Box
// Takes an optional className to add to the container for the wrapped component

const homeBox = (WrappedComponent, className) => {
	class HOC extends Component {
		constructor(props) {
			super(props);
		}

		render() {
			return (
				<div className={classNames(className, "home-box")}>
					<WrappedComponent { ...this.props } />
				</div>
			)
		}
	}

	return HOC;
}


// The main render of the home page

class Home extends Component {
	constructor(props) {
		super(props);
		this.state = {
			hello: "hello",
		}
	}

	render() {
		const { listOfUsers } = this.state;
		const { className } = this.props; 

		const Pr = homeBox(Profile, "hb-top");
		const Au = homeBox(AppointmentsAsUser);
		const Am = homeBox(AppointmentsAsMentor);

		return (
			<Fragment>
				<div className="banner" />
				<div className="home-main">
					<Pr />
					<Au />
					<Am />
				</div>
			</Fragment>
		);
	}
}

export default Home;
