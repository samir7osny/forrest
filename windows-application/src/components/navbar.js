import React from 'react';
import {
    Link
} from 'react-router-dom';
import "./navbar.css";
import { FaGithub, FaSimplybuilt, FaFileAlt, FaUsers, FaRobot } from 'react-icons/fa';

const linkStyle = {
    textDecoration: "none"
}
export function Navbar() {
    return (
        <nav>
            <Link to="/" style={linkStyle}>
                <div className="logo">
                    <h1><strong>F</strong>orrest</h1>
                </div >
            </Link>
            <ul>
                <li>
                    <Link to="/simulation" style={linkStyle}><FaRobot className="icons" /></Link>
                </li>
                <li>
                    <Link to="/documentation" style={linkStyle}><FaFileAlt className="icons" /></Link>
                </li>
                <li>
                    <Link to="/team" style={linkStyle}><FaUsers className="icons" /></Link>
                </li>
            </ul>
            <div className="code">
                <a href="https://www.google.com" target="_blank" rel="noopener noreferrer" >
                    <FaGithub className="icons" />
                </a>
            </div>
        </nav >
    );
}