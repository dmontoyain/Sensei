import React, { Component, Fragment } from 'react';

// Components
import { apiUserProjectsAvailableMentors } from '../../apihandling/api';
import { ErrorModal } from '../Extra/Modal';

// Authentication
import authClient from '../../security/Authentication';

// CSS
import './Mentoring.css';


// HOC that wraps the Mentoring class
const projectWrap = (WrappedComponent) => {
	class HOC extends Component {
		constructor(props) {
			super(props);
			this.state = {
				fullProjects: [],
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
					});
				})
				.catch(err => {
					this.showErrorTimeout();
				});
		}

		componentWillUnmount() {
			clearTimeout(this.errorTimeout);
		}

		showErrorTimeout = () => {
			this.setState({ serverError: true });
			this.errorTimeout = setTimeout(() => this.setState({ serverError: false }), 3000);
		}

		render() {
			const { serverError } = this.state;
			return (
				<Fragment>
					<WrappedComponent { ...this.state } className="container"/>
					<ErrorModal show={serverError}>Server appears to be offline</ErrorModal>
				</Fragment>
			);
		}
	}

	return HOC;
}

export default projectWrap;
