import React, { createRef, useState, useEffect } from 'react'
export function Path(props) {
    const pathRef = createRef();
    const svgRef = createRef();
    const [path, setPath] = useState([]);
    const [lastElm, setLastElm] = useState({});

    function createPointHead(point, rad, color) {
        let circ = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        circ.setAttribute("cx", point.x);
        circ.setAttribute("cy", point.y);
        circ.setAttribute("r", rad);
        circ.setAttribute('fill', color);
        return circ;
    }

    function addPoint(p) {
        let type = path.length ? "L" : "m"
        if (path.length && JSON.stringify(p) === JSON.stringify(path[path.length - 1].p))
            return
        setLastElm({ type, p })
        let circ = createPointHead(p, 5, 'red');
        svgRef.current.appendChild(circ);
    }

    function addCurve(p, p1, p2) {
        if (path.length && JSON.stringify(p) === JSON.stringify(path[path.length - 1].p))
            return
        let circ = createPointHead(p, 5, 'red');
        setLastElm(
            { type: "C", p, p1, p2 }
        )
        svgRef.current.appendChild(circ);
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

    useEffect(() => console.log(path), [path])

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
        let p1 = point;
        if (path[path.length - 1].type === "C")
            p1 = path[path.length - 1].p2;
        let p2 = { x: Math.round(e.clientX - x), y: Math.round(e.clientY - y) };
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
        <div style={{ justifyContent: "center", paddingTop: 19, display: "flex" }}>
            <svg
                style={{ flex: 1, height: "90vh", backgroundColor: 'lightgrey' }}
                onMouseDown={(e) => { if (!e.button) handleMoveDown(e) }}
                onMouseUp={(e) => { if (!e.button) handleMoveUp(e) }}
                onMouseMove={(e) => { if (e.buttons === 1) handleDrag(e) }}
                ref={svgRef}
            >
                <path
                    ref={pathRef}
                    id="lineAB"
                    d={path.map((point) => pathToString(point)).join(" ") + pathToString(lastElm)}
                    stroke="red"
                    stroke-width="3"
                    fill="none"
                />
            </svg>
        </div>
    )
}
