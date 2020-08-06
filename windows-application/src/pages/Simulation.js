import React, { useState, useRef } from 'react'
import { connect, disconnect } from "./../api/setup_viewer"
import "./Simulation.css"
import { Path } from './Path';
export function Simulation() {
    const [ip, setIP] = useState("localhost");
    const [port, setPort] = useState("1234")
    const elm = useRef();
    return (
        <div class="simulation">
            <div >
                <h1>Webots streaming viewer</h1>
                <p>
                    Connect to:
                 </p>
                <input id="IPInput" type="text" value={ip} onChange={(val) => setIP(val)} />
                <input id="PortInput" type="text" value={port} onChange={(val) => setPort(val)} />
                <input id="ConnectButton" type="button" value="Connect" onClick={() => connect(ip, port, elm.current)} />
            </div>
            <Path x="test" />
            <div id="playerDiv" ref={elm} style={{ flex: 1, width: "100%" }}></div>
        </div>
    )
}

