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
                    <p>Sensei</p>
                </div>
                <div>
                    <p>Kyle-San</p>
                </div>
            </nav>
          </div>
      </header>
    );
  }
}

export default Header;