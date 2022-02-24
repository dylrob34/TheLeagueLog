import React from 'react'
import { Table, Button } from 'react-bootstrap';

class People extends React.Component {
    constructor(props) {
        super();
        this.state = {
            people: [],
            add: false,
            name: "",
            summonerName: "",
        }

        this.loadPeople = this.loadPeople.bind(this);
        this.addPerson = this.addPerson.bind(this);
        this.removePerson = this.removePerson.bind(this);
        this.showAddPerson = this.showAddPerson.bind(this);
        this.hideAddPerson = this.hideAddPerson.bind(this);
        this.getPeopleList = this.getPeopleList.bind(this);
        this.onName = this.onName.bind(this);
        this.onSummonerName = this.onSummonerName.bind(this);

        this.loadPeople();
    }

    addPerson() {
        fetch("/api/addPeople", {
                mode: 'cors',
                method: 'post',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    name: this.state.name,
                    summonerName: this.state.summonerName
                })
            })
            .then((res) => res.json())
            .then((res) => {
                this.loadPeople();
            })
    }

    removePerson(summonerName) {
        fetch("/api/removePeople", {
                mode: 'cors',
                method: 'post',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    summonerName: summonerName
                })
            })
            .then((res) => res.json())
            .then((res) => {
                this.loadPeople();
            })
    }

    showAddPerson() {
        this.setState({ add: true });
    }

    hideAddPerson() {
        this.setState({add: false, name: "", summonerName: ""});
    }

    getPeopleList() {
        var people = this.state.people.map((person) => <tr key={person.id}><td>{person.name}</td><td>{person.summonerName}</td><td><Button onClick={() => this.removePerson(person.summonerName)} variant="danger">Delete</Button></td></tr>);
        if (!this.state.add) {
            return people;
        } else {
            people.push(<tr key="add"><td><input placeholder="name" onChange={this.onName}></input></td>
            <td><input placeholder="summoner name" onChange={this.onSummonerName}></input></td>
            <td><Button onClick={this.addPerson} variant="primary">Add</Button><Button onClick={this.hideAddPerson} variant="danger">Delete</Button></td></tr>);
            return people;
        }
    }

    onName(e) {
        e.preventDefault();
        this.setState({name: e.target.value});
    }

    onSummonerName(e) {
        e.preventDefault();
        this.setState({summonerName: e.target.value});
    }

    loadPeople() {
        try {
            fetch("/api/people", {
                mode: 'cors',
                method: 'get',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
                .then((res) => res.json())
                .then((result) => {
                    this.setState({ add: false, people: result, name: "", summonerName: "" });
                })
        } catch (error) {
            console.log("Error is" + error);
        }
    }

    render() {
        var people = this.getPeopleList();

        return (
            <Table striped bordered hover>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Summoner Name</th>
                        <th><Button variant="primary" onClick={this.showAddPerson}>Add</Button></th>
                    </tr>
                </thead>
                <tbody>
                    {people}
                </tbody>
            </Table>
        );
    }
}



export default People;
