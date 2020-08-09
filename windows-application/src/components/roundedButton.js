import React from 'react';
import "./roundedButton.css";
export default function RoundedButton(props) {
    return (
        <button
            style={{
                height: props.size * 4,
                width: props.size * 4,
            }}
            onClick={props.onClick}
            className="rounded-button"
        >
            {props.content}
        </button>
    )
}
