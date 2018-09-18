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

	getItem = (a, b) => {
		return (
			<div className="user-info-text">
				<span className="user-info-text-left">{a}</span>
				<span className="user-info-text-right">{b}</span>
			</div>
		);
	}

	render() {
		const { correction_point, first_name, last_name, login } = authClient.profile;
		console.log(authClient.profile);
		console.log(authClient.profile);
		console.log(authClient.profile);
		console.log(authClient.profile);
		console.log(authClient.profile);
		console.log(authClient.profile);
		console.log(authClient.profile);
		const { grade, level } = this.cursus;

		return (
			<div className="home-top">
				<div className="profile-avatar">
					<Avatar
					login={login}
					size="medium"
					/>
				</div>
				<div className="profile-info">
					<div className="info-blurb shadow">
						<div className="profile-name">{`${first_name} ${last_name}`}</div>
						{this.getItem('Grade:', grade)}
						{this.getItem('Level:', level)}
						{this.getItem('Correction Point:', correction_point)}
					</div>
					<div className="info-blurb shadow">
						<div className="profile-name"> Shihan {login} </div>
						{this.getItem('Genin:', '10 / 25')}
						{this.getItem('Chunin:', '3 / 12')}
						{this.getItem('Rate:', '5')}
					</div>
				</div>
			</div>
		);
	};
}

export default Profile;