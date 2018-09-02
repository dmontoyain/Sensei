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

//Components
import Header from '../components/Header/Header.js';
import PrivateRoute from '../security/PrivateRoute.js';
import NotFound from '../components/NotFound/NotFound.js';
import ProjectTile from '../components/ProjectTile/ProjectTile.js';
import Home from '../components/Home/Home.js';

// import ConceptTile from './components/ConceptTile/ConceptTile.js';
import Footer from '../components/Footer/Footer.js';


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
					<Header />
					<Switch>
						<Redirect from="/home" to="/" />
						<PrivateRoute exact path="/" component={Home} />
						<PrivateRoute path="/projects" component={ProjectTile} />
						<Route component={NotFound} />
					</Switch>
					<Footer />
				</div>
			</Router>
		);
	}
}

export default App;
