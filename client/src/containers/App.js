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

import '../assets/css/default.min.css'

// Higher-Order Components
import withHeaderFooter from '../components/Header_Footer/HeaderFooter.js';

// Components
import PrivateRoute from '../security/PrivateRoute.js';
import ProjectTile from '../components/ProjectTile/ProjectTile.js';

// Page Components
import NotFound from '../components/NotFound/NotFound.js';
import LogInPage from '../components/LogInPage/LogInPage';
import Home from '../components/Home/Home.js';



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
				<div>
					<Switch>
						<Route exact path="/" component={LogInPage} />
						<PrivateRoute path="/home" component={withHeaderFooter(Home)} />
						<PrivateRoute path="/gimmehelp" component={withHeaderFooter(ProjectTile)} />
						<PrivateRoute path="/iwannahelp" component={withHeaderFooter(ProjectTile)} />
						<Route component={NotFound} />
					</Switch>
				</div>
			</Router>
		);
	}
}

export default App;
