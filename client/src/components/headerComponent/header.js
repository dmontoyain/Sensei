import React, { Component } from 'react';

class Header extends Component {
    _selectItem() {
        console.log("click");
    }
  render() {
    return (
      <header>
          <div>
            <nav className="content">
                <div >
                    <p>Home</p>
                </div>
                <div onClick={() => this._selectItem()}>
                    <p id="defaultName">Sensei</p><p id="helpText">Be a mentor</p>
                </div>
                <div>
                    <p id="defaultName">Kyle-San</p><p id="helpText">Find a mentor</p>
                </div>
            </nav>
          </div>
      </header>
    );
  }
}

export default Header;