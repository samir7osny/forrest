import React from "react";
import "./App.css";
import { Navbar } from "./components/navbar";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Redirect,
} from "react-router-dom";
import { Simulation } from "./pages/Simulation";
export function App() {
  return (
    <Router>
      <div className="App">
        <header>
          <Navbar />
        </header>
        {/* A <Switch> looks through its children <Route>s and
            renders the first one that matches the current URL. */}
        <Switch>
          <Route
            exact
            path="/"
            render={() => {
              return <Redirect to="/simulation" />;
            }}
          />
          <Route exact path="/simulation">
            <Simulation />
          </Route>
          <Route exact path="/documentation">
            <Simulation />
          </Route>
          <Route exact path="/team">
            <Simulation />
          </Route>
        </Switch>
      </div>
    </Router>
  );
}
