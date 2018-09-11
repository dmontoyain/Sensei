import React from 'react';

import classNames from 'classnames';

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

export default ScheduleModal;
