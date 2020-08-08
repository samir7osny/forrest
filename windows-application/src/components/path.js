import React, { createRef, useState, useEffect } from 'react'
import { Handle } from './handle';
import "./path.css"
export function Path(props) {
    const pathRef = createRef();
    const svgRef = createRef();
    const [path, setPath] = useState([]);
    const [lastElm, setLastElm] = useState({});
    const [handleP1, setHandleP1] = useState();
    const [handleP2, setHandleP2] = useState();
    let [counter, setCounter] = useState(0);
    function createPointHead(point, rad) {
        let circ = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        circ.setAttribute("cx", point.x);
        circ.setAttribute("cy", point.y);
        circ.setAttribute("r", rad);
        circ.setAttribute("class", "point");
        let text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        text.textContent = counter;
        text.setAttributeNS(null, "x", point.x);
        text.setAttributeNS(null, "y", point.y + 10);
        text.setAttributeNS(null, "text-anchor", "middle");
        text.setAttribute("class", "point-text");
        text.style.userSelect = "none"
        setCounter(counter + 1)
        return [circ, text];
    }

    function addPoint(p) {
        let type = path.length ? "L" : "m"
        if (path.length && JSON.stringify(p) === JSON.stringify(path[path.length - 1].p))
            return
        setLastElm({ type, p })
        let [circ, text] = createPointHead(p, 30, 'red');
        svgRef.current.appendChild(circ);
        svgRef.current.appendChild(text);
    }

    function addCurve(p, p1, p2) {
        if (path.length && JSON.stringify(p) === JSON.stringify(path[path.length - 1].p))
            return
        setLastElm(
            { type: "C", p, p1, p2 }
        )
    }

    function pathToString(elm) {
        switch (elm.type) {
            case "C":
                return `C ${elm.p1.x} ${elm.p1.y} ${elm.p2.x} ${elm.p2.y} ${elm.p.x} ${elm.p.y}`
            case "L":
            case "m":
                return `${elm.type} ${elm.p.x} ${elm.p.y}`
            default:
                return ""
        }
    }

    //useEffect(() => console.log(path), [path])

    function handleMoveDown(e) {
        const { x, y } = svgRef.current.getBoundingClientRect()
        const point = { x: Math.round(e.clientX - x), y: Math.round(e.clientY - y) }
        addPoint(point)
    }

    function handleDrag(e) {
        if (!path.length)
            return

        const { x, y } = svgRef.current.getBoundingClientRect();
        const point = { x: lastElm.p.x, y: lastElm.p.y };
        const handleX = e.clientX - x
        const handleY = e.clientY - y
        let p1 = { x: Math.round(handleX - 2 * (handleX - point.x)), y: Math.round(handleY - 2 * (handleY - point.y)) };
        let p2 = p1;

        let h1 = p1;
        let h2 = { x: Math.round(handleX), y: Math.round(handleY) };
        setHandleP1(h1);
        setHandleP2(h2);
        addCurve(point, p1, p2);
    }

    function handleMoveUp() {
        if (lastElm) {
            if (path.length && JSON.stringify(lastElm.p) === JSON.stringify(path[path.length - 1].p)) {
                setLastElm({ undefined })
                return
            }
            setPath([...path, lastElm])
            setLastElm({})
        }
    }

    return (
        <div style={{ justifyContent: "center", display: "flex" }}>
            <svg
                style={{ flex: 1, backgroundColor: 'lightgrey' }}
                onMouseDown={(e) => { if (!e.button) handleMoveDown(e) }}
                onMouseUp={(e) => { if (!e.button) handleMoveUp(e) }}
                onMouseMove={(e) => { if (e.buttons === 1) handleDrag(e) }}
                ref={svgRef}
            >
                <Handle
                    p1={handleP1}
                    p2={handleP2}
                    rad={5}
                    width={3}
                    color={getComputedStyle(document.documentElement).getPropertyValue('--logo-dark-color')}
                />
                <path
                    ref={pathRef}
                    d={path.map((point) => pathToString(point)).join(" ") + pathToString(lastElm)}
                    stroke-width="20"
                    fill="none"
                    className="path"
                    style={{
                        filter: "drop-shadow( 0 5px 5px gray)"
                    }}
                    strokeLinecap="round"
                    strokeLinejoin="round"
                />
            </svg>
        </div>
    )
}
