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
				<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAALxSURBVGhD7ZhLiM1RHMfn6RUy5bEhG0RR0sRmapRJTTY2Hgt7sRKRhWxs1IQpsbBgo5ASkiiWFlNMKTZEKTVNNE0eSXL5/M75Utdt7j3nf+/9/0/6f+rbefzeNTX3fzoaUalUtqAbaOJXvkxT8xHrLtSpdrJBosPop0tbIPRwnaVXbcVB4E4SVFymBKCVEbUWB4GvlMPB+SsaZ/s0D1HrA+tfOP9AK9ReGARsULyD8xu0TOZcoN5sdEctODgfkDkMAoYV6+B8SqZcoe52teDgHPfnRcAOxf7huEy5Qt0BX95DXxdlCqMcpMVQtxzEUQ7SYqib/iDU2IQeo4O6qoG6fdjHfAvpDnJZua3BsyxdMlXB/Tzst+WX5CD3lNvB+RaaK3MVmLuxnUfpD2JwN4aWyqUGbOu0DaOoQQzu37KslVtzFDmIgW0KDco1O1kGwacH9YWKGg9ZZwT7d7RP6bMROwj+e9Fn+bYMchon2Wb71CU4dpB38msL5L/CMkvlwokdBPu0d2sf9GQPEYtUMowUBzHo6wVaqbKNSXUQg94mUL9K1yflQQz6+4JWqfzMpDwIvdlryn6Vrk+qg9DXJzSsso1JcRB6es+yUSXDiB0E/0n5tQXyP0fLVS6c2EGwn/ZurYdeHqAFKhVH7CAGMf342ct5kPB/xloXfC6x9KhEPFkGiYUa9X792uN58zWLHIT7b2iP3JqjqEG4+8gyIJcasM3XNowiBuH8Gq2WuQZsu9E5HcMgII9Briq3DfGEZbFMNWA/ioz0Hh/IOUSdSXSN/RxdV8G9vZ5csAaMJAcJgbrlk6mjHKTFULccxPHfDsL5hEy5QumtvgMPfYzKFAYBmxXr4Gz/sLplzg3qjvgOPJyPyBQGMb0ETflwD+dxdIatfXu0XdS6z/ovcV+IBomOKTgJ6OeuWouDWPt5cNOnKRb6eImWqLV4yNFFgkPIPvxzh7r2ajKKFqql5iBnJ8nWoEH2Q+0Wdbah9ewDH647On4Df++3nsnyaMwAAAAASUVORK5CYII="></img>
				LogOut
				{loggedOut ? <Redirect to="/" /> : null}
			</div>
		);
	}
}

export default LogOutButton;
