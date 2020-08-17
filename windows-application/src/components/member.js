import React from "react";
import "./member.css";

export default function Member({ name, pic }) {
  return (
    <div className="member">
      <img src={pic || "https://picsum.photos/200/200"} />
      <h2>{name}</h2>
      <ul class="links"></ul>
    </div>
  );
}
