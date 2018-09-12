import React, { Component } from 'react';

import classNames from 'classnames';

class Hover extends Component {
	constructor(props) {
		super(props);
		this.state = {
			isHovering: false,
		};
		this.timer = 0;
	}

	toggleHover = () => {
		this.setState({ isHovering: !this.state.isHovering });
	}

	// enableHover = () => {
	// 	this.setState({ isHovering: true });
	// }

	// disableHover = () => {
	// 	this.setState({ isHovering: false });
	// }

	render() {
		const { hoverElement, hideOnHover, className, children } = this.props;
		const { isHovering } = this.state;

		return (
			<div
				onMouseEnter={this.toggleHover}
				onMouseLeave={this.toggleHover}
			>
				<div className={classNames(className)}>
					{ hideOnHover && isHovering ? null : hoverElement}
					{ isHovering && children }
				</div>
			</div>
		);
	}
}

export default Hover;
