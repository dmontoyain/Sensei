import React, { Component, Fragment } from 'react';
import ReactCSSTransitionGroup from 'react-addons-css-transition-group';

import classNames from 'classnames';

import closeIcon from '../../assets/images/close.png';

// A modal wrapper for any component

const withModal = (childComponents, closeModal) => {
	return (
		<Fragment>
			<div className="modal-window">
				<div className="modal-header">
					<img src={closeIcon} alt="close" onClick={closeModal} />
				</div>
				<div className="modal-body">
					{React.Children.map(childComponents, child => React.cloneElement(child, { closeModal: closeModal}))}
				</div>
			</div>
			<div className="modal-background" onClick={closeModal}/>
		</Fragment>
	);
}

// Requires a 'value' for the Button Text

class ButtonModal extends Component {
	constructor(props) {
		super(props);
		this.state = {
			showModal: false,
		};
	};

	closeModal = (e) => {
		e.preventDefault();
		this.setState({ showModal: false });
	}

	openModal = (e) => {
		e.preventDefault();
		this.setState({ showModal: true });
	}

	render() {
		const { value, children, ...rest } = this.props;
		const { showModal } = this.state;

		return (
			<Fragment>
				<button { ...rest } onClick={this.openModal}>{value}</button>
				{showModal ? withModal(children, this.closeModal) : null}
			</Fragment>
		);
	};
}

// For Error messages that display for a few seconds

class ErrorModal extends Component {
	constructor(props) {
		super(props);
		this.state = {
			show: false,
		}
	}

	closeModal = () => {
		this.setState({ show: false });
	}

	openModal = () => {
		this.setState({ show: true });
	}

	componentDidMount() {
		setTimeout(() => this.openModal(), 1000);
		setTimeout(() => this.closeModal(), 4500);
	}

	render() {
		const text = this.props.children;
		const { show } = this.state;

		if (!show) return null;

		return (
			<Fragment>
				<ReactCSSTransitionGroup
					transitionName='fade'
					transitionEnterTimeout={1000}
					transitionLeaveTimeout={500}
				>
					<div key="fake" className="modal-error-window" onClick={this.closeModal}>
						{text}
					</div>
				</ReactCSSTransitionGroup>
			</Fragment>
		);
	}
}

export {
	withModal,
	ButtonModal,
	ErrorModal,
}
