import React, { Component, Fragment } from 'react';

// Components
import { apiUserProjectsAvailableMentors, apiAppointments, apiMentor } from '../../apihandling/api';
import { ButtonModal } from '../Extra/Modal';
import { ScheduleModal, ActivationModal } from './MentorModals';

// Security
import authClient from '../../security/Authentication';

// CSS
import './Mentoring.css';

// Main Page Render for /ineedhelp

class HelpMeList extends Component {
	constructor(props) {
		super(props);
		this.state = {
			myProjects: this.filterSubscribed(props.filteredProjects),
			requested: true,
		};
	};

	filterSubscribed = (data) => {
		return data.filter(d => (d.abletomentor == false));
	}

	componentWillReceiveProps(nextProps) {
		this.setState({ myProjects: this.filterSubscribed(nextProps.filteredProjects)});
	}

	render() {
		const { myProjects } = this.state;

		return (
			<div>
				{myProjects.map((item, idx) =>
					<div key={item.id} className="project-row" style={{ animation: `fadein ${idx * 0.1}s` }} >
			 			<span id="projectName">{item.project.name}</span>
						<ButtonModal value="SCHEDULE APPOINTMENT" className="schedule">
							<ScheduleModal item={item}/>
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
			myProjects: this.filterSubscribed(props.filteredProjects),
		};
	};

	filterSubscribed = (data) => {
		return data.filter(d => d.abletomentor == true);
	}

	componentWillReceiveProps(nextProps) {
		this.setState({ myProjects: this.filterSubscribed(nextProps.filteredProjects)});
	}

	toggleActive = (idx) => {
		let projectList = this.state.myProjects;

		// Api call to toggle Active State
		apiMentor.put(projectList[idx].id, { active: !projectList[idx].active })
			.then(response => {
				projectList[idx].active = !projectList[idx].active;
				this.setState({ myProjects: projectList });
			})
			.catch(err => {
				// No change - an error occurred
			});
	}

	render() {
		const { myProjects } = this.state;
		const onStyle = {
			color: 'white',
			backgroundColor: 'crimson',
			padding: '5px',
			border: 'none',
			borderRadius: '4px',
		};
		const offStyle = {
			color: 'white',
			backgroundColor: 'darkgreen',
			padding: '5px',
			border: 'none',
			borderRadius: '4px',
		}
		return (
			<div>
				{myProjects.map((item, idx) =>
					<div key={item.id} className="project-row" style={{ animation: `fadein ${idx * 0.1}s` }}>
			 			<span>{item.project.name}</span>
						<ButtonModal
							className="switch" className="schedule"
							style={item.active === false ? offStyle : onStyle}
							value={item.active === false ? "Begin Sensei Service" : "Finish Sensei Service"}
						>
							<ActivationModal item={item} toggleActive={() => this.toggleActive(idx)}/>
						</ButtonModal>
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
			apiCall(authClient.profile.login)
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
			if (e.target.value.length) {
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
					<div className="search_box">
						<input onChange={this.filterProjects} className="search-bar" value={filter} />
						<button onClick={this.clearFilter} className="search-clear"> Clear Filter </button>
					</div>
					<WrappedComponent { ...this.state } className="container"/>
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
