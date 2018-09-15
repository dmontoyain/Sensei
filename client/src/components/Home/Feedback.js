import React, { Fragment, PureComponent } from 'react';

// CSS
import './Home.css';

class Feedback extends PureComponent {
	constructor(props) {
		super(props);
		this.state = {
			userAbsent: false,
			userRating: 0,
		}
		this.ratings = ['☆☆☆☆☆', '★☆☆☆☆', '★★☆☆☆', '★★★☆☆', '★★★★☆', '★★★★★']
	}

	toggleUserAbsent = () => {
		this.setState(prevState => ({ userAbsent: !prevState.userAbsent }));
	}

	submitFeedback = () => {
		const { cancel } = this.props;
		// DO STUFF
	}

	adjustRating = (idx) => {
		this.setState({ userRating: idx });
	}

	bStar = (idx) => {
		return <h4 className="fb-icon-box" onClick={() => this.adjustRating(idx)} >★</h4>
	}

	wStar = (idx) => {
		return <h4 className="fb-icon-box" onClick={() => this.adjustRating(idx)} >☆</h4>
	}

	noRating = () => {
		return (
			<Fragment>
				{this.wStar(1)}
				{this.wStar(2)}
				{this.wStar(3)}
				{this.wStar(4)}
				{this.wStar(5)}
			</Fragment>
		);
	}

	render() {
		const { main } = this.props;
		const { userAbsent, userRating } = this.state;
		const absent = userAbsent ? '✓' : '▢';

		return (
			<div className="feedback-container">
				{main}
				<div className="fb-absent">
					<h4>Mentor was absent &nbsp;&nbsp;</h4>
					<h4 onClick={this.toggleUserAbsent} className="fb-icon-box">{absent}</h4>
				</div>
				<div className="fb-rating">
					{userRating > 0 ? this.bStar(1) : this.wStar(1)}
					{userRating > 1 ? this.bStar(2) : this.wStar(2)}
					{userRating > 2 ? this.bStar(3) : this.wStar(3)}
					{userRating > 3 ? this.bStar(4) : this.wStar(4)}
					{userRating > 4 ? this.bStar(5) : this.wStar(5)}
				</div>
				<textarea
					placeholder="feedback goes here"
					spellCheck="false"
					style={{ fontSize: '14px', height: '180px', width: '330px', padding: '10px', resize: 'none' }}
				/>
				<div onClick={this.submitFeedback}>
					Submit
				</div>
			</div>
		);
	}
}

export default Feedback;
