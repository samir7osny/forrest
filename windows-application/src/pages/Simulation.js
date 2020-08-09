import React, { useState, useRef, useEffect } from 'react'
import { connect, disconnect } from "./../api/setup_viewer"
import "./Simulation.css"
import { Path } from '../components/path';
import ControlPanel from '../components/controlPanel';
export function Simulation() {
    const [ip, setIP] = useState("localhost");
    const [port, setPort] = useState("1234")
    const [connected, setConnected] = useState(true);
    const pathRef = useRef();
    const elm = useRef();

    function handleConnect() {
        setConnected(true);
    }

    function sendPath() {
        console.log("this is the <path> DOM element:\n", pathRef.current.getPath())
    }

    function clearPath() {
        pathRef.current.clear()
    }

    function uploadPath() {

    }

    function resetSimulation() {

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
                            <div className="controller"><ControlPanel
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

