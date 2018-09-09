import React, { Component } from 'react';

// Security

import authClient from '../../security/Authentication';

// Components

import Avatar from '../Extra/Avatar';

// Main Component

const InfoBlurb = ({ ...props }) => {
	const { label, text } = { ...props };

	return (
		<div className="info-blurb">
			<h4>{label}</h4>
			<p>{text}</p>
		</div>
	);
}

class Profile extends Component {
	constructor(props) {
		super(props);
		this.state = {
		};
	};

	render() {
		return (
			<div className="profile-container">
				<Avatar login="nwang"/*{authClient.login}*/ size="medium" className="profile-avatar" />
				<div className="profile-info">
					<InfoBlurb label="Level" text="15" />
					<InfoBlurb label="CP" text="42" />
					<InfoBlurb label="Apts" text="3" />
					<InfoBlurb label="Lessons" text="5" />
				</div>
			</div>
		);
	};
}

export default Profile;
