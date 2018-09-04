import React, { Component } from 'react';
import ProjectList from "./ProjectList"

class ProjectTile extends Component {
    constructor() {
        super();
        this.state = {
            listProjects: [],
            topics: [],
        }
    }
    filterProjects (e) { 
        this.setState({userInputProjects: e.target.value})
    }
    filterConcepts (e) {
        this.setState({userInputConcepts: e.target.value})
    }

  render() {
    const { listProjects } = this.state;
    // const { topics } = this.state;
    // if (this.state.userInputProjects) {
    //     projects = projects.filter( project =>
    //         project.name.toLowerCase()
    //         .includes(this.state.userInputProjects.toLowerCase()))
    // }

    // if (this.state.userInputConcepts) {
    //     concepts = concepts.filter( concept =>
    //         concept.name.toLowerCase()
    //         .includes(this.state.userInputConcepts.toLowerCase()))
    //         .filter( concept => concept.isConcept === true)
    // }

    return (
        <div className="ProjectsList">
            {
                listProjects.map()
            }
        </div>
        // <div>
        //     {/* <div className="gridSearch">
        //         <input className="search" type="text" placeholder="Search for a project" onChange={this.filterProjects.bind(this)}/>
        //         <input className="search" type="text" placeholder="Search for a concept" onChange={this.filterConcepts.bind(this)}/>
        //     </div> */}
        //     <div className="grid">
        //         {listProjects.map(item =>
        //                             <div key={item.name} className="cell" id={item.mass > 100 ? "mentorsAvailableTrue" : "mentorsAvailableFalse"}>
        //                                     <span id="projectName">{item.name}</span>
        //                                     <span id="mentorText">Mentors Available:</span>
        //                                     <span id="mentorsAvailable">{item.mass}</span>
        //                                     <span id="projectNameDisplay">{item.name}</span>
        //                             </div>
        //                         )}
        //         {concepts.map(concept =>
        //                     <div key={concept.name} className="cell" id={concept.mentors > 0 ? "mentorsAvailableTrue" : "mentorsAvailableFalse"}>
        //                             <span id="projectName">{concept.name}</span>
        //                             <span id="mentorText">Mentors Available:</span>
        //                             <span id="mentorsAvailable">{concept.mentors}</span>
        //                             <span id="projectNameDisplay">{concept.name}</span>
        //                     </div>
        //                 )}
        //     </div>
        // </div>
    );
  }
}

export default ProjectTile;
