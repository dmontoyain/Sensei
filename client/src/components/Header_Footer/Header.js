import React, { Component } from 'react';
import { NavLink } from 'react-router-dom';

import Hover from '../Extra/Hover';

// CSS
import './Header.css';

class NavBar extends Component {
	constructor(props) {
		super(props);
		this.state = {
			show: false,
			pages: [
				{ link: '/home', name: 'Home' },
				{ link: '/gimmehelp', name: 'My Projects' },
				{ link: '/iwannahelp', name: 'Projects' },
			],
		};
	}

	toggleNavBar = () => {
		this.setState({ show: !this.state.show })
	}

	render() {
		const { show, pages } = this.state;

		return (
			<Hover component={}>
				<div className="navBar">
			 		{pages.map((page, idx) => (
			 			<NavLink key={idx} exact to={page.link}>
		 					<p>{page.name}</p>
		 				</NavLink>
			 		))}
			 	</div>
			</Hover>
		);
	}
} 

class Header extends Component {
	constructor(props) {
		super(props);
	}

	render() {

	 	return (
	 		<header className="">
	 			<NavBar />
 	 	 	 	<div onClick={() => this._selectItem()}>
 	 	 	 	 	<p id="defaultName">Sensei</p><p id="helpText">Be a mentor</p>
 	 	 	 	</div>
 	 	 	 	<div>
 	 	 	 	 	<p id="defaultName">Kyle-San</p><p id="helpText">Find a mentor</p>
 	 	 	 	</div>
	 		</header>
	 	);
	}
}

export default Header;
