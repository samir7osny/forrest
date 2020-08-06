import React from 'react';
import {
    Link
} from 'react-router-dom';
import "./navbar.css";
import { FaGithub } from 'react-icons/fa';

const linkStyle = {
    textDecoration: "none"
}
export function Navbar() {
    return (
        <nav>
            <Link to="/" style={linkStyle}>
                <div class="logo">
                    <h1>Forrest</h1>
                </div >
            </Link>
            <ul>
                <li>
                    <Link to="/simulation" style={linkStyle}>Simulation</Link>
                </li>
                <li>
                    <Link to="/documentation" style={linkStyle}>Documentation</Link>
                </li>
                <li>
                    <Link to="/team" style={linkStyle}>Our Team</Link>
                </li>
            </ul>
            <div class="code">
                <a href="https://www.google.com" target="_blank" rel="noopener noreferrer" >
                    <FaGithub className="icons" />
                </a>
            </div>
        </nav >
    );
}