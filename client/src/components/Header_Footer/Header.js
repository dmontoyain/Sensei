import React, { Component, Fragment } from 'react';
import { NavLink } from 'react-router-dom';

import Hover from '../Extra/Hover';

// CSS
import './Header.css';

// Image

import testImage from '../../assets/images/test.png'

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
			<div className="flex flex-wrap nav-bar">
				<img src={testImage} className="home-icon"/>
		 		{pages.map((page, idx) => (
		 			<NavLink key={idx} exact to={page.link} className="nav-link">
	 					<p className="nav-text">{page.name}</p>
	 				</NavLink>
		 		))}
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

class Header extends Component {
	constructor(props) {
		super(props);
	}

	render() {

	 	return (
	 		<header>
	 			<NavBar />
	 		</header>
	 	);
	}
}

export default Header;
