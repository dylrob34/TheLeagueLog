import React from 'react';
import { Table, Button } from 'react-bootstrap';

class Cases extends React.Component {
    constructor(props) {
        super();
        this.state = {
            cases: [],
            add: false,
            id: "",
            case: "",
            description: "",
        }

        this.load = this.load.bind(this);
        this.add = this.add.bind(this);
        this.remove = this.remove.bind(this);
        this.showAdd = this.showAdd.bind(this);
        this.hideAdd = this.hideAdd.bind(this);
        this.getList = this.getList.bind(this);
        this.onId = this.onId.bind(this);
        this.onCase = this.onCase.bind(this);
        this.onDescription = this.onDescription.bind(this);

        this.load();
    }

    add() {
        fetch("/api/addCase", {
                mode: 'cors',
                method: 'post',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    id: this.state.id,
                    case: this.state.case,
                    description: this.state.description
                })
            })
            .then((res) => res.json())
            .then((res) => {
                this.load();
            })
    }

    remove(id) {
        fetch("/api/removeCase", {
                mode: 'cors',
                method: 'post',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    id: id
                })
            })
            .then((res) => res.json())
            .then((res) => {
                this.load();
            })
    }

    showAdd() {
        this.setState({ add: true });
    }

    hideAdd() {
        this.setState({add: false});
    }

    getList() {
        var cases = this.state.cases.map((cases) => <tr key={cases.id}><td>{cases.id}</td><td>{cases.case}</td><td>{cases.description}</td><td><Button onClick={() => this.remove(cases.id)} variant="danger">Delete</Button></td></tr>);
        if (!this.state.add) {
            return cases;
        } else {
            cases.push(<tr key="add">
            <td><input placeholder="Case Id" onChange={this.onId}></input></td>
            <td><input placeholder="Case Name" onChange={this.onCase}></input></td>
            <td><input placeholder="Case Description" onChange={this.onDescription}></input></td>
            <td><Button onClick={this.add} variant="primary">Add</Button><Button onClick={this.hideAdd} variant="danger">Delete</Button></td>
            </tr>);
            return cases;
        }
    }

    onId(e) {
        e.preventDefault();
        this.setState({id: e.target.value});
    }

    onCase(e) {
        e.preventDefault();
        this.setState({case: e.target.value});
    }

    onDescription(e) {
        e.preventDefault();
        this.setState({description: e.target.value});
    }

    load() {
        try {
            fetch("/api/cases", {
                mode: 'cors',
                method: 'get',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
                .then((res) => res.json())
                .then((result) => {
                    this.setState({ add: false, cases: result });
                })
        } catch (error) {
            console.log("Error is" + error);
        }
    }

    render() {
        var cases = this.getList();

        return (
            <Table striped bordered hover>
                <thead>
                    <tr>
                        <th>Id</th>
                        <th>Name</th>
                        <th>Description</th>
                        <th><Button variant="primary" onClick={this.showAdd}>Add</Button></th>
                    </tr>
                </thead>
                <tbody>
                    {cases}
                </tbody>
            </Table>
        );
    }
}

export default Cases;