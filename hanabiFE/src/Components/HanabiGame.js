import React from 'react';


//Create the css for ActivePage
class HanabiGame extends React.Component {
    state = { gameId: null }
    componentDidMount() {
        this.setState({gameId: this.props.match.params.game_id})

    }

    render() {
        return (
            <div id="game-wrapper">
                Game!<br></br>
                <h3>ID: {this.state.gameId}</h3>
            </div>
        );

    }
}

export default HanabiGame;
