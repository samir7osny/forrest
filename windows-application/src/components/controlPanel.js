import React from 'react';
import "./controlPanel.css";
import RoundedButton from './roundedButton'
import { FaStarHalfAlt, FaSyncAlt, FaTrashAlt, FaRunning, FaUpload } from 'react-icons/fa';

export default function ControlPanel() {
    const smallSize = 25;
    const bigSize = 60;
    return (
        <div className="control-panel">
            <RoundedButton size={40} content={<FaRunning size={bigSize} />} onClick={() => console.log("Hello")} />
            <div className="small-buttons-container">
                <RoundedButton size={15} content={<FaTrashAlt size={smallSize} trans />} onClick={() => console.log("Hello")} />
                <RoundedButton size={15} content={<FaSyncAlt size={smallSize} />} onClick={() => console.log("Hello")} />
                <RoundedButton size={15} content={<FaUpload size={smallSize} trans />} onClick={() => console.log("Hello")} />
            </div>
        </div>
    )
}
