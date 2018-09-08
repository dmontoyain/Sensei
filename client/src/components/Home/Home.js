import React, { Component } from 'react';

// Components

import {
	AppointmentsAsUser,
	AppointmentsAsMentor
} from './Appointments';

import Profile from './Profile';

// Security
import authClient from '../../security/Authentication';

// CSS
import './Home.css';

// Extra

import classNames from 'classnames';

// Bounds the given component within a Home Box
// Takes an optional className to add to the container for the wrapped component

const homeBox = (WrappedComponent, className) => {
	class HOC extends Component {
		constructor(props) {
			super(props);
		}

		render() {
			return (
				<div className={classNames("home-box", className)}>
					<WrappedComponent { ...this.props } />
				</div>
			)
		}
	}

	return HOC;
}

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

		const Pr = homeBox(Profile, "hb-double-width");
		const Au = homeBox(AppointmentsAsUser);
		const Am = homeBox(AppointmentsAsMentor);

		return (
			<div className="home-main">
				<Pr />
				<Au />
				<Am />
			</div>
		);
	}
}

export default Home;
