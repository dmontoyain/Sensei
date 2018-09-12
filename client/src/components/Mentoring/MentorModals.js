import React from 'react';

import { apiSubscribeUnSubscribeMentor } from '../../apihandling/api';

// CSS
import './Mentoring.css';

const ScheduleModal = ({ ...props }) => {

	const { item } = { ...props }

	const subscribeForAppointment = (e, item) => {
		e.preventDefault();
		// Construct body of post request
		const body = {
			project: item.project.name,
			login: authClient.profile.login,
		};

		// Api call to create the appointment.
		apiAppointments.post(body)
			.then(response => {

			})
			.catch(err => {

			});
	}

	return (
		<div className="schedule-modal">
			<span>You have requested assistance on</span>
			<span>{item.project.name}</span>
			<span>The button below will search for any available mentors to come to the rescue</span>
			<span>WARNING: This requires ONE correction point. Do you wish to proceed?</span>
			{item.project.onlineMentors}
			<button onClick={e => this.subscribeForAppointment(e, item)}>Request Assistance!</button>
		</div>
	);
}


const ActivationModal = ({ ...props }) => {
	const { item, toggleActive } = { ...props }
	return (
		<div className="schedule-modal" style={{textAlign: 'center'}}>
			<span>{item.active ? "Stop serving as a Sensei for" : "Serve as a Sensei for"}</span>
			<span>{item.project.name}?</span>
			<button onClick={toggleActive}>OK</button>
		</div>
	)
}

export {
	ScheduleModal,
	ActivationModal,
}
