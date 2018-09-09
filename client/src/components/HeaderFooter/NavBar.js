import React, { Component, Fragment } from 'react';
import { NavLink } from 'react-router-dom';

// Icons 

import homeIcon from '../../assets/images/home.png';
import learnIcon from '../../assets/images/grasshopper.png';
import teachIcon from '../../assets/images/sensei.png';

// CSS

import './HeaderFooter.css'

class NavBar extends Component {
	constructor(props) {
		super(props);
		this.state = {
			pages: [
				{ name: 'Home', link: '/home', icon: homeIcon, },
				{ name: 'Help me!', link: '/helpme', icon: learnIcon, },
				{ name: 'Let me Assist', link: '/helpyou', icon: teachIcon, },
			],
		};
	}

	render() {
		const { pages } = this.state;

		return (
			<div className="navbar-main">
				<div className="navlink-container">
			 		{pages.map((page, idx) => (
			 			<NavLink key={idx} exact to={page.link} className="navlink">
				 			<img alt={page.name} src={page.icon} className="navbar-icon"/>
		 				</NavLink>
			 		))}
			 	</div>
			</div>
		);
	}
}

export default NavBar;
