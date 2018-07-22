import React, { Component } from 'react';
import './Assets/css/default.min.css'

//Components
import Header from './components/headerComponent/header.js';
import HomePage from './components/pages/homePage.js';
import Footer from './components/footerComponent/footer.js';


class App extends Component {
  render() {
    return (
      <div> 
        <Header />
        <HomePage />
        <Footer />
      </div>
    );
  }
}

export default App;
