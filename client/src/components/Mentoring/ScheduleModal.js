import React from 'react';

import classNames from 'classnames';

import apiSubscribeUnSubscribeMentor from '../../apihandling/api';
// CSS
import './Mentoring.css';

const ScheduleModal = ({ ...props }) => {

	const { item } = { ...props }

	return (
		<div className="schedule-modal">
			<span>{item.project.name}</span>
			{item.project.onlineMentors}
		</div>
	);
}

const ActivationModal = ({ ...props }, id) => {
	const { item } = { ...props }
	return (
		<div className="schedule-modal" style={{textAlign: 'center'}}>
			<span>{item.active ? "Stop serving as a Sensei for" : "Serve as a Sensei for"}</span>
			<span>{item.project.name}?</span>
		</div>
	)
}

export {
	ScheduleModal,
	ActivationModal,
}
