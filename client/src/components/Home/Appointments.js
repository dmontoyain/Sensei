import React, { Component, Fragment } from 'react';

import {
	apiPendingAppointmentsAsMentor,
	apiPendingAppointmentsAsUser,
	apiMentorPendingAppointments,
	apiUserPendingAppointments,
} from '../../apihandling/api';


// Components

import NoData from '../Extra/NoData';
import Avatar from '../Extra/Avatar';

// Security

import authClient from '../../security/Authentication';

// Icons

import noDataOne from '../../assets/images/floatingguru.png';
import noDataTwo from '../../assets/images/floatingguru2.png';

// CSS

import './Home.css'

const monthsRef = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "Jun.", "Jul.", "Aug.", "Sep.", "Oct.", "Nov.", "Dec."];
const daysRef = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

function formatTime(startTime) {
	const newDate = new Date(startTime);
	return {
		day: daysRef[newDate.getDay()],
		mth: monthsRef[newDate.getMonth()],
		dayN: newDate.getDate(),
		hr: newDate.getHours(),
		mn: newDate.getMinutes(),
		sc: newDate.getSeconds(),
	}
}

// main container style
const style = {
	display: 'flex',
	marginBottom: '30px',
	borderBottom: '1px solid firebrick',
}

// Avatar styling
const imageStyle = {
	borderRadius: '4px',
	maxHeight: '80px',
	marginRight: '20px',
}

// a tag styling
const aStyle = {
	textDecoration: 'none',
	color: 'darkgreen',
}


function formatStringForUser(obj) {
	const { appointment, user } = obj;
	const t = formatTime(appointment.start_time);
	const time = new Date(appointment.start_time).toLocaleString('en-US', { weekday: 'long', month: 'short', hour: 'numeric', minute: 'numeric', hour12: true});
	return `You have an appointment on ${time}`;
};

function formatStringForMentor(obj) {
	const { appointment, user } = obj;

	// Get formatted date
	const t = formatTime(appointment.start_time);

	const time = new Date(appointment.start_time).toLocaleString('en-US', { timeZone: 'America/Los_Angeles', weekday: 'long', month: 'short', hour: 'numeric', minute: 'numeric', hour12: true});
	return (
		<div key={appointment.id} style={style}>
			<Avatar size="small" login={user.login} style={imageStyle} />
			<div>
				<a style={aStyle} href={`https://profile.intra.42.fr/users/${user.login}`}>
					<h2>{`${user.login}`}</h2>
				</a>
				<h3>{`${time}`}</h3><br/><br/>
			</div>
		</div>
	);
};


const Appointments = ({ ...props }) => {

	const { myAppointments, noDataIcon, stringFormatter } = { ...props };

	if (!myAppointments.length) {
		return <NoData text="No Appointments" icon={noDataIcon} />;
	}

	return (
		<div style={{ marginTop: '10px'}}>
			{myAppointments.map(obj => stringFormatter(obj))}
		</div>
	);
}

// HOC that wraps the Appointments class
const appointmentWrap = (WrappedComponent, apiCall, title, noDataIcon, stringFormatter) => {
	class HOC extends Component {
		constructor(props) {
			super(props);
			this.state = {
				myAppointments: [],
				noDataIcon: noDataIcon,
			}
		}

		componentWillMount() {
			console.log("PROFILE", authClient.profile.id);
			apiCall.get(authClient.profile.id)
				.then(data => {
					this.setState({ myAppointments: data.data === {} ? [] : data.data });
				})
				.catch(err => {
					// No appointments for user
				});
		}

		render() {
			return (
				<Fragment>
					<h4 className="home-box-title">{title}</h4>
					<WrappedComponent
						{ ...this.state }
						stringFormatter={stringFormatter}
					/>
				</Fragment>
			);
		}
	}

	return HOC;
}



const AppointmentsAsUser = appointmentWrap(Appointments, apiUserPendingAppointments, "Learning", noDataOne, formatStringForUser);

const AppointmentsAsMentor = appointmentWrap(Appointments, apiMentorPendingAppointments, "Teaching", noDataTwo, formatStringForMentor);

export {
	AppointmentsAsUser,
	AppointmentsAsMentor,
}
