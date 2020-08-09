import React, { createRef, useState, useEffect } from 'react'
import * as d3 from 'd3'
// import { w3cwebsocket as W3CWebSocket } from "websocket";
export function PositionGraph(props) {

    const [width, setWidth] = useState(500);
    const [height, setHeight] = useState(200);
    const margin = {top: 20, right: 20, bottom: 20, left: 20}
    const svgRef = createRef();

    const [points, setPoints] = useState([]);

    useEffect(() => {
        
    }, []);

    useEffect(() => {
        let svg = d3.select(svgRef.current)
            .attr('preserveAspectRatio', 'xMinYMin meet')
            .attr('viewBox', `0 0 ${width} ${height}`)

        let xScale = d3.scaleLinear()
            .domain([0, width])
            .range([margin.left, width - margin.right])
            
        let yScale = d3.scaleLinear()
            .domain([0, height])
            .range([height- margin.bottom, margin.top])

        let line = d3.line()
            .x(d => xScale(d.x))
            .y(d => yScale(d.y))

        let t = d3.transition().duration(500)

        let paths = svg.selectAll('path').data([points])
        paths.exit()
            .transition(t)
            .attr('opacity', 0)
            .remove()
        let paths_enter = paths.enter().append('path')
            .attr('fill', 'none')
            .attr('stroke', 'black')
            .attr('stroke-width', '5')
        let new_paths = paths_enter.merge(paths)
            .attr('d', d=>line(d))
        var oldTotalLengths = new_paths.nodes().map(ele => parseFloat(ele.getAttribute('old_length'))||0)
        var totalLengths = new_paths.nodes().map(ele => ele.getTotalLength())
        console.log(oldTotalLengths, totalLengths)
        new_paths.attr("stroke-dasharray", (d, i)=>totalLengths[i])
            .attr("stroke-dashoffset", (d, i)=>totalLengths[i] - oldTotalLengths[i])
            .transition(t)
            .attr("stroke-dashoffset", 0)
            .attr("old_length", (d, i)=>totalLengths[i])
            
        console.log(new_paths.nodes())

        let bullets = svg.selectAll('circle')
            .data(points)
        bullets.exit()
            .transition(t)
            .attr('r', 0)
            .remove()
        let bullets_enter = bullets.enter()
            .append('circle')
            .attr('r', 0)
            .attr('fill', 'black')
            .attr('cx', (d, i)=>xScale((points[i-1]||points[i]).x))
            .attr('cy', (d, i)=>yScale((points[i-1]||points[i]).y))
            .transition(t)
            .attr('cx', d=>xScale(d.x))
            .attr('cy', d=>yScale(d.y))
            .attr('r', 10)
        // bullets = bullets_enter.merge(bullets)
            
        let texts = svg.selectAll('text')
            .data(points)
        texts.exit()
            .transition(t)
            .attr('font-size', 0)
            .remove()
        let texts_enter = texts.enter()
            .append('text')
            .text((d, i) => i + 1)
            .style("text-anchor", "middle")
            .style("alignment-baseline", "middle")
            .attr('x', (d, i)=>xScale((points[i-1]||points[i]).x))
            .attr('y', (d, i)=>yScale((points[i-1]||points[i]).y))
            .attr('fill', 'white')
            .attr('font-size', 0)
            .transition(t)
            .attr('x', d=>xScale(d.x))
            .attr('y', d=>yScale(d.y))
            .attr('font-size', '10')

        // setTimeout(() => {
        //     let o_points = [
        //         {x: 20, y: 30},
        //         {x: 69, y: 40},
        //         {x: 200, y: 74},
        //         {x: 300, y: 100},
        //         {x: 200, y: 120},
        //         {x: 100, y: 150},
        //     ]
        //     let count = points.length
        //     if(count == o_points.length) setPoints([])
        //     else setPoints(o_points.slice(0, count + 1))
        // }, 1000)
    }, [width, height, margin, points, svgRef]);

    return (
        <div style={{ width: '100%' }}>
            <svg
                style={{ width: '100%', backgroundColor: 'lightgrey' }}
                ref={svgRef}
            >
            </svg>
        </div>
    )
}
