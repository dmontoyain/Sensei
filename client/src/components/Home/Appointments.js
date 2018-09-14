import React, { Component, Fragment } from 'react';

// Components
import NoData from '../Extra/NoData';
import Avatar from '../Extra/Avatar';

// API Handler
import {
	apiPendingAppointmentsAsMentor,
	apiPendingAppointmentsAsUser,
	apiMentorPendingAppointments,
	apiUserPendingAppointments,
} from '../../apihandling/api';

// Security
import authClient from '../../security/Authentication';

// Icons
import noDataOne from '../../assets/images/floatingguru.png';
import noDataTwo from '../../assets/images/floatingguru2.png';

// CSS
import './Home.css'

const appointmentWrap = (apiCall, title, noDataIcon) => {
	class HOC extends Component {
		constructor(props) {
			super(props);
			this.state = {
				myAppointments: [],
			}
		}

		componentWillMount() {
			apiCall(authClient.profile.id)
				.then(data => {
					this.setState({ myAppointments: data.data === {} ? [] : data.data });
				})
				.catch(err => {
					// No appointments for user
				});
		}


		formatAppointment = (obj) => {
			// Declare variables
			const { appointment, project, user, userMentoring } = obj;

			// Seperate out the login information
			const { login } = user ? user : userMentoring; // This is the only difference between the data returned by the apiUser... endpoint and the apiMentor... endpoint.

			// Get formatted date
			const time = new Date(appointment.start_time).toLocaleString('en-US', { timeZone: 'America/Los_Angeles', weekday: 'long', month: 'short', hour: 'numeric', minute: 'numeric', hour12: true});

			// The main appointment row
			return (
				<div key={appointment.id} className="appointment-row-container">
					<Avatar size="small" login={login} className="appointment-image" />
					<div>
						<a
							style={{ textDecoration: 'none', color: 'darkgreen', fontSize: '1.4em' }}
							href={`https://profile.intra.42.fr/users/${login}`}
						>
							{login}
						</a>
						<h3>
							{time}
						</h3>
					</div>
				</div>
			);
		}

		render() {
			const { myAppointments } = this.state;

			// Set appointments to the map of divs of each appointment
			const appointments = (
				myAppointments.length ?
				myAppointments.map(obj => this.formatAppointment(obj)) :
				<NoData text="No Appointments" icon={noDataIcon} />
			);

			return (
				<Fragment>
					<h4 className="home-box-title" style={{ marginBottom: '15px' }}>{title}</h4>
					{appointments}
				</Fragment>
			);
		}
	}

	return HOC;
}

const AppointmentsAsUser = appointmentWrap(apiUserPendingAppointments.get, "You will be mentored by...", noDataOne);

const AppointmentsAsMentor = appointmentWrap(apiMentorPendingAppointments.get, "You will mentor...", noDataTwo);

export {
	AppointmentsAsUser,
	AppointmentsAsMentor,
}
