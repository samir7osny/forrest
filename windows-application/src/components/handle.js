import React from 'react'

export function Handle(props) {
    return (
        props.p1 && props.p2 ? (
            <React.Fragment>
                <path
                    d={`m ${props.p1.x} ${props.p1.y} L ${props.p2.x} ${props.p2.y}`}
                    stroke={`${props.color ? props.color : "red"}`}
                    stroke-width={`${props.width ? props.width : 2}`}
                    fill="none"
                ></path>
                <circle
                    cx={`${props.p1.x}`}
                    cy={`${props.p1.y}`}
                    r={`${props.rad ? props.rad : 5}`}
                    fill={`${props.color ? props.color : "red"}`}
                />
                <circle
                    cx={`${props.p2.x}`}
                    cy={`${props.p2.y}`}
                    r={`${props.rad ? props.rad : 5}`}
                    fill={`${props.color ? props.color : "red"}`}
                />
            </React.Fragment>
        ) : null
    )
}
