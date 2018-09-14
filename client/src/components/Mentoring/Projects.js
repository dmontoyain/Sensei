import React, { Component, Fragment } from 'react';

// Components
import { apiUserProjectsAvailableMentors, apiAppointments, apiMentor } from '../../apihandling/api';
import { ButtonModal, ErrorModal } from '../Extra/Modal';
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
		console.log(myProjects);
		return (
			<Fragment>
				{myProjects.map((item, idx) =>
					<div key={item.id} className="project-row" style={{ animation: `fadein ${idx * 0.1}s` }} >
			 			<div className="project-row-name">{item.project.name}</div>
						<ButtonModal value="Schedule Appointment" className="project-row-schedule-button">
							<ScheduleModal item={item}/>
						</ButtonModal>
	 				</div>
				)}
			</Fragment>
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
			<Fragment>
				{myProjects.map((item, idx) =>
					<div key={item.id} className="project-row" style={{ animation: `fadein ${idx * 0.1}s` }}>
			 			<div className="project-row-name">{item.project.name}</div>
						<ButtonModal
							className="switch" className="project-row-schedule-button"
							style={item.active === false ? offStyle : onStyle}
							value={item.active === false ? "Begin Sensei Service" : "Finish Sensei Service"}
						>
							<ActivationModal item={item} toggleActive={() => this.toggleActive(idx)}/>
						</ButtonModal>
		 			</div>
				)}
			</Fragment>
		);
	};
}


// HOC that wraps the Mentoring class
const projectWrap = (WrappedComponent) => {
	class HOC extends Component {
		constructor(props) {
			super(props);
			this.state = {
				fullProjects: [],
				filteredProjects: [],
				filter: "",
				serverError: false,
			}
			this.errorTimeout = null;
		}

		componentWillMount() {
			// Makes the api call given through the 
			apiUserProjectsAvailableMentors.get(authClient.profile.login)
				.then(data => {
					this.setState({
						fullProjects: data.data === {} ? [] : data.data,
						filteredProjects:data.data === {} ? [] : data.data,
					});
				})
				.catch(err => {
					this.showErrorTimeout();
				});
		}

		componentWillUnmount() {
			if (this.errorTimeout) {
				clearTimeout(this.errorTimeout);
			}
		}

		showErrorTimeout = () => {
			this.setState({ serverError: true });
			this.errorTimeout = setTimeout(() => this.setState({ serverError: false }), 3000);
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
		clearFilter = () => {
			const { fullProjects } = this.state;
			this.setState({
				filter: "",
				filteredProjects: fullProjects,
			});
		}

		render() {
			const { filter, filteredProjects, serverError } = this.state;

			return (
				<Fragment>
					<div className="search-container">
						<input onChange={this.filterProjects} className="search-bar" value={filter} />
						<button onClick={this.clearFilter} className="search-clear-button">Clear Filter</button>
					</div>
					<WrappedComponent { ...this.state } className="container"/>
					<ErrorModal show={serverError}>Server appears to be offline</ErrorModal>
				</Fragment>
			);
		}
	}

	return HOC;
}

const HelpMe = projectWrap(HelpMeList);

const HelpYou = projectWrap(HelpYouList);

export {
	HelpMe,
	HelpYou,
}
