import React, { Component, Fragment } from 'react';
import PropTypes from 'prop-types';

import classNames from 'classnames';

import closeIcon from '../../assets/images/close.png';

// CSS
import './Extra.css';

// A modal wrapper for any component

const withModal = (childComponents, closeModal) => {
	const childrenWithProps = React.Children.map(childComponents, child => typeof(child) != 'string' ? React.cloneElement(child, { closeModal: closeModal}) : child);

	return (
		<Fragment>
			<div className="modal-window">
				<div className="modal-header">
					<img src={closeIcon} alt="close" onClick={closeModal} />
				</div>
				<div className="modal-body">
					{childrenWithProps}
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

	closeModal = () => {
		this.setState({ showModal: false });
	}

	openModal = () => {
		this.setState({ showModal: true });
	}

	render() {
		const { value, children, ...rest } = this.props;
		const { showModal } = this.state;
		console.log(rest);

		const modal = (showModal ? withModal(children, this.closeModal) : <Fragment></Fragment>);

		return (
			<Fragment>
				{modal}
				<button { ...rest } onClick={this.openModal}>{value}</button>
			</Fragment>
		);
	};
}

ButtonModal.propTypes = {
	value: PropTypes.any.isRequired,
}

// For Error messages that display for a few seconds

class ErrorModal extends Component {
	constructor(props) {
		super(props);
		this.state = {
			className: null,
		}
		this.timeout = null;
	}

	openModal = () => {
		this.setState({ className: 'fadeIn' });
	}

	closeModal = () => {
		const { className } = this.state;

		if (className === 'fadeIn') {
			this.setState({ className: 'fadeOut' });
			this.timeout = setTimeout(() => {
				this.setState({ className: null });
			}, 700);
		}
	}

	componentWillUnmount() {
		clearTimeout(this.timeout);
	}

	componentDidUpdate(prevProps) {
		const { show } = this.props;

		if (show !== prevProps.show && show === true) {
			this.openModal();
		} else if (show != prevProps.show && show === false) {
			this.closeModal();
		}
	}

	render() {
		const text = this.props.children;
		const { className } = this.state;

		if (!className) return (<Fragment></Fragment>);

		return (
			<div className={classNames("error-modal", className)} onClick={this.closeModal}>
				{text}
			</div>
		);
	}
}

ErrorModal.propTypes = {
	show: PropTypes.bool,
}

export {
	withModal,
	ButtonModal,
	ErrorModal,
}
