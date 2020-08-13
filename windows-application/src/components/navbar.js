import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import "./navbar.css";
import { FaGithub, FaFileAlt, FaUsers, FaRobot } from "react-icons/fa";

const linkStyle = {
  textDecoration: "none",
};
export function Navbar() {
  const [dir, setDir] = useState("/simulation");
  useEffect(() => {
    setDir(document.location.pathname);
  }, []);
  return (
    <nav>
      <ul>
        <li className={dir === "/simulation" ? "active" : null}>
          <Link
            to="/simulation"
            style={linkStyle}
            onClick={() => setDir("/simulation")}
          >
            <FaRobot className="icons" />
          </Link>
        </li>
        <li className={dir === "/documentation" ? "active" : null}>
          <Link
            to="/documentation"
            style={linkStyle}
            onClick={() => setDir("/documentation")}
          >
            <FaFileAlt className="icons" />
          </Link>
        </li>
        <li className={dir === "/team" ? "active" : null}>
          <Link to="/team" style={linkStyle} onClick={() => setDir("/team")}>
            <FaUsers className="icons" />
          </Link>
        </li>
      </ul>

      <div className="code">
        <a
          href="https://www.google.com"
          target="_blank"
          rel="noopener noreferrer"
        >
          <FaGithub className="icons" />
        </a>
      </div>
    </nav>
  );
}
