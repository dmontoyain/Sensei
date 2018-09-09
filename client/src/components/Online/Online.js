import React, { Fragment} from 'react';

import {
	apiUsersOnline
} from '../../apihandling/api';

//CSS
import './Online.css';

class Online extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			students: [],
		};
	}

	tick = () => {
		apiUsersOnline.get()
			.then(data => {
				this.setState({ students: data.data});
			})
			.catch(err => {
				// FAKE REMOVE LATER
				this.setState({ students: [
					{ login:"jmeier", id: 54 },
					{ login: "bpierce", id: 35353 },
				]});
			})
	}

	componentDidMount() {
		this.tick();
		this.interval = setInterval(() => this.tick(), 60000);
	}

	componentWillUnmount() {
		clearInterval(this.interval);
	}

	render () {
		const { students } = this.state;
		let now = new Date().toLocaleString();
		return (
			<div>
				<p>As of {now}</p>
				<p>There are {students.length} people logged in</p>
			</div>
		);
	}
}

export default Online;
