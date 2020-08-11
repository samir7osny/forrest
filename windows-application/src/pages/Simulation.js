import React, { useState, useRef, useEffect } from 'react'
import { connect, disconnect } from "./../api/setup_viewer"
import "./Simulation.css"
import { Path } from '../components/path';
import { PositionGraph } from './PositionGraph';
import ControlPanel from '../components/controlPanel';
export function Simulation() {
    const [ip, setIP] = useState("localhost");
    const [port, setPort] = useState("1234")
    const [connected, setConnected] = useState(true);
    const [available, setAvailable] = useState(false);
    const [socket, setSocket] = useState(null);
    const [playing, setPlaying] = useState(false);
    const pathRef = useRef();
    const elm = useRef();

    function createWebsocket() {
        let socket = new WebSocket('ws://localhost:7374')
        socket.onopen = () => {
            console.log('WebSocket Client Connected')
            setSocket(socket)
            setAvailable(true)
        }
        socket.onmessage = (message) => {
            message = JSON.parse(message.data)
            console.log(message)
            setAvailable(true)
        }
        socket.onclose = () => {
            createWebsocket()
        }
    }

    function handlePing() {
        console.log(socket, available)
        if (socket && available) {
            console.log('ping')
            let mssg = { command: 'PING' }
            socket.send(JSON.stringify(mssg))
            setAvailable(false)
        }
    }

    function handleConnect() {
        setConnected(true)
    }

    useEffect(() => {
        if (connected && elm.current) {
            connect(ip, port, elm.current)
            createWebsocket()
        }
    }, [connected, elm])

    useEffect(() => {
        if (connected && socket && available) {
            const interval = setInterval(() => {
              handlePing()
            }, 5000);
            return () => {
              clearInterval(interval);
            };
        }
    }, [connected, socket, available])

    function sendPath() {
        let path = pathRef.current.getPath().getAttribute('d')
        let width = pathRef.current.getPath().parentNode.getBoundingClientRect().width
        let height = pathRef.current.getPath().parentNode.getBoundingClientRect().height
        console.log("this is the <path> DOM element:\n", path, width, height)

        if (socket && available) {
            let mssg = {
                command: 'PATH',
                path: {
                    path_str: path,
                    width,
                    height,
                },
            }
            socket.send(JSON.stringify(mssg))
            setAvailable(false)
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
        if (socket && available) {
            let mssg = {
                command: playing ? 'PAUSE' : 'PLAY'
            }
            socket.send(JSON.stringify(mssg))
            setAvailable(false)
            setPlaying(!playing)
        }
    }
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
                            <div className="graph"><PositionGraph /></div>
                            <div className="controller">
                                {available ? 'available' : 'not'}
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

