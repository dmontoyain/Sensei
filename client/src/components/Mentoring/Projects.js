import React, { Component, Fragment } from 'react';

// Components

import {
	apiUserProjectsAvailableMentors,
	apiAppointments,
} from '../../apihandling/api';
import { ButtonModal } from '../Extra/Modal';
import ScheduleModal from './ScheduleModal';

// CSS

import './Mentoring.css';

// Main Page Render for /ineedhelp

class HelpMeList extends Component {
	constructor(props) {
		super(props);
		this.state = {
			myProjects: this.filterSubscribed(props.filteredProjects),
		};
	};

	filterSubscribed = (data) => {
		return data.filter(d => d.abletomentor == false);
	}

	subscribeForAppointment = (e, item) => {
		e.preventDefault();
		// Construct body of post request
		const body = {
			project: item.project.name,
			login: authClient.profile.login,
		};

		// Api call to create the appointment.
		apiAppointments.post(body)
			.then(response => {

			})
			.catch(err => {

			});
	}

	componentWillReceiveProps(nextProps) {
		this.setState({ myProjects: this.filterSubscribed(nextProps.filteredProjects)});
	}

	render() {
		const { myProjects } = this.state;

		return (
			<div>
				{myProjects.map((item, idx) =>
					<div key={item.id} className="project-row" style={{ animation: `fadein ${idx * 0.1}s` }}>
			 			<span id="projectName">{item.project.name}</span>
						<span id="mentorsAvailable">{item.mass}</span>
						<span id="projectNameDisplay">{item.name}</span>
						<ButtonModal value="SCHEDULE APPOINTMENT">
							<ScheduleModal item={item} />
						</ButtonModal>
		 			</div>
				)}
			</div>
		);
	};
}

// Main Page Render for /iwannhelp

class HelpYouList extends Component {
	constructor(props) {
		super(props);
		this.state = {
			myProjects: [],
		};
	};

	filterSubscribed = (data) => {
		console.log(data);
		return data.filter(d => d.abletomentor == true);
	}

	componentWillReceiveProps(nextProps) {
		this.setState({ myProjects: this.filterSubscribed(nextProps.filteredProjects)});
	}

	render() {
		const { myProjects } = this.state;

		return (
			<div>
				{myProjects.map(item =>
					<div key={item.id} className="cell" id={item.mass > 100 ? "mentorsAvailableTrue" : "mentorsAvailableFalse"}>
			 			<span id="projectName">{item.project.name}</span>
			 			<span id="mentorText">Mentors Available:</span>
						<span id="mentorsAvailable">{item.mass}</span>
						<span id="projectNameDisplay">{item.name}</span>
		 			</div>
				)}
			</div>
		);
	};
}


// HOC that wraps the Mentoring class
const projectWrap = (WrappedComponent, apiCall) => {
	class HOC extends Component {
		constructor(props) {
			super(props);
			this.state = {
				fullProjects: [],
				filteredProjects: [],
				filter: "",
			}
		}

		componentWillMount() {
			// Makes the api call given through the 
			apiCall("nwang")//authClient.login)
				.then(data => {
					this.setState({
						fullProjects: data.data === {} ? [] : data.data,
						filteredProjects:data.data === {} ? [] : data.data,
					});
				})
				.catch(err => {
					this.setState({
						fullProjects: [
							{ fake: "fake", deleteme: "Delete me later", start_time: "2018-08-10T18:19:49.955709+00:00", name: 'heyooo'},
							{ fake: "DOUBLEfake", deleteme: "This is just a test", start_time: "2018-08-09T14:08:36.695116+00:00", name: 'yoz'},
						],
						filteredProjects: [
							{ fake: "fake", deleteme: "Delete me later", start_time: "2018-08-10T18:19:49.955709+00:00", name: 'heyooo' },
							{ fake: "DOUBLEfake", deleteme: "This is just a test", start_time: "2018-08-09T14:08:36.695116+00:00", name: 'yoz'},
						],
					})
				});
		}

		filterProjects = (e) => {
			const { fullProjects, filter } = this.state;

			this.setState({ filter: e.target.value });

			// If user has input a filter value
			if (filter.length) {
				// Filter out any projects where the name has the user's input value
				this.setState({ filteredProjects: fullProjects.filter(p => p.project.name.toLowerCase().includes(e.target.value.toLowerCase())) });
			} else {
				// Reset filteredProjects to be the full list of Projects
				this.setState({ filteredProjects: fullProjects });
			}
		}

		// Clears the Filter Input
		clearFilter = (e) => {
			e.preventDefault();
			const { fullProjects } = this.state;
			this.setState({
				filter: "",
				filteredProjects: fullProjects,
			});
		}

		render() {
			const { filter, filteredProjects } = this.state;

			return (
				<Fragment>
					<input onChange={this.filterProjects} value={filter} />
					<button onClick={this.clearFilter}>Clear Filter </button>
					<WrappedComponent { ...this.state } />
				</Fragment>
			);
		}
	}

	return HOC;
}

const HelpMe = projectWrap(HelpMeList, apiUserProjectsAvailableMentors.get);

const HelpYou = projectWrap(HelpYouList, apiUserProjectsAvailableMentors.get);

export {
	HelpMe,
	HelpYou,
}
