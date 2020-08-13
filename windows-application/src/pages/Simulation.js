import React, { useState, useRef, useEffect } from "react";
import { connect } from "./../api/setup_viewer";
import "./Simulation.css";
import { Path } from "../components/path";
import { PositionGraph } from "../components/positionGraph";
import ControlPanel from "../components/controlPanel";

let states = {
  STATE_INIT: 0,
  STATE_READY: 1,
  STATE_PLAY: 2,
  STATE_DONE: 3,
};

let buffer = [];

export function Simulation() {
  const [ip, setIP] = useState("localhost");
  const [port, setPort] = useState("1234");
  const [connected, setConnected] = useState(false);
//   const [available, setAvailable] = useState(false);
  const [socket, setSocket] = useState({socket: null, available: false});
  const [info, setInfo] = useState({});
  const [current_state, setCurrentState] = useState(states.STATE_INIT);
  const pathRef = useRef();
  const elm = useRef();

  // ############################################ Socket ############################################
  function socketSend(mssg, buffered = false) {
    if (socket.available) {
      if (buffered && buffer.length > 0) {
        mssg = buffer.shift();
        console.log("buffer");
      } else if (buffered) return;
      console.log('>', JSON.parse(mssg))
      setSocket({socket: null, available: false});
      socket.socket.send(mssg);

      // Testing
      // setTimeout(() => {
      //     // setInfo([++count])
      //     setAvailable(true)
      // }, 2000);
    } else if (!buffered) buffer.push(mssg);
    // console.log(buffer)
  }
  function createWebsocket() {
    // console.log('Trying to connect...')
    let new_socket = new WebSocket("ws://localhost:7374");
    new_socket.onopen = () => {
      // console.log('WebSocket Client Connected')
    //   console.log(buffer);
      setSocket({socket: new_socket, available: true});
    };
    new_socket.onmessage = (message) => {
      message = JSON.parse(message.data);
      console.log('<', message)

      if (message.command === "INFO") setInfo(message);

      if (message.current_state) setCurrentState(message.current_state);
    };
    new_socket.onclose = () => {
      // console.log('disconnected')
      createWebsocket();
    };
  }
  useEffect(() => {
    if (socket.available) socketSend(null, true);
  }, [socket.available]);

  // Testing
  // useEffect(() => {
  //     setTimeout(() => {
  //         setCurrentState((current_state + 1) % 4)
  //     }, 5000);
  // }, [current_state])

  // ############################################ Connect ############################################
  function handleConnect() {
    setConnected(true);
  }
  useEffect(() => {
    if (connected && elm.current) {
      connect(ip, port, elm.current);
      createWebsocket();
    }
    // Testing
    // createWebsocket()
  }, [connected, elm]);

  // ############################################ Ping ############################################
  function handlePing() {
    // console.log(socket, available)
    if (socket.socket && socket.available) {
      let mssg = { command: "PING" };
      // console.log(mssg.command, '########################')
      socketSend(JSON.stringify(mssg));
    }
  }
  useEffect(() => {
    if (connected && socket.socket && socket.available) {
      const interval = setInterval(() => {
        handlePing();
      }, 2000);
      return () => {
        clearInterval(interval);
      };
    }
  }, [connected, socket.socket, socket.available]);

  // Testing
  // useEffect(() => {
  //     const interval = setInterval(() => {
  //         if (count == text_info.length - 1) return
  //         console.log(count)
  //         setInfo(text_info[++count])
  //     }, 2000);
  //     return () => {
  //         clearInterval(interval);
  //     };
  // }, [])

  // ############################################ Path ############################################
  function sendPath() {
    let path = pathRef.current.getPath().getAttribute("d");
    let width = pathRef.current.getPath().parentNode.getBoundingClientRect()
      .width;
    let height = pathRef.current.getPath().parentNode.getBoundingClientRect()
      .height;
    // console.log("this is the <path> DOM element:\n", path, width, height)

    let mssg = {
        command: "PATH",
        path: {
          path_str: path,
          width,
          height,
        },
    }
    setCurrentState(states.STATE_INIT)
    setSocket({socket: null, available: false})
    document.getElementById('resetButton').click()
    buffer.push(JSON.stringify(mssg))

    // if (socket) {
    //   // console.log(mssg.command)
    //   socketSend(JSON.stringify(mssg));
    // }
  }
  function clearPath() {
    pathRef.current.clear();
  }
  function uploadPath() {}
  function resetSimulation() {
    sendPath();
  }

  // ############################################ Toggle ############################################
  function handleToggle() {
    if (socket.socket && (current_state == states.STATE_PLAY || current_state == states.STATE_READY)) {
      let mssg = {
        command: current_state == states.STATE_PLAY ? "PAUSE" : "PLAY",
      };
      // console.log(mssg.command)
      socketSend(JSON.stringify(mssg));
    }
  }

  function getStateString(state) {
    switch (state) {
      case 0:
        return "IDLE";
      case 3:
        return "DONE";
      case 2:
        return "PLAYING";
      default:
        return "READY";
    }
  }
  return (
    <div className="simulation">
      {!connected ? (
        <React.Fragment>
          <div className="logo">
            <img src={require("./../assets/images/forrest.png")} alt="logo" />
          </div>
          <div className="login">
            <h1>Webots streaming viewer</h1>
            <input
              id="IPInput"
              type="text"
              value={ip}
              onChange={(val) => setIP(val.target.value)}
            />
            <input
              id="PortInput"
              type="text"
              value={port}
              onChange={(val) => setPort(val.target.value)}
            />
            <input
              id="ConnectButton"
              type="button"
              value="Connect"
              onClick={handleConnect}
            />
          </div>
        </React.Fragment>
      ) : (
        <React.Fragment>
          <div id="playerDiv" ref={elm} className="simulator"></div>
          <div className="svg">
            <Path className="svg" ref={pathRef} />
          </div>
          <div className="graph">
            <PositionGraph data={info} />
          </div>
          <div className="controller">
            <h1>{getStateString(current_state)}</h1>
            <p className={socket.available ? "available" : "unavailable"}>
              <span style={{ color: "darkgrey" }}>socket: </span>
              {socket.available ? "available" : "unavailable"}
            </p>
            <ControlPanel
              run={sendPath}
              reset={resetSimulation}
              clear={clearPath}
              upload={uploadPath}
              toggle={handleToggle}
              toggleState={
                current_state === states.STATE_PLAY
                  ? "pause"
                  : current_state === states.STATE_READY
                  ? "play"
                  : null
              }
            />
          </div>
        </React.Fragment>
      )}
    </div>
  );
}
