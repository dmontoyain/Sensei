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
		this.timeout = null;
		this.interval = null;
	}

	tick = () => {
		apiUsersOnline.get()
			.then(data => {
				this.setState({ students: data.data != {} ? data.data : [] });
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
		this.timeout = setTimeout(() => {
			this.interval = setInterval(() => this.tick(), 60000);
		}, (Math.ceil(Date.now() / 60000) * 60000) - Date.now())
	}

	componentWillUnmount() {
		if (this.timeout)
			clearTimeout(this.timeout);
		if (this.interval)
			clearInterval(this.interval);
	}

	render () {
		const { students } = this.state;
		const time = new Date((Math.floor(Date.now() / 60000) * 60000)).toLocaleString();

		if (students.length === 1) {
			return (
				<div className="box">
					<p>As of {time}</p>
					<p>There is {students.length} person logged in</p>
				</div>
			);
		}
			else {
				return (
					<div className="box">
						<p>As of {time}</p>
						<p>There are {students.length} people logged in</p>
					</div>
				);
			}
	}
}

export default Online;
