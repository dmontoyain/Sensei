import React, { Component, Fragment } from 'react';

import {
	apiPendingAppointmentsAsMentor,
	apiPendingAppointmentsAsUser
} from '../../apihandling/api';

import authClient from '../../security/Authentication';

// CSS

import './Home.css'

const monthsRef = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "Jun.", "Jul.", "Aug.", "Sep.", "Oct.", "Nov.", "Dec."];
const daysRef = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

const Appointments = ({ ...props }) => {

	const { myAppointments } = { ...props };

	const formatStartTime = (st) => {
		const date = new Date(st);
		const day = daysRef[date.getDay()];
		const mth = monthsRef[date.getMonth()];
		const dayN = date.getDate();
		const hr = date.getHours();
		const mn = date.getMinutes();
		const sc = date.getSeconds();
		return `You have an appointment on ${day}, ${mth} ${dayN} at ${hr}:${mn}:${sc}`;
	}

	return (
		<div>
			{myAppointments.map((apnt, idx) => (
				<div key={idx}>
					<span>{formatStartTime(apnt.start_time)}</span>
				</div>
			))}
		</div>
	);
}

// HOC that wraps the Appointments class
const appointmentWrap = (WrappedComponent, apiCall, title) => {
	class HOC extends Component {
		constructor(props) {
			super(props);
			this.state = {
				myAppointments: [],
			}
		}

		componentWillMount() {
			apiCall.get("nwang")//authClient.login)
				.then(data => {
					this.setState({ myAppointments: data.data === {} ? [] : data.data });
				})
				.catch(err => {
					this.setState({
						myAppointments: [
							{ fake: "fake", deleteme: "Delete me later", start_time: "2018-08-10T18:19:49.955709+00:00", },
							{ fake: "DOUBLEfake", deleteme: "This is just a test", start_time: "2018-08-09T14:08:36.695116+00:00", },
						],
					})
				})
		}

		render() {
			return (
				<Fragment>
					<h4 className="home-box-title">{title}</h4>
					<WrappedComponent
						myAppointments={this.state.myAppointments}
						{ ...this.props }
					/>
				</Fragment>
			);
		}
	}

	return HOC;
}

const AppointmentsAsUser = appointmentWrap(Appointments, apiPendingAppointmentsAsUser, "Learning");

const AppointmentsAsMentor = appointmentWrap(Appointments, apiPendingAppointmentsAsMentor, "Teaching");

export {
	AppointmentsAsUser,
	AppointmentsAsMentor,
}
