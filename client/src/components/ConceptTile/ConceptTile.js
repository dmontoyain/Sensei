import React, { Component } from 'react';

class ConceptTile extends Component {
    constructor() {
        super();
        this.state = {  concepts: [ 
                                    {name: "pointers", mentors: 9},
                                    {name: "linked lists", mentors: 5}
                                ] }
    }
    // componentWillMount(){
    //     fetch ( 'https://swapi.co/api/people/?format=json')
    //     .then( response => response.json() )
    //     .then( ({results:projects}) => this.setState({projects}))
    // }
    // filterProjects (e) {
    //     this.setState({userInputProjects: e.target.value})
    // }
    filterConcepts (e) {
        this.setState({userInputConcepts: e.target.value})
    }

  render() {

    let concepts = this.state.concepts;

    if (this.state.userInputConcepts) {
        concepts = concepts.filter( concept =>
            concept.name.toLowerCase()
            .includes(this.state.userInputConcepts.toLowerCase()))
    }

    return (
        <div>
            <div className="gridSearch">
                <input className="search" type="text" placeholder="Search for a concept" onChange={this.filterConcepts.bind(this)}/>
            </div>
            <div className="grid">
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

export default ConceptTile;