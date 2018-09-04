import React, { Component } from 'react';
import { apiUsers } from '../../apihandling/api';
import authClient from '../../security/Authentication';

// CSS
import './Home.css';


class Home extends Component {
	constructor(props) {
		super(props);
		this.state = {
			listOfUsers: [],
			hello: "hello",
		}
	}

	componentWillMount() {
		apiUsers.get()
			.then(data => {
				this.setState({ listOfUsers: data.data });
			})
			.catch(err => {
			})
	}

	render() {
		const { listOfUsers } = this.state;

		return (
			<div className="flex bg-purple">
				<h1>HOME</h1>
				<h1>HOME</h1>
				<div>HOME</div>
				<div>HOME</div>
				{listOfUsers.map(user => (
					<h1 className="" key={user.id}>{user.login}</h1>
				))}
			</div>
		);
	}
}

export default Home;
