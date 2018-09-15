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
		const { correction_point, first_name, last_name, login } = authClient.profile;
		const { grade, level } = this.cursus;

		return (
			<div className="home-top">
				{/* <div className="profile-text">{`${grade} ${first_name} ${last_name}`}</div> */}
				<div className="profile-avatar">
					<Avatar
					login={login}
					size="medium"
					/>
				</div>
				<div className="profile-info">
					<div className="info-blurb shadow">
						<ul>
							<li className="profile-name">
								<h2>{`${first_name} ${last_name}`}</h2>
							</li>
							<li><h3>Grade:</h3><h4>{`${grade}`}</h4></li>
							<li><h3>Level</h3><h4>{level}</h4></li>
							<li><h3>Correction Point</h3><h4>{`${correction_point}`}</h4></li>
						</ul>
					</div>
					<div className="info-blurb shadow">
						laksdfjklasdjfkladjs
					</div>
				</div>
			</div>
		);
	};
}

export default Profile;
