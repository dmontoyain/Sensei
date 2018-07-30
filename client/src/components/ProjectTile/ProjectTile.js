import React, { Component } from 'react';

class ProjectTile extends Component {
    constructor() {
        super();
        this.state = {  projects: [] }
    }
    componentWillMount(){
        fetch ( 'https://swapi.co/api/people/?format=json')
        .then( response => response.json() )
        .then( ({results:projects}) => this.setState({projects}))
    }
    filterProjects (e) {
        this.setState({userInput: e.target.value})
    }

  render() {

    let projects = this.state.projects;
    if (this.state.userInput) {
        projects = projects.filter( project =>
            project.name.toLowerCase()
            .includes(this.state.userInput.toLowerCase()))
    }

    return (
        <div>
            <div className="projectSearch">
                <input type="text" placeholder="Search for a project" onChange={this.filterProjects.bind(this)}/>
            </div>
            <div className="grid">
                {projects.map(item =>
                                    <div key={item.name} className="cell" id={item.mass > 100 ? "mentorsAvailableTrue" : "mentorsAvailableFalse"}>
                                            <span id="projectName">{item.name}</span>
                                            <span id="mentorText">Mentors Available:</span>
                                            <span id="mentorsAvailable">{item.mass}</span>
                                            <span id="projectNameDisplay">{item.name}</span>
                                    </div>
                                )}
            </div>
        </div>
    );
  }
}

export default ProjectTile;