import React from 'react';
import { Redirect } from 'react-router-dom';

//Create the css for ActivePage
class GameList extends React.Component {
    state = { toGame: false }    

    handleGameClick = (gameId,callback) => {
        console.log('clicked: ',gameId);
        callback(gameId);
        this.setState({gameId: gameId, toGame: true});
    }
    
    render() {
        let rows=[];
        this.props.gameList.forEach(
            (gameId) => {
                rows.push(
                    <li onClick={() => this.handleGameClick(gameId, this.props.itemOnClick)} key={gameId}>
                        {gameId}
                    </li>
                );
            }
        );

        if (this.state.toGame === true) {
            return <Redirect to={`/game/${this.state.gameId}`} />
        }

        return (
            <div id="game-list-wrapper">
                <ul id="games-list">
                    {rows}
                </ul>   
            </div>
        );

    }
}

export default GameList;
