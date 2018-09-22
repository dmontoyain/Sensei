import React, { Component, Fragment } from 'react';
import PropTypes from 'prop-types';

// Components
import projectWrap from './projectWrap';
import { apiUserProjectsAvailableMentors, apiAppointments, apiMentor } from '../../apihandling/api';
import { ButtonModal } from '../Extra/Modal';
import ScheduleModal from './MentorModals';

// Security
import authClient from '../../security/Authentication';

// CSS
import './Mentoring.css';

// Main List Render for /helpme
class HelpMeList extends Component {
	constructor(props) {
		super(props);
		const projects = this.filterUnsubscribed(props.fullProjects);
		this.state = {
			myProjects: projects,
			filteredProjects: projects,
			filter: '',
		};
	};

	// Compare the props and update if necessary
	componentDidUpdate(prevProps) {
		const obj1 = JSON.stringify(this.props); 
		const obj2 = JSON.stringify(prevProps);

		if (obj1 !== obj2) {
			const newProjects = this.filterUnsubscribed(this.props.fullProjects);
			this.setState({
				myProjects: newProjects,
				filteredProjects: newProjects,
				filter: ''
			});
		}
	}

	filterUnsubscribed = (data) => {
		return data.filter(d => (d.abletomentor == false));
	}

	filterProjects = (e) => {
		const { myProjects } = this.state;
		const { value } = e.target;

		this.setState({ filter: value });

		// If user has input a filter value
		if (value.length) {
			// Filter out any projects where the name has the user's input value
			const valueLower = value.toLowerCase();
			this.setState({ filteredProjects: myProjects.filter(p => p.project.name.toLowerCase().includes(valueLower)) });
		} else {
			// Reset filteredProjects to be the full list of Projects
			this.setState({ filteredProjects: myProjects });
		}
	}

	// Clears the Filter Input
	clearFilter = () => {
		this.setState({ filter: "", filteredProjects: this.state.myProjects, });
	}

	render() {
		const { filteredProjects, filter } = this.state;

		return (
			<Fragment>
				<div className="search-container">
					<input onChange={this.filterProjects} className="search-bar" value={filter} />
					<button onClick={this.clearFilter} className="search-clear-button">Clear Filter</button>
				</div>
				{filteredProjects.map((item, idx) =>
					<div key={item.id} className="project-row" style={{ animation: `fadein ${idx * 0.1}s` }} >
			 			<div className="project-row-name">{item.project.name}</div>
						<ButtonModal value="Schedule Appointment" className="purple-switch">
							<ScheduleModal item={item}/>
						</ButtonModal>
	 				</div>
				)}
			</Fragment>
		);
	};
}

HelpMeList.propTypes = {
	fullProjects: PropTypes.array.isRequired,
}

const HelpMe = projectWrap(HelpMeList);

export default HelpMe;

