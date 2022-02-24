import React from 'react';
import { Table, Button } from 'react-bootstrap';

class Messages extends React.Component {
    constructor(props) {
        super();
        this.state = {
            messages: [],
            add: false,
            case: "",
            message: "",
        }

        this.load = this.load.bind(this);
        this.add = this.add.bind(this);
        this.remove = this.remove.bind(this);
        this.showAdd = this.showAdd.bind(this);
        this.hideAdd = this.hideAdd.bind(this);
        this.getList = this.getList.bind(this);
        this.onCase = this.onCase.bind(this);
        this.onMessage = this.onMessage.bind(this);

        this.load();
    }

    add() {
        fetch("/api/addMessage", {
            mode: 'cors',
            method: 'post',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                case: this.state.case,
                message: this.state.message
            })
        })
            .then((res) => res.json())
            .then((res) => {
                this.load();
            })
    }

    remove(id) {
        fetch("/api/removeMessage", {
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
        this.setState({ add: false });
    }

    getList() {
        var messages = this.state.messages.map((messages) => <tr key={messages.id}><td>{messages.case}</td><td>{messages.message}</td><td><Button onClick={() => this.remove(messages.id)} variant="danger">Delete</Button></td></tr>);
        if (!this.state.add) {
            return messages;
        } else {
            messages.push(<tr key="add">
                <td><input placeholder="Case" onChange={this.onCase}></input></td>
                <td><input placeholder="Message" onChange={this.onMessage}></input></td>
                <td><Button onClick={this.add} variant="primary">Add</Button><Button onClick={this.hideAdd} variant="danger">Delete</Button></td>
            </tr>);
            return messages;
        }
    }

    onCase(e) {
        e.preventDefault();
        this.setState({ case: e.target.value });
    }

    onMessage(e) {
        e.preventDefault();
        this.setState({ message: e.target.value });
    }

    load() {
        try {
            fetch("/api/messages", {
                mode: 'cors',
                method: 'get',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
                .then((res) => res.json())
                .then((result) => {
                    this.setState({ add: false, messages: result });
                })
        } catch (error) {
            console.log("Error is" + error);
        }
    }

    render() {
        var messages = this.getList();

        return (
            <Table striped bordered hover>
                <thead>
                    <tr>
                        <th>Case</th>
                        <th>Message</th>
                        <th><Button variant="primary" onClick={this.showAdd}>Add</Button></th>
                    </tr>
                </thead>
                <tbody>
                    {messages}
                </tbody>
            </Table>
        );
    }
}

export default Messages;