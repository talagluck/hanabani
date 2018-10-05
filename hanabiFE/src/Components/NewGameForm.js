import React from 'react';

//Create the css for ActivePage
class NewGameForm extends React.Component {
    constructor(props) {
        super(props);
        this.state={newGameName:''}
    }

    handleChange = (event) => {
        this.setState({ newGameName: event.target.value });
    }

    createGame = (event) => {
        event.preventDefault();
        this.props.callback(this.state.newGameName);
    }

    render() {
        return (
            <div id="New-game-form">
                <form action="" id="create-game">
                    <input type="text" id="create-game-name" onChange={this.handleChange} value={this.state.newGameName} />
                    <button onClick={this.createGame} type="submit" value="submit">Submit</button>
                </form>
            </div>
        );

    }
}

export default NewGameForm;
