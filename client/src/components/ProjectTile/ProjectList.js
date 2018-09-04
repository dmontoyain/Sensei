import React from "react";
import apiUserProjectsAvailableMentors from "../../apihandling/api" 
import ProjectListItem from "./ProjectListItem"
import authClient from "../../security/Authentication"

class ProjectList extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            listProjects: [],
            listtype: ""
        }
    }

    componentWillMount(props) {
        //	/api/user/:login/projects/availablementors
        apiUserProjectsAvailableMentors.get("bpierce") //authClient.profile.login
        .then(response => {
            this.setState({
                listProjects: response.data
            })
        })
        .catch(err => {})
    }

    render() {
        return (
            <div className="projectsTable">
                {listProjects.map(projectListItem =>
                    <ProjectListItem type={this.state.listtype}/>
                )}
            </div>
        );
        <Project/>
    }
}