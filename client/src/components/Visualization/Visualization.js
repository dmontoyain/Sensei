import React, { Fragment, PureComponent } from 'react';
import * as d3 from "d3";

// Components
import authClient from '../../security/Authentication';

// API
import { apiUserStats } from '../../apihandling/api';

class Visualization extends PureComponent {
	constructor(props) {
		super(props);
		this.state = {
			stats: [],
			width: screen.width,
			height: screen.height,
		};
	}

	componentWillMount() {
		apiUserStats.get(authClient.profile.id)
			.then(res => {
				this.setState({ stats: res.data.mentorStats })
			})
			.catch(err => {
				// Do nothing
			})
	}

	renderBubbles = () => {
		const { stats } = this.state;

		if (stats.length === 0) return;


	}

	render() {
		const bubbles = this.renderBubbles();

		return (
			<Fragment>
			</Fragment>
		);
	}
}

export default Visualization;
