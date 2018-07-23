import React, { Component } from 'react';

class HomePage extends Component {

  render() {
    return (
        <div className="grid">
            <div className="cell" id="mentorsAvailableTrue">
              <span id="projectName">printf</span>
              <span id="mentorText">Mentors Available:</span>
              <span id="mentorsAvailable">5</span>
            </div>
            <div className="cell" id="mentorsAvailableTrue">
              <span id="projectName">ls</span>
              <span id="mentorText">Mentors Available:</span>
              <span id="mentorsAvailable">2</span>
            </div>
            <div className="cell" id="mentorsAvailableFalse">
              <span id="projectName">malloc</span>
              <span id="mentorText">Mentors Available:</span>
              <span id="mentorsAvailable">0</span>
            </div>
            <div className="cell" id="mentorsAvailableTrue">
              <span id="projectName">beginner exam</span>
              <span id="mentorText">Mentors Available:</span>
              <span id="mentorsAvailable">15</span>
            </div>
            <div className="cell" id="mentorsAvailableTrue">
              <span id="projectName">wolf 3d</span>
              <span id="mentorText">Mentors Available:</span>
              <span id="mentorsAvailable">2</span>
            </div>
            <div className="cell" id="mentorsAvailableTrue">
              <span id="projectName">fdf</span>
              <span id="mentorText">Mentors Available:</span>
              <span id="mentorsAvailable">7</span>
            </div>
            <div className="cell" id="mentorsAvailableTrue">
              <span id="projectName">fractol</span>
              <span id="mentorText">Mentors Available:</span>
              <span id="mentorsAvailable">4</span>
            </div>
            <div className="cell" id="mentorsAvailableTrue">
              <span id="projectName">filler</span>
              <span id="mentorText">Mentors Available:</span>
              <span id="mentorsAvailable">8</span>
            </div>
            <div className="cell" id="mentorsAvailableFalse">
              <span id="projectName">lemin</span>
              <span id="mentorText">Mentors Available:</span>
              <span id="mentorsAvailable">0</span>
            </div>
        </div>
    );
  }
}

export default HomePage;