import React from "react";
import "./Documentation.css";
import doc from "./../assets/Forrest.pdf";
export default function Documentation() {
  return (
    <div className="documentation">
      <h1>Documentation</h1>
      <a href={doc} target="_blank">
        <p>click here to open the document</p>
      </a>
    </div>
  );
}
