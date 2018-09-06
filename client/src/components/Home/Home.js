import React, { Component } from 'react';

import {
	apiPendingAppointmentsAsMentor,
	apiPendingAppointmentsAsUser
} from '../../apihandling/api';

import authClient from '../../security/Authentication';

// CSS
import './Home.css';


function appointmentWrap(WrappedComponent, apiCall) {
	return class extends React.Component {
		constructor(props) {
			super(props);
			this.state = {
				myAppointments: [],
			}
		}

		componentWillMount() {
			apiCall.get("nwang")//authClient.login)
				.then(data => {
					this.setState({ myAppointments: data.data === {} ? [] : data.data });
				})
				.catch(err => {
					return ;
				})
		}

		render() {
			const { myAppointments } = this.state;

			return ( <WrappedComponent /> );
		}
	}
}

class Appointments extends Component {
	constructor(props) {
		super(props);
		this.state = {
			myAppointments: [],
		};
	}

	componentWillMount() {
		const userApts = apiPendingAppointmentsAsUser.get("nwang")//authClient.login)
			.then(data => {
				return data.data === {} ? [] : data.data;
			})
			.catch(err => {
				return [];
			});

		const mentorApts = apiPendingAppointmentsAsMentor.get("nwang")//authClient.login)
			.then(data => {
				return data.data === {} ? [] : data.data;
			})
			.catch(err => {
				return [];
			});

		Promise.all([userApts, mentorApts])
			.then(values => {
				console.log(values);
			})
			.catch(err => {
				console.log("PROMISE ALL FAIL", err);
			})
	}

	render() {
		const { myAppointments } = this.state;

		return (
			<div>
				{myAppointments.map(apnt => {
					<span>{apnt}</span>
				})}
			</div>
		);
	}
}


class Home extends Component {
	constructor(props) {
		super(props);
		this.state = {
			listOfUsers: [],
			hello: "hello",
		}
	}

	componentWillMount() {
	}

	render() {
		const { listOfUsers } = this.state;

		return (
			<div>
				<div className="flex flex-wrap">
					<Appointments />
				</div>
				<div className="flex">
					{listOfUsers.map(user => (
						<h1 className="" key={user.id}>{user.login}</h1>
					))}
				</div>
			</div>
		);
	}
}

export default Home;
