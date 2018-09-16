import React, { Fragment, PureComponent } from 'react';
import PropTypes from 'prop-types';

// Components
import Rating from '../Extra/Rating';
import { ErrorModal } from '../Extra/Modal';

// CSS
import './Home.css';


class Feedback extends PureComponent {
	constructor(props) {
		super(props);
		this.state = {
			userAbsent: false,
			userRating: 0,
			feedback: "",
			ratingBorder: "2px solid white",
			taBorder: "2px solid lightgrey",
		}
	}

	submitFeedback = () => {
		const { cancel } = this.props;
		const { userAbsent, userRating, feedback } = this.state;
		let errOccurred = false;

		if (!userAbsent && userRating === 0) {
			errOccurred = true;
			this.setState({ ratingBorder: "2px solid red" });
		}

		if (!userAbsent && !feedback.length) {
			errOccurred = true;
			this.setState({ taBorder: "2px solid red" });
		}

		// Either submit the feedback, or cancel the appointment if there are no user errors
		if (!errOccurred) {
			if (userAbsent) {
				// Cancel appointment
				this.props.cancel();
			} else {
				// Submit appointment
				this.props.submit(userRating, feedback);
			}
		}
	}

	adjustAbsent = () => {
		this.setState(prevState => ({
			userAbsent: !prevState.userAbsent,
			ratingBorder: '2px solid white',
			taBorder: '2px solid lightgrey',
		}));
	}

	adjustRating = (idx) => {
		this.setState({ userRating: idx, ratingBorder: '2px solid white' });
	}

	adjustFeedback = (e) => {
		this.setState({ feedback: e.target.value, taBorder: '2px solid lightgrey' });
	}

	render() {
		const { main } = this.props;
		const { userAbsent, userRating, feedback, ratingBorder, taBorder} = this.state;
		const absent = userAbsent ? '✓' : '▢';

		return (
			<Fragment>
				<div className="feedback-container">

					{main}

					<div className="fb-absent">
						<h4>Mentor was absent &nbsp;&nbsp;</h4>
						<h4 onClick={this.adjustAbsent} className="fb-icon-box">{absent}</h4>
					</div>

					<div className="fb-rating">
						<h4 style={{ border: ratingBorder }}>Rate your Mentor &nbsp;&nbsp;</h4>
						<Rating onClick={(r) => this.adjustRating(r)} size={5}/>
					</div>

					<textarea
						placeholder="feedback goes here"
						value={feedback}
						onChange={this.adjustFeedback}
						spellCheck="false"
						style={{ fontSize: '14px', height: '180px', width: '330px', padding: '10px', resize: 'none', border: taBorder }}
					/>

					<div className="fb-submit" onClick={this.submitFeedback}>
						Submit Feedback
					</div>

				</div>
			</Fragment>
		);
	}
}

Feedback.propTypes = {
	main: PropTypes.element,
	cancel: PropTypes.func,
	submitFeedback: PropTypes.func,
}

export default Feedback;
