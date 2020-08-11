import React, { createRef, useState, useEffect } from 'react'
import * as d3 from 'd3'
// import { w3cwebsocket as W3CWebSocket } from "websocket";
export function PositionGraph(props) {

    const [width, setWidth] = useState(0);
    const [height, setHeight] = useState(0);
    const margin = {top: 20, right: 20, bottom: 20, left: 20}
    const svgRef = createRef();

    // const [points, setPoints] = useState([]);
    // const [points2, setPoints2] = useState([]);
    const [count, setCount] = useState(0);
    const [arrow, setArow] = useState({position: {x: 200, y: 200}, angle:0});

    function setSVGSize() {
        let svg_current = svgRef.current
        if (svg_current) {
            setWidth(svg_current.getBoundingClientRect().width)
            setHeight(svg_current.getBoundingClientRect().height)
        }
    }

    useEffect(() => {
        setSVGSize()
        window.addEventListener('resize', setSVGSize);
    
        return () => {
          window.removeEventListener('resize', setSVGSize);
        };
      }, [svgRef]);

    useEffect(() => {
        // let o_points = [
        //     {x: 20, y: 30},
        //     {x: 69, y: 40},
        //     {x: 200, y: 74},
        //     {x: 300, y: 100},
        //     {x: 200, y: 120},
        //     {x: 100, y: 150},
        // ]

        console.log(width)

        let o_points = [
            {x: 172, y: 109},
            {x: 515, y: 138},
            {x: 545, y: 276},
            {x: 248, y: 394},
        ]

        let points = [], points2 = []

        if(count == o_points.length) points = []
        else points = o_points.slice(0, count + 1)

        if(count == o_points.length) points2 = []
        else points2 = o_points.reverse().slice(0, count + 1)

        let svg = d3.select(svgRef.current)
            // .attr('preserveAspectRatio', 'xMinYMin meet')
            // .attr('viewBox', `0 0 ${width} ${height}`)

        let xScale = d3.scaleLinear()
            .domain([0, width])
            .range([margin.left, width - margin.right])
            
        let yScale = d3.scaleLinear()
            .domain([0, height])
            .range([margin.top, height - margin.bottom])

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
            .style('stroke', 'var(--logo-light-color)')
            .attr('stroke-width', '20')
            .attr('stroke-linecap', 'round')
            .attr('stroke-linejoin', 'round')
        let new_paths = paths_enter.merge(paths)
            .attr('d', d=>line(d))
            .attr('stroke', (d, i)=>i == 0 ? 'black' : 'red')
        var oldTotalLengths = new_paths.nodes().map(ele => parseFloat(ele.getAttribute('old_length'))||0)
        var totalLengths = new_paths.nodes().map(ele => ele.getTotalLength())
        new_paths.attr("stroke-dasharray", (d, i)=>totalLengths[i])
            .attr("stroke-dashoffset", (d, i)=>totalLengths[i] - oldTotalLengths[i])
            .transition(t)
            .attr("stroke-dashoffset", 0)
            .attr("old_length", (d, i)=>totalLengths[i])

        let bullets = svg.selectAll('circle.bullet')
            .data(points)
        bullets.exit()
            .transition(t)
            .attr('r', 0)
            .remove()
        let bullets_enter = bullets.enter()
            .append('circle')
            .attr('r', 0)
            .attr('class', 'bullet')
            .attr('fill', 'black')
            .style('fill', 'var(--logo-light-color)')
            .attr('cx', (d, i)=>xScale((points[i-1]||points[i]).x))
            .attr('cy', (d, i)=>yScale((points[i-1]||points[i]).y))
        bullets_enter.merge(bullets)
            .transition(t)
            .attr('cx', d=>xScale(d.x))
            .attr('cy', d=>yScale(d.y))
            .attr('r', 30)
            
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
            .attr('fill', 'wheat')
            .attr('font-size', 0)
            .style('font-family', '"Righteous", cursive')
        texts_enter.merge(texts)
            .transition(t)
            .attr('x', d=>xScale(d.x))
            .attr('y', d=>yScale(d.y))
            .attr('font-size', 30)

        let arrow_svg = svg.selectAll('svg#arrow')
            .data([arrow])
        arrow_svg.exit()
            .remove()
        let arrow_svg_enter = arrow_svg.enter()
            .append('svg')
            .attr("id", "arrow")
            .attr('x', (d, i)=>xScale(0))
            .attr('y', (d, i)=>yScale(0))
            .attr('width', 60)
            .attr('height', 60)
            .attr('fill', 'red')
        arrow_svg_enter.merge(arrow_svg)
            .attr('viewBox', '0 0 219.151 219.151')
            .html(
                `
                <g>
                    <path d="M109.576,219.151c60.419,0,109.573-49.156,109.573-109.576C219.149,49.156,169.995,0,109.576,0S0.002,49.156,0.002,109.575
                        C0.002,169.995,49.157,219.151,109.576,219.151z M109.576,15c52.148,0,94.573,42.426,94.574,94.575
                        c0,52.149-42.425,94.575-94.574,94.576c-52.148-0.001-94.573-42.427-94.573-94.577C15.003,57.427,57.428,15,109.576,15z"/>
                    <path d="M94.861,156.507c2.929,2.928,7.678,2.927,10.606,0c2.93-2.93,2.93-7.678-0.001-10.608l-28.82-28.819l83.457-0.008
                        c4.142-0.001,7.499-3.358,7.499-7.502c-0.001-4.142-3.358-7.498-7.5-7.498l-83.46,0.008l28.827-28.825
                        c2.929-2.929,2.929-7.679,0-10.607c-1.465-1.464-3.384-2.197-5.304-2.197c-1.919,0-3.838,0.733-5.303,2.196l-41.629,41.628
                        c-1.407,1.406-2.197,3.313-2.197,5.303c0.001,1.99,0.791,3.896,2.198,5.305L94.861,156.507z"/>
                </g>
                `
            )
            .transition(t)
            .attr('x', d=>xScale(d.position.x))
            .attr('y', d=>yScale(d.position.y))
        let old_angles = arrow_svg_enter.merge(arrow_svg).nodes().map(ele => parseFloat(ele.dataset.angle)||0)
        arrow_svg_enter.merge(arrow_svg).attr('data-angle', (d, i)=>([arrow])[i].angle)
        arrow_svg_enter.merge(arrow_svg)
            .selectAll('g')
            .style('transform-origin', `center center`)
            .style('transform', (d, i)=>`rotate(${old_angles[i]}deg)`)
            .transition(t)
            .style('transform', (d, i)=>`rotate(${([arrow])[i].angle}deg)`)

        setTimeout(() => {

            if (count < o_points.length - 1) setCount((count + 1) % (o_points.length + 1))
            if (count == 3) setArow({position: {x: 300, y:200}, angle:30})

        }, 1000)
    }, [width, height, margin, count, svgRef]);

    return (
        <div style={{ width: '100%', height: '100%' }}>
            <svg
                style={{ width: '100%', height:'100%', backgroundColor: 'lightgrey' }}
                ref={svgRef}
            >
            </svg>
        </div>
    )
}
