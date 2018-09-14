import React, { Component, Fragment } from 'react';

// Security

import authClient from '../../security/Authentication';

// Components

import Avatar from '../Extra/Avatar';

// CSS

import './Home.css';

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
		const { first_name, last_name, login } = authClient.profile;
		const { grade, level } = this.cursus;

		return (
			<Fragment>
				<div className="profile-text">{`${grade} ${first_name} ${last_name}`}</div>
				<div className="profile-container">
					<Avatar
						login={login}
						size="medium"
						className="profile-avatar"
					/>
					<div className="profile-info">
						<div className="info-blurb shadow">
							<h1>Level</h1>
							<p>{level}</p>
						</div>
						<div className="info-blurb shadow">
							laksdfjklasdjfkladjs
						</div>
					</div>
				</div>
			</Fragment>
		);
	};
}

export default Profile;
