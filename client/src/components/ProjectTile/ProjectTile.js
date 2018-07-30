import React, { Component } from 'react';

class ProjectTile extends Component {
    constructor() {
        super();
        this.state = {  projects: [],
                        concepts: [ {name: "pointers", mentors: 9, isConcept: true},
                                    {name: "linked lists", mentors: 5, isConcept: false}] }
    }
    componentWillMount(){
        fetch ( 'https://swapi.co/api/people/?format=json')
        .then( response => response.json() )
        .then( ({results:projects}) => this.setState({projects}))
    }
    filterProjects (e) {
        this.setState({userInputProjects: e.target.value})
    }
    filterConcepts (e) {
        this.setState({userInputConcepts: e.target.value})
    }

  render() {

    let projects = this.state.projects;
    let concepts = this.state.concepts;

    if (this.state.userInputProjects) {
        projects = projects.filter( project =>
            project.name.toLowerCase()
            .includes(this.state.userInputProjects.toLowerCase()))
    }

    if (this.state.userInputConcepts) {
        concepts = concepts.filter( concept =>
            concept.name.toLowerCase()
            .includes(this.state.userInputConcepts.toLowerCase()))
    }

    return (
        <div>
            <div className="gridSearch">
                <input className="search" type="text" placeholder="Search for a project" onChange={this.filterProjects.bind(this)}/>
                <input className="search" type="text" placeholder="Search for a concept" onChange={this.filterConcepts.bind(this)}/>
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
                {concepts.map(concept =>
                                    <div key={concept.name} className="cell" id={concept.mentors > 0 ? "mentorsAvailableTrue" : "mentorsAvailableFalse"}>
                                            <span id="projectName">{concept.name}</span>
                                            <span id="mentorText">Mentors Available:</span>
                                            <span id="mentorsAvailable">{concept.mentors}</span>
                                            <span id="projectNameDisplay">{concept.name}</span>
                                    </div>
                                )}
            </div>
        </div>
    );
  }
}

export default ProjectTile;