import React, { Component, Fragment } from 'react';

// Security

import authClient from '../../security/Authentication';

// Components

import Avatar from '../Extra/Avatar';

// CSS

import './Home.css';

// Main Component

const InfoBlurb = ({ ...props }) => {
	const { label, text } = { ...props };

	return (
		<div className="info-blurb shadow">
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
		// Grab the correct curses for the user
		this.cursus = authClient.profile.cursus_users.filter(cur => cur.cursus_id == 1)[0];
		console.log("PROFILE", authClient.profile);
	};

	render() {
		const { first_name, last_name } = authClient.profile;
		const { grade, level } = this.cursus;

		return (
			<Fragment>
				<div className="profile-text">{`${grade} ${first_name} ${last_name}`}</div>
				<div className="profile-container">
					<Avatar
						login={authClient.profile.login}
						size="medium"
						className="profile-avatar"
					/>
					<div className="profile-info">
						<InfoBlurb label="Level" text={level} />
						<InfoBlurb label="CP" text="42" />
						<InfoBlurb label="Apts" text="3" />
						<InfoBlurb label="Lessons" text="5" />
					</div>
				</div>
			</Fragment>
		);
	};
}

export default Profile;
