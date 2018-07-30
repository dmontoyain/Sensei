import React, { Component } from 'react';
import './Assets/css/default.min.css'

//Components
import Header from './components/headerComponent/header.js';
import ProjectTile from './components/ProjectTile/ProjectTile.js';
// import ConceptTile from './components/ConceptTile/ConceptTile.js';
import Footer from './components/footerComponent/footer.js';


class App extends Component {
  render() {
    return (
      <div> 
        <Header />
        <ProjectTile />
        {/* <ConceptTile /> */}
        <Footer />
      </div>
    );
  }
}

export default App;
