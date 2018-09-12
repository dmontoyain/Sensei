import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';

import authClient from '../../security/Authentication';

// CSS
import './HeaderFooter.css';

class LogOutButton extends Component{
	constructor(props) {
		super(props);
		this.state = {
			loggedOut: false,
		}
	}

	logOut = () => {
		authClient.clearCredentials();
		this.setState({ loggedOut: true });
	}

	render() {
		const { loggedOut } = this.state;

		return (
			<div className="logout-button" onClick={this.logOut}>
				Log Out
				{loggedOut ? <Redirect to="/" /> : null}
			</div>
		);
	}
}

export default LogOutButton;
