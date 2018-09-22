import React, { Component, Fragment } from 'react';

// Components
import NoData from '../Extra/NoData';
import Avatar from '../Extra/Avatar';
import Feedback from './Feedback';
import { ButtonModal, ErrorModal } from '../Extra/Modal';

// API Handler
import {
	apiMentorPendingAppointments,
	apiUserPendingAppointments,
	apiAppointment,
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

		filterOutApt = (idx) => {
			this.setState({ myAppointments: this.state.myAppointments.filter((_, i) => i != idx) });
		}

		cancelAppointment = (aptId, idx) => {
			// Uses filter to delete the appointment from state that was successfully 'cancelled' on the database end.
			apiAppointment.delete(aptId)
				.then(response => {
					this.filterOutApt(idx);
				})
				.catch(err => {
				})
		}

		submitFeedback = (aptId, idx, rating, feedback) => {
			const data = {
				rating: rating,
				feedback: feedback,
				status: 1,
			}
			apiAppointment.put(aptId, data)
				.then(res => {
					this.filterOutApt(idx);
				})
				.catch(err => {
					// Something happened
				})
		}


		formatAppointment = (obj, idx) => {
			// Declare variables
			const { appointment, project, user, mentor } = obj;

			// Seperate out the login information
			const { login } = user ? user : mentor; // This is the only difference between the data returned by the apiUser... endpoint and the apiMentor... endpoint.

			// Get formatted date
			const time = new Date(appointment.start_time).toLocaleString('en-US', { timeZone: 'GMT', weekday: 'long', month: 'short', hour: 'numeric', minute: 'numeric', hour12: true});

			const main = (
				<div className="appointment-info">
					<Avatar size="small" login={login} className="appointment-image" />
					<div>
						<a
							style={{ textDecoration: 'none', color: 'darkgreen', fontSize: '1.4em' }}
							href={`https://profile.intra.42.fr/users/${login}`}
						>
							{login}
						</a>
						<h3 style={{ color: 'firebrick' }}>{project.name}</h3>
						<h3>{time}</h3>
					</div>
				</div>
			);


			// Save the Feedback button if needed
			// Perhaps a timeout function?
			const feedback = (
				mentor ? (
					<ButtonModal value="Feedback" className="appointment-feedback-button">
						<Feedback
							main={main}
							cancel={() => this.cancelAppointment(appointment.id, idx)}
							submit={(rating, feedback) => this.submitFeedback(appointment.id, idx, rating, feedback)}
						/>
					</ButtonModal>
				) : (
					<Fragment/>
				)
			);

			// The main appointment row
			return (
				<div key={appointment.id} className="appointment-container">
					{main}
					{feedback}
				</div>
			);
		}

		render() {
			const { myAppointments } = this.state;

			// Set appointments to the map of divs of each appointment
			const appointments = (
				myAppointments.length ?
				myAppointments.map((obj, idx) => this.formatAppointment(obj, idx)) :
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
