import React from 'react';
import './App.css';
import { connect, disconnect } from "./api/setup_viewer"
export default class App extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      ip: "localhost",
      port: "1234",
    };
    this.simuRender = React.createRef();
  }

  componentDidMount() {
    console.log(document.getElementById("IPInput"))
  }

  render() {
    return (
      <div className="App">
        <header>
          <nav>Hello</nav>
        </header>
        <div>
          <h1>Webots streaming viewer</h1>
          <p>
            Connect to:
          </p>
          <input id="IPInput" type="text" value={this.state.ip} onChange={(val) => this.setState({ ip: val })} />
          <input id="PortInput" type="text" value={this.state.port} onChange={(val) => this.setState({ port: val })} />
          <input id="ConnectButton" type="button" value="Connect" onClick={() => connect(this.state.ip, this.state.port, this.elm)} />
        </div>
        <div id="playerDiv" style={{ flex: 1, width: "100%" }}></div>
      </div>
    );
  }
}