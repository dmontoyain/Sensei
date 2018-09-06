
import React, { Component, Fragment } from 'react';

class Avatar extends Component {
	constructor(props){
		super(props);
		this.state = {
			imgAddr: 'https://cdn.intra.42.fr',
			size: 'small',
			user: '',
		};
		this.changeSize = this.changeSize.bind(this);
		this.changeUser = this.changeUser.bind(this);
	}

	componentDidMount() {
	}

	changeUser(e) {
		this.setState({
			user: e.target.value
		});
	}

	changeSize(e) {
		this.setState({
			size: `${e.target.value}`
		});
	}

	render() {
		const { user } = this.state;

		return (
			<Fragment>
				<select onChange={this.changeSize}>
					<option value="small">small</option>
					<option value="medium">mEdIuM</option>
					<option value="large">LARGE</option>
				</select>
				<input onChange={this.changeUser} value={user}/>
				<img src={`https://cdn.intra.42.fr/users/${this.state.size}_${this.state.user}.jpg`} />
			</Fragment>
		)
	}
}

export default Avatar
