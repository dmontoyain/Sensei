import React,
{
	Component,
} from 'react';

import {
	Route,
	Switch,
	Redirect,
	BrowserRouter as Router,
} from 'react-router-dom';

// import '../assets/css/default.min.css'

// Higher-Order Components
import withHeaderFooter from '../components/HeaderFooter/HeaderFooter';

// Components
import PrivateRoute from '../security/PrivateRoute';
import ProjectTile from '../components/ProjectTile/ProjectTile';
import { HelpMe, HelpYou } from '../components/Mentoring/Projects';

// Page Components
import NotFound from '../components/NotFound/NotFound';
import LogInPage from '../components/LogInPage/LogInPage';
import Home from '../components/Home/Home';



class App extends Component {
	constructor(props) {
		super(props);
		this.state = {};
	}

	// filterRoute = (routeName) => {
	// 	const { routes } = this.state;
	// 	console.log(routeName);
	// 	return (routes.includes(routeName) ? routeName : "notfound");
	// }

	render() {
		return (
			<Router>
				<Switch>
					<Route exact path="/" component={LogInPage} />
					<PrivateRoute path="/home" component={withHeaderFooter(Home)} />
					<PrivateRoute path="/helpme" component={withHeaderFooter(HelpMe)} />
					<PrivateRoute path="/helpyou" component={withHeaderFooter(HelpYou)} />
					<Route component={NotFound} />
				</Switch>
			</Router>
		);
	}
}

export default App;
