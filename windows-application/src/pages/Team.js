import React from "react";
import "./Team.css";
import Member from "../components/member";

const linkedin = {
  samir: "https://www.linkedin.com/in/samir7osny/",
  touny: "https://www.linkedin.com/in/omar-touny-66934311b/",
  riad: "https://www.linkedin.com/in/riadadel/",
  soli: "",
};
export default function Team() {
  return (
    <div className="team">
      <h1>Team members</h1>
      <div className="members-container">
        <Member
          name="Ahmed Soliman"
          pic={require("./../assets/images/soli.jpg")}
        />
        <Member
          name="Omar Touny"
          pic={require("./../assets/images/touny.jpg")}
        />
        <Member name="Riad Adel" pic={require("./../assets/images/riad.jpg")} />
        <Member
          name="Samir Hosny"
          pic={require("./../assets/images/samir.jpg")}
        />
      </div>
    </div>
  );
}
