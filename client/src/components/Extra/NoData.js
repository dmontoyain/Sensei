import React, { Fragment } from 'react';

// Icon

import noData from '../../assets/images/floatingguru.png';

// CSS

import './Extra.css';

const NoData = ({ ...props }) => {
	const { text, icon } = { ...props };

	return (
		<div className="no-data-container">
			<img className="no-data-icon" src={icon} alt="No Data" />
			<h3 className="no-data-text">{text.toUpperCase()}</h3>
		</div>
	);
}

export default NoData;
