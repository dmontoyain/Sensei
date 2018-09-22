import React, { Component, Fragment } from 'react';

// Components
import projectWrap from './projectWrap';
import { apiMentor } from '../../apihandling/api';
import { ButtonModal } from '../Extra/Modal';

// Icon
import settingsIcon from '../../assets/images/settings.png';

// CSS
import './Mentoring.css';


// Main list render for /helpyou
class HelpYouList extends Component {
	constructor(props) {
		super(props);
		const projects = this.filterSubscribed(props.fullProjects);
		this.state = {
			myProjects: projects,
			filteredProjects: projects,
			filter: '',
		};
	};

	componentDidUpdate(prevProps) {
		const obj1 = JSON.stringify(this.props); 
		const obj2 = JSON.stringify(prevProps);

		if (obj1 != obj2) {
			const newProjects = this.filterSubscribed(this.props.fullProjects);
			this.setState({
				myProjects: newProjects,
				filteredProjects: newProjects,
				filter: ''
			});
		}
	}

	filterSubscribed = (data) => {
		return data.filter(d => d.abletomentor == true);
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


	// Sets a single project to it's opposite status
	toggleActive = (idx) => {
		let projectList = this.state.filteredProjects;
		// Api call to toggle Active State
		apiMentor.put(projectList[idx].id, { active: !projectList[idx].active })
			.then(response => {
				projectList[idx].active = !projectList[idx].active;
				this.setState({ filteredProjects: projectList });
			})
			.catch(err => {
				// No change - an error occurred
			});
	}

	// Sets all filtered projects to the given state
	toggleActiveStateAll = (newState) => {
		// Exit if there is nothing to enable
		if (this.state.filteredProjects.length == 0) {
			return ;
		}

		// Copy existing projects in order to update the state later
		const filteredProjects = JSON.parse(JSON.stringify(this.state.filteredProjects));

		// Declare lists
		let projectsToFulfill = [],
			promises = [];

		filteredProjects.forEach(p => p.active != newState ? projectsToFulfill.push(p) : null);

		// Exit if there are no projects to update
		if (projectsToFulfill.length == 0) {
			return ;
		}

		// Make a request to the server to update each of the projects' active states
		projectsToFulfill.forEach((p, i) => {
			promises[i] = new Promise((resolve, reject) =>
				apiMentor.put(p.id, { active: newState })
					.then(res => resolve(res))
					.catch(err=> reject(err))
				);
		});


		// Once all requests have been made, set the new State
		Promise.all(promises)
			.then(res => {
				const myProjects = JSON.parse(JSON.stringify(this.state.myProjects));
				const BreakException = {};
				filteredProjects.forEach(p => {
					p.active = newState;
					try {
						myProjects.forEach(myP => {
							if (myP.id === p.id) {
								myP.active = newState;
								throw BreakException;
							}
						})
					} catch (e) {
						// Do nothing, just escape the inner for each loop early
					}
				});
				this.setState({
					filteredProjects: filteredProjects,
					myProjects: myProjects,
				 });
			})
			.catch(err => {
				// At least one promise failed to return;
			});
	}

	getButton = (item, idx) => {
		if (item.active === false) {
			return <button className='red-switch' onClick={() => this.toggleActive(idx)}>Disabled</button>
		}
		return <button className='green-switch' onClick={() => this.toggleActive(idx)}>Enabled</button>
	}

	render() {
		const { filteredProjects, filter } = this.state;

		return (
			<Fragment>
				<div className="search-container">
					<input onChange={this.filterProjects} className="search-bar" value={filter} />
					<button onClick={this.clearFilter} className="search-clear-button">Clear Filter</button>
					<div className="settings-container">
						<button className="settings-button">
							Options
							<img className="settings-icon" src={settingsIcon} alt='settings'/>
						</button>
						<div className="settings-content">
							<div className="settings-item" onClick={() => this.toggleActiveStateAll(true)}>Enable All</div>
							<div className="settings-item" onClick={() => this.toggleActiveStateAll(false)}>Disable All</div>
						</div>
					</div>
				</div>
				{filteredProjects.map((item, idx) =>
					<div key={item.id} className="project-row" style={{ animation: `fadein ${idx * 0.1}s` }}>
			 			<div className="project-row-name">{item.project.name}</div>
			 			{this.getButton(item, idx)}
		 			</div>
				)}
			</Fragment>
		);
	};
}

const HelpYou = projectWrap(HelpYouList);

export default HelpYou;

