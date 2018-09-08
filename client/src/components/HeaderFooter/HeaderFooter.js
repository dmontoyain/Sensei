import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';

import NavBar from './NavBar';

import './HeaderFooter.css';

class Header extends Component {
	constructor(props) {
		super(props);
	}

	render() {

	 	return (
	 		<header className="header-container">
	 			<NavBar />
	 		</header>
	 	);
	}
}

class Footer extends Component {
  render() {
    return (
        <footer className="footer-container">
            <h4 className="footer-text">@Team Sensei 2018</h4>
        </footer>
    );
  }
}

//	A Higher-Order Component that wraps the given component
//	within a Header and a Footer

const withHeaderFooter = (WrappedComponent) => {
	return class extends Component {
		render () {
			return (
				<div className="header-footer-component-container">
					<Header />
					<div className="wc-container">
						<WrappedComponent />
					</div>
					<Footer />
				</div>
			);
		}
	}
};

export default withHeaderFooter;
