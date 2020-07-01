import React from 'react';
import "./navbar.css"
export function Navbar() {
    return (
        <nav>
            <div class="logo">
                <h1>Forrest</h1>
            </div>
            <ul>
                <li>
                    Simulation
                </li>
                <li>
                    Documentation
                </li>
                <li>
                    Our team
                </li>
            </ul>
            <div class="code">
                Github
            </div>
        </nav>
    );
}