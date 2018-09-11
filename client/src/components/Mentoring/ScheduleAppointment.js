import React from 'react';

import classNames from 'classnames';

// CSS
import './Mentoring.css';

const ScheduleAppointment = ({ ...props }) => {

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

export default ScheduleAppointment;
