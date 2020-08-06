import React from 'react';
import './App.css';
import { Navbar } from './components/navbar';
import {
  BrowserRouter as Router,
  Switch,
  Route,
} from "react-router-dom";
import { Simulation } from './pages/Simulation';
export function App() {
  return (
    <Router>
      <div className="App">
        <header>
          <Navbar></Navbar>
        </header>
        {/* A <Switch> looks through its children <Route>s and
            renders the first one that matches the current URL. */}
        <Switch>
          <Route path="/">
            <Simulation />
          </Route>
          <Route path="/simulation">
            <Simulation />
          </Route>
          <Route path="/documentation">
            <Simulation />
          </Route>
          <Route path="/team">
            <Simulation />
          </Route>
        </Switch>
      </div>
    </Router>
  );
}
