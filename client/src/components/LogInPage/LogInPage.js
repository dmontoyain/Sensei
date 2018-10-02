import React, { Fragment, Component } from 'react';
import { Redirect, Route } from 'react-router-dom';
import queryString from 'query-string';
import authClient from '../../security/Authentication';

// Components
import { SendToIntra } from '../Authentication/Auth';

import logo42 from '../../assets/images/logo42.png';
// CSS
import './LogInPage.css';

class BackgroundImage extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			currentImageIdx: 0,
			address: `https://source.unsplash.com/${window.innerWidth}x${window.innerHeight}/?nature`,
		}
	}

	componentDidMount() {
		setInterval(() => {
			let { currentImageIdx } = this.state;
			currentImageIdx = currentImageIdx == 4 ? 0 : currentImageIdx + 1;
			this.setState({
				currentImageIdx: currentImageIdx,
				address: `https://source.unsplash.com/${window.innerWidth + currentImageIdx}x${window.innerHeight}/?nature`,
			});
		}, 10000);
	}

	render() {
		return (
			<div>
				<img className='bg' src={this.state.address}/>
			</div>
		);
	}
  };
  
//   ReactDOM.render(
// 	<BackgroundImage/>,
// 	document.getElementsByClassName('login-root')
//   );

const LogInPage = () =>  {
	const intraAuth = 'https://api.intra.42.fr/oauth/authorize?' +
						queryString.stringify({
							client_id: SENSEI_UUID,
							redirect_uri: `${WEBSITE}/auth`,
							response_type: 'code',
							state: 'thebestshakesareatdennysbecarefulthoughsomeonemightsmashyourcarwindow',
						});

	// If user is already logged in, redirect to Home
	if (authClient.isAuthenticated()) {
		return <Redirect to="/home" />;
	}

	// If they aren't authenticated, clear cached credentials, just in case.
	authClient.clearCredentials();

	return (
		<div className="login-root">
			<BackgroundImage/>
			<div className="logInFull">
				<div className="login-logo">
					<img src={logo42} alt="42 logo"/>
				</div>
				<div className="logInSenseiTitle">
					<h1>Sensei</h1>
				</div>
				<div className="logInSenseiBox">
					<p className="logInSenseiText">Every expert was once a beginner.</p>
				</div>
				{/* <div className="buttom-gradient"> */}
				<div className="logInSenseiSignInBox">
					<a className="sign-submit" href={intraAuth}>
						<div className="buttom-gradient">Sign In</div>
					</a>
				</div>
			</div>
		</div>
	);
}

export default LogInPage;
