import React from 'react';

import Header from './Header';
import Footer from './Footer';

// A Higher-Order Component that wraps the given component within a Header and a Footer

const withHeaderFooter = (WrappedComponent) => {
	return class extends React.Component {
		render () {
			return (
				<div className="flex flex-column">
					<Header />
					<div className="flex-none">
						<WrappedComponent />
					</div>
					<Footer />
				</div>
			);
		}
	}
};

export default withHeaderFooter;
