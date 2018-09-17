import React, { PureComponent, Fragment } from 'react';
import PropTypes from 'prop-types';

class Rating extends PureComponent {
	constructor(props) {
		super(props);
		this.state = {
			rating: 0, // default to zero
		}
	}

	adjustRating = (rating) => {
		const realRating = (rating === this.state.rating) ? 0 : rating;
		this.setState({ rating: realRating });
		this.props.onClick(realRating); // Parent onClick function
	}

	bStar = (r) => {
		return (
			<h4
				key={r}
				className="rating-star-icon"
				onClick={() => this.adjustRating(r)}
			>
				★
			</h4>
		);
	}

	wStar = (r) => {
		return (
			<h4
				key={r}
				className="rating-star-icon"
				onClick={() => this.adjustRating(r)}
			>
				☆
			</h4>
		);
	}

	// When rating is not 0
	getRating = () => {
		const { rating } = this.state;
		const { bStar, wStar } = this;
		let stars = [];

		for (let i = 1 ; i <= this.props.size ; ++i) {
			stars.push(i > rating ? this.wStar(i) : this.bStar(i));
		}

		return stars;
	}

	render() {
		const stars = this.getRating();

		return (
			<div className="rating-container">
				{stars}
			</div>
		);
	}
}

Rating.propTypes = {
	onClick: PropTypes.func,
	size: PropTypes.number,
}

export default Rating;
