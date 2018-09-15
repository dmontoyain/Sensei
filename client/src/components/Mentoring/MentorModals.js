import React, { Component } from 'react';

// Components
import { ErrorModal } from '../Extra/Modal.js';

// Authentication
import { apiSubscribeUnSubscribeMentor,
	apiAppointments,
} from '../../apihandling/api';

import authClient from '../../security/Authentication'

// CSS
import './Mentoring.css';


class ScheduleModal extends Component {
	constructor(props) {
		super(props);
		this.state = {
			errorModal: false,
			blockRequest: false,
		}
		this.timeout1 = null;
		this.timeout2 = null;
		this.isM = true;
	}

	blockRequestTimeout = () => {
		// Buttom spam protection
		this.setState({ blockRequest: true });
		this.timeout1 = setTimeout(() => this.setState({ blockRequest: false }), 5000);
	}

	showErrorTimeout = () => {
		// Error modal shows for 6 seconds
		this.setState({ errorModal: true });
		this.timeout2 = setTimeout(() => this.setState({ errorModal: false }), 2000);
	}

	subscribeForAppointment = () => {
		const { item, closeModal } = this.props;
		const { blockRequest } = this.state;

		if (blockRequest)
			return ;
		this.blockRequestTimeout();

		// Api call to create the appointment.
		apiAppointments.post({
				project: item.project.name,
				login: authClient.profile.login,
			})
			.then(response => {
				if (this.isM) {
					this.props.closeModal();
				}
			})
			.catch(err => {
				if (this.isM){
					this.showErrorTimeout();
				}
			});
	}

	componentDidMount() {
		this.isM = true;
	}

	componentWillUnmount() {
		this.isM = false;
		clearTimeout(this.timeout1);
		clearTimeout(this.timeout2);
	}

	render() {
		const { item } = this.props;
		const { name, onlineMentors } = item.project;
		const { errorModal } = this.state;
		const zeroStyle = {
			color: 'crimson',
			fontWeight: 'bold',
		};
		const isStyle = {
			color: 'darkgreen',
			fontWeight: 'bold',
		};
		return (
			<div className="schedule-modal">
				<h2 style={{paddingBottom: "4%"}}>--- {name} ---</h2>
				<span className="s-modal-text">WARNING: This requires ONE correction point</span>
				<span>Mentors available for {name} : <span style={onlineMentors > 0 ? isStyle : zeroStyle}>{onlineMentors}</span></span>
				<button className="s-modal-button" onClick={this.subscribeForAppointment}>Request Assistance!</button>
				<ErrorModal show={errorModal}>
					No Mentors Available
				</ErrorModal>
			</div>
		);
	}
}

export {ScheduleModal};
