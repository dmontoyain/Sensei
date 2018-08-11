import React, { Component } from 'react';
import '../assets/css/default.min.css'

//Components
import Header from '../components/Header/Header.js';
import ProjectTile from '../components/ProjectTile/ProjectTile.js';
// import ConceptTile from './components/ConceptTile/ConceptTile.js';
import Footer from '../components/Footer/Footer.js';


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
