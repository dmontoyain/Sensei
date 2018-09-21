import React, { Component, Fragment } from 'react';
import { NavLink } from 'react-router-dom';

import LogOutButton from './LogOutButton';

// Icons 

import senseiTitle from '../../assets/images/senseititle.png';
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
			<div className="navlink-container">
				<div className='main-title'>
					<img className="title-image" src={senseiTitle} alt='Master your inner strength' />
				</div>
				{pages.map((page, idx) => (
					<div key={idx} className="navlink">
						<NavLink  exact to={page.link} >
							<img alt={page.name} src={page.icon} className="navbar-icon"/>
						</NavLink>
					</div>
					))}
				<LogOutButton className="logout"/>				 
			</div>
		);
	}
}

export default NavBar;
