import React from 'react';
import logo from './logo.svg';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';

import { Nav, Navbar, Form, FormControl, Button } from 'react-bootstrap';
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";

import People from './components/people.jsx';
import Cases from './components/cases.jsx';
import Messages from './components/messages.jsx';
import Home from './components/home.jsx';

class App extends React.Component {
  render() {
    return (

      <Router>
          <Navbar bg="light" expand="lg">
            <Navbar.Brand><Link to="/">The League Log</Link></Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
              <Nav className="mr-auto">
                <Nav.Link><Link to="/people">People</Link></Nav.Link>
                <Nav.Link><Link to="/cases">Cases</Link></Nav.Link>
                <Nav.Link><Link to="/messages">Messages</Link></Nav.Link>
              </Nav>
            </Navbar.Collapse>
          </Navbar>
          
        <Switch>
          <Route path="/messages">
            <Messages />
          </Route>
          <Route path="/cases">
            <Cases />
          </Route>
          <Route path="/people">
            <People />
          </Route>
          <Route>
            <Home />
          </Route>
        </Switch>
      </Router>
    );
  }
}

export default App;
