import React, { Component } from 'react';

import {
	Route,
	Switch,
	BrowserRouter as Router,
} from 'react-router-dom';

// Higher-Order Components
import withHeaderFooter from '../components/HeaderFooter/HeaderFooter';

// Components
import PrivateRoute from '../components/Authentication/PrivateRoute';
import { Auth } from '../components/Authentication/Auth';
import HelpMe from '../components/Mentoring/HelpMe';
import HelpYou from '../components/Mentoring/HelpYou';
import Visualization from '../components/Visualization/Visualization';

// Page Components
import NotFound from '../components/NotFound/NotFound';
import LogInPage from '../components/LogInPage/LogInPage';
import Home from '../components/Home/Home';



class App extends Component {
	constructor(props) {
		super(props);
		this.state = {};
	}

	render() {
		return (
			<Router>
				<Switch>
					<Route exact path="/" component={LogInPage} />
					<Route exact path="/auth" component={Auth} />
					<PrivateRoute exact path="/home" component={withHeaderFooter(Home)} />
					<PrivateRoute exact path="/helpme" component={withHeaderFooter(HelpMe)} />
					<PrivateRoute exact path="/helpyou" component={withHeaderFooter(HelpYou)} />
					<PrivateRoute exact path="/visualization" component={withHeaderFooter(Visualization)} />
					<Route component={NotFound /* Default Switch Statement returns the NotFound page */ } />
				</Switch>
			</Router>
		);
	}
}

export default App;
