import React, { useState, useRef, useEffect } from 'react'
import { connect, disconnect } from "./../api/setup_viewer"
import "./Simulation.css"
import { Path } from '../components/path';
import { PositionGraph } from '../components/positionGraph';
import ControlPanel from '../components/controlPanel';

let states = {
    STATE_INIT: 0,
    STATE_READY: 1,
    STATE_PLAY: 2,
    STATE_DONE: 3,
}

let count = -1
let text_info = [
    {
      "command": "INFO",
      "path": "m 155 248 C 242 202 242 202 324 253",
      "checkpoints": [
        [
          216.8894113563816,
          218.28191356026326
        ],
        [
          237.6297437115229,
          214.140689373391
        ],
        [
          258.517121296062,
          217.21547657093788
        ],
        [
          324,
          253
        ]
      ],
      "current_state": 1
    },
    {
      "command": "INFO",
      "robot": {
        "position": [
          154.11573309491453,
          248.00028585745807
        ],
        "angle": -0.0028405119967596887
      },
      "target": [
        21.47000556696537,
        11.28347655389777
      ],
      "current_state": 2
    },
    {
      "command": "INFO",
      "robot": {
        "position": [
          154.11823182115563,
          249.77932647291854
        ],
        "angle": 9.998308612189659
      },
      "target": [
        21.47000556696537,
        11.28347655389777
      ],
      "current_state": 2
    },
    {
      "command": "INFO",
      "robot": {
        "position": [
          154.44287846773284,
          246.05963536831788
        ],
        "angle": 18.62135338749187
      },
      "target": [
        22.367465520868706,
        11.748113344232877
      ],
      "current_state": 2
    },
    {
      "command": "INFO",
      "robot": {
        "position": [
          155.852331977807,
          249.37904100628458
        ],
        "angle": 18.265601750333875
      },
      "target": [
        22.367465520868706,
        11.748113344232877
      ],
      "current_state": 2
    },
    {
      "command": "INFO",
      "robot": {
        "position": [
          159.13831043969518,
          244.35636846622955
        ],
        "angle": 20.54426096791
      },
      "target": [
        26.8614375478287,
        14.058352069721678
      ],
      "current_state": 2
    },
    {
      "command": "INFO",
      "robot": {
        "position": [
          164.69885157666693,
          246.21768527907156
        ],
        "angle": 20.463435302775615
      },
      "target": [
        30.466406225331866,
        15.88737073587302
      ],
      "current_state": 2
    },
    {
      "command": "INFO",
      "robot": {
        "position": [
          167.8060132747258,
          241.15500301026887
        ],
        "angle": 22.193519017133745
      },
      "target": [
        34.98848740378216,
        18.142068729953223
      ],
      "current_state": 2
    },
    {
      "command": "INFO",
      "robot": {
        "position": [
          173.3983460284894,
          242.86635357337477
        ],
        "angle": 22.15271463376772
      },
      "target": [
        38.622063433111975,
        19.91355526384092
      ],
      "current_state": 2
    },
    {
      "command": "INFO",
      "robot": {
        "position": [
          176.3591342979692,
          237.7092687421981
        ],
        "angle": 23.967765127466116
      },
      "target": [
        43.18904738977545,
        22.075792907883624
      ],
      "current_state": 2
    },
    {
      "command": "INFO",
      "robot": {
        "position": [
          182.0002495756493,
          239.24880999631608
        ],
        "angle": 23.881265409605653
      },
      "target": [
        46.86710213011156,
        23.75292758146861
      ],
      "current_state": 2
    },
    {
      "command": "INFO",
      "robot": {
        "position": [
          184.80007636049385,
          234.00458602450502
        ],
        "angle": 25.510160723904313
      },
      "target": [
        51.50214628386732,
        25.764971568399403
      ],
      "current_state": 2
    },
    {
      "command": "INFO",
      "robot": {
        "position": [
          190.49129229161787,
          235.3790792312087
        ],
        "angle": 25.37187113145921
      },
      "target": [
        55.245861785069394,
        27.289780316989948
      ],
      "current_state": 2
    },
    {
      "command": "INFO",
      "robot": {
        "position": [
          193.14813903592633,
          230.06386041779126
        ],
        "angle": 26.617286652037617
      },
      "target": [
        59.978181896339805,
        29.060520013205917
      ],
      "current_state": 2
    },
    {
      "command": "INFO",
      "robot": {
        "position": [
          198.8993640101748,
          231.3033363531227
        ],
        "angle": 26.41347361012544
      },
      "target": [
        61.8894113563816,
        29.718086439736737
      ],
      "current_state": 2
    },
    {
      "command": "INFO",
      "robot": {
        "position": [
          201.4536995985839,
          225.942912161121
        ],
        "angle": 27.287487144624304
      },
      "target": [
        61.8894113563816,
        29.718086439736737
      ],
      "current_state": 1
    },
    {
      "command": "INFO",
      "robot": {
        "position": [
          207.2373217623964,
          227.09367728817574
        ],
        "angle": 27.16571647446576
      },
      "target": [
        61.8894113563816,
        29.718086439736737
      ],
      "current_state": 1
    },
    {
      "command": "INFO",
      "robot": {
        "position": [
          209.7273912257056,
          221.7007750497399
        ],
        "angle": 29.226750336622736
      },
      "target": [
        61.8894113563816,
        29.718086439736737
      ],
      "current_state": 1
    },
    {
      "command": "INFO",
      "robot": {
        "position": [
          215.46204061475828,
          222.7406283486696
        ],
        "angle": 28.798047650213487
      },
      "target": [
        82.6297437115229,
        33.85931062660899
      ],
      "current_state": 1
    },
    {
      "command": "INFO",
      "robot": {
        "position": [
          217.76852741646053,
          217.280284794198
        ],
        "angle": 28.472385449776233
      },
      "target": [
        82.6297437115229,
        33.85931062660899
      ],
      "current_state": 1
    }
]
let buffer = []

