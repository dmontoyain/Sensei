import React, { Component } from 'react';

import './Extra.css';

// const Hover = ({ onHover, children }) => (
// 	<div className="hover">
// 		<div className="hover__no-hover">{children}</div>
// 		<div className="hover__hover">{onHover}</div>
// 	</div>
// );

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

	render() {
		const { children } = this.props;
		return (
			<div onMouseEnter={this.toggleHover} onMouseLeave={this.toggleHover}>
				<div
				>
					Hover Me
				</div>
				<div>
					{ this.state.isHovering && children }
				</div>
			</div>
		);
	}
}

export default Hover;
