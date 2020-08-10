import React, { useState, useRef, useEffect } from 'react'
import { connect, disconnect } from "./../api/setup_viewer"
import "./Simulation.css"
import { Path } from '../components/path';
import ControlPanel from '../components/controlPanel';
import { w3cwebsocket as W3CWebSocket } from "websocket";
export function Simulation() {
    const [ip, setIP] = useState("localhost");
    const [port, setPort] = useState("1234")
    const [connected, setConnected] = useState(false);
    const [socket, setSocket] = useState({socket: null, available: false});
    const [playing, setPlaying] = useState(false);
    const pathRef = useRef();
    const elm = useRef();

    function handleConnect() {
        let socket = new W3CWebSocket('ws://localhost:7374')
        socket.onopen = () => {
            console.log('WebSocket Client Connected')
            setSocket({socket, available: true})
            setConnected(true)
        }
        socket.onmessage = (message) => {
            let mssg = JSON.parse(message)
            console.log(mssg)
            setSocket({socket, available: true})
        }
    }

    function sendPath() {
        console.log("this is the <path> DOM element:\n", pathRef.current.getPath())
        if (socket.socket && socket.available) {
            let mssg = {
                command: 'PATH',
                path_str: pathRef.current.getPath(),
                width: pathRef.current.parentNode.getBBox().width,
                height: pathRef.current.parentNode.getBBox().height
            }
            socket.send(mssg)
            setSocket({socket, available: false})
            setPlaying(false)
        }
    }

    function clearPath() {
        pathRef.current.clear()
    }

    function uploadPath() {

    }

    function resetSimulation() {
        sendPath()
    }

    function handleToggle() {
        if (socket.socket && socket.available) {
            let mssg = {
                command: playing ? 'PAUSE' : 'PLAY',
            }
            socket.send(mssg)
            setSocket({socket, available: false})
            setPlaying(!playing)
        }
    }
    useEffect(() => { false && connected && connect(ip, port, document.getElementById("playerDiv")) }, [connected])
    return (
        <div className="simulation">
            {
                !connected ? (
                    <div >
                        <h1>Webots streaming viewer</h1>
                        <p>
                            Connect to:
                     </p>
                        <input id="IPInput" type="text" value={ip} onChange={(val) => setIP(val.target.value)} />
                        <input id="PortInput" type="text" value={port} onChange={(val) => setPort(val.target.value)} />
                        <input id="ConnectButton" type="button" value="Connect" onClick={handleConnect} />
                    </div>
                ) : (
                        <React.Fragment>
                            <div id="playerDiv" ref={elm} className="simulator"></div>
                            <div className="svg">
                                <Path
                                    className="svg"
                                    ref={pathRef}
                                />
                            </div>
                            <div className="graph"></div>
                            <div className="controller">
                                
                                <button onClick={handleToggle}>toggle</button>
                            <ControlPanel
                                run={sendPath}
                                reset={resetSimulation}
                                clear={clearPath}
                                upload={uploadPath}
                            /></div>
                        </React.Fragment>
                    )
            }
        </div>
    )
}

