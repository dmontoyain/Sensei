import React, { Component } from 'react';

import {
	AppointmentsAsUser,
	AppointmentsAsMentor
} from './Appointments';

import authClient from '../../security/Authentication';
import classNames from 'classnames';

// CSS
import './Home.css';

// Bounds the given component within a 'box'

const homeBox = (WrappedComponent) => {
	class HOC extends Component {
		constructor(props) {
			super(props);
		}

		render() {
			return (
				<div className="home-box">
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

		const Au = homeBox(AppointmentsAsUser);
		const Am = homeBox(AppointmentsAsMentor);

		return (
			<div className="home-main">
				<Au />
				<Am />
			</div>
		);
	}
}

export default Home;
