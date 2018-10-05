import React, { Component } from 'react';
import './App.css';
import { Route, Switch } from 'react-router-dom';
import Hanabi from './hanabi';
import NewGameForm from './Components/NewGameForm.js'
import GameList from './Components/GameList.js'
import HanabiGame from './Components/HanabiGame.js'


class App extends Component {
  constructor(props) {
    // console.log('constructor');
    super(props);
    this.state = {
      connected:false,
      gameList:[],
      clientId:null,
      gameId:null,
      toGame:false,
    }
  }

  componentDidMount(){
    Hanabi.connect(
      (clientId) => {
        this.setState({
          connected: true,
          clientId: clientId
        });
        console.log("2 connected, client id: " + clientId)
      }
    );

    Hanabi.subscribeGameListUpdate(
      gameList => this.setState({gameList:gameList})
    );
  }

  goToGame = (gameId) => {
    this.setState({ gameId: gameId,toGame: true });
  }



  render() {
    return (
      <div className="App">
      <Switch>
            <Route exact path="/" 
              render={
                () => 
                  <div>
                    <NewGameForm callback={Hanabi.joinGame}/>
                    <GameList gameList={this.state.gameList} 
                              itemOnClick={this.goToGame} 
                    />
                  </div>
              }
            /> 

            <Route path="/game/:game_id"
              render={
                (props) =>
                  <div>
                    <HanabiGame {...props} clientId={this.state.clientId} hanabi={Hanabi} />
                  </div>
              }
            />
      </Switch>
      </div>
    );
  }
}

export default App;
