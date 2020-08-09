import React from 'react';
import "./controlPanel.css";
import RoundedButton from './roundedButton'
import { FaSyncAlt, FaTrashAlt, FaRunning, FaUpload } from 'react-icons/fa';

export default function ControlPanel(props) {
    const smallSize = 25;
    const bigSize = 60;
    return (
        <div className="control-panel">
            <RoundedButton size={40} content={<FaRunning size={bigSize} />} onClick={props.run} />
            <div className="small-buttons-container">
                <RoundedButton size={15} content={<FaTrashAlt size={smallSize} />} onClick={props.clear} />
                <RoundedButton size={15} content={<FaSyncAlt size={smallSize} />} onClick={props.reset} />
                <RoundedButton size={15} content={<FaUpload size={smallSize} />} onClick={props.upload} />
            </div>
        </div>
    )
}
