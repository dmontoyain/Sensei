
import React, { Component, Fragment } from 'react';

import classNames from 'classnames';

const Avatar = ({ ...props }) => {

	const { size, login, className, style } = { ...props };

	return (
		<img
			src={`https://cdn.intra.42.fr/users/${size}_${login}.jpg`}
			className={classNames("avatar-image", className)}
			style={style}
		/>
	);
}

export default Avatar
