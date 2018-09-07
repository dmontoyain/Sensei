import React, { Component, Fragment } from 'react';
import { NavLink } from 'react-router-dom';

import testImage from '../../assets/images/test.png'

// CSS

import './HeaderFooter.css'

class NavBar extends Component {
	constructor(props) {
		super(props);
		this.state = {
			pages: [
				{ name: 'Home', link: '/home', },
				{ name: 'Help me!', link: '/gimmehelp', },
				{ name: 'Let me Assist', link: '/iwannahelp', },
			],
		};
	}

	render() {
		const { pages } = this.state;

		return (
			<div className="navbar-main">
				<div className="navbar-icon-container">
					<img src={testImage} className="navbar-icon"/>
				</div>
				<div className="navlink-container">
			 		{pages.map((page, idx) => (
			 			<NavLink key={idx} exact to={page.link} className="navlink">
		 					<p className="navlink-text">{page.name}</p>
		 				</NavLink>
			 		))}
			 	</div>
			</div>
		);
	}
}

			// <Hover
			// 	className="flex flex-wrap"
			// 	hoverElement={<img src={testImage} height='75'/>}
			// >
			// STUFF GOES HERE
			// </Hover>

export default NavBar;