export function Simulation() {
    const [ip, setIP] = useState("localhost");
    const [port, setPort] = useState("1234")
    const [connected, setConnected] = useState(false);
    const [available, setAvailable] = useState(false);
    const [socket, setSocket] = useState(null);
    const [info, setInfo] = useState({});
    const [playing, setPlaying] = useState(false);
    const [current_state, setCurrentState] = useState(states.STATE_INIT);
    const pathRef = useRef();
    const elm = useRef();


    // ############################################ Socket ############################################
    function socketSend(mssg, buffered=false) {
        if (available) {
            if (buffered && buffer.length > 0) {mssg = buffer.shift(); console.log('buffer')}
            else if (buffered) return
            // console.log(mssg)
            setAvailable(false)
            socket.send(mssg)
            
            // Testing
            // setTimeout(() => {
            //     // setInfo([++count])
            //     setAvailable(true)
            // }, 2000);
        }
        else if (!buffered) buffer.push(mssg)
        // console.log(buffer)
    }
    function createWebsocket() {
        // console.log('Trying to connect...')
        let new_socket = new WebSocket('ws://localhost:7374')
        new_socket.onopen = () => {
            // console.log('WebSocket Client Connected')
            console.log(buffer)
            setSocket(new_socket)
            setAvailable(true)
        }
        new_socket.onmessage = (message) => {
            message = JSON.parse(message.data)
            // console.log(message)

            if (message.command == 'INFO') setInfo(message)

            if (message.current_state) setCurrentState(message.current_state)
        }
        new_socket.onclose = () => {
            // console.log('disconnected')
            createWebsocket()
        }
    }
    useEffect(() => {
        if (available) socketSend(null, true)
    }, [available])


    // Testing
    // useEffect(() => {
    //     setTimeout(() => {
    //         setCurrentState((current_state + 1) % 4)
    //     }, 5000);
    // }, [current_state])

    // ############################################ Connect ############################################
    function handleConnect() {
        setConnected(true)
    }
    useEffect(() => {
        if (connected && elm.current) {
            connect(ip, port, elm.current)
            createWebsocket()
        }
        // Testing
        // createWebsocket() 
    }, [connected, elm])

    // ############################################ Ping ############################################
    function handlePing() {
        // console.log(socket, available)
        if (socket && available) {
            let mssg = { command: 'PING' }
            // console.log(mssg.command, '########################')
            socketSend(JSON.stringify(mssg))
        }
    }
    useEffect(() => {
        if (connected && socket && available) {
            const interval = setInterval(() => {
              handlePing()
            }, 2000);
            return () => {
              clearInterval(interval);
            };
        }
    }, [connected, socket, available])

    
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
        let path = pathRef.current.getPath().getAttribute('d')
        let width = pathRef.current.getPath().parentNode.getBoundingClientRect().width
        let height = pathRef.current.getPath().parentNode.getBoundingClientRect().height
        // console.log("this is the <path> DOM element:\n", path, width, height)

        if (socket) {
            let mssg = {
                command: 'PATH',
                path: {
                    path_str: path,
                    width,
                    height,
                },
            }
            // console.log(mssg.command)
            socketSend(JSON.stringify(mssg))
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

    // ############################################ Toggle ############################################
    function handleToggle() {
        if (socket) {
            let mssg = {
                command: playing ? 'PAUSE' : 'PLAY'
            }
            // console.log(mssg.command)
            socketSend(JSON.stringify(mssg))
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
                            <div className="graph"><PositionGraph data={info}/></div>
                            <div className="controller">
                                {available ? 'available' : 'not'}
                                <h1>{Object.keys(states).find(key => states[key] === current_state)}</h1>
                            <ControlPanel
                                run={sendPath}
                                reset={resetSimulation}
                                clear={clearPath}
                                upload={uploadPath}
                                toggle={handleToggle}
                                toggleState={current_state==states.STATE_PLAY ? 'pause' : current_state==states.STATE_READY ? 'play' : null}
                            /></div>
                        </React.Fragment>
                    )
            }
        </div>
    )
}

