class Game {
  selected_tile = null;
  constructor() {
    this.user_id = "ravery";
    this.games = [];
    this.game = null;
    this.self = this;

    this.fetchGames();
  }
  fetchGames () {
    // clear the current game if there is one
    this.games = [];
    if(this.game) {
      this.game = null;
      document.getElementById("game").innerHTML = "";
      document.querySelector(".game-state").innerHTML = "";
      document.querySelector(".game-turns").innerHTML = "";
    }


    fetch(`/api/v1/game/${this.user_id}`)
      .then((res) => res.json())
      .then((data) => {
        this.games = data.data;
        this.displayGames();

        // Select the first game if there are any
        if(this.games.length > 0) {
          this.selectGame(this.games[0].id);
        }

      });
  }
  createNewGame () {
    fetch("/api/v1/game/create", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          user_id: this.user_id
        })
    })
      .then((res) => res.json())
      .then(() => {
        this.fetchGames();
      });
  }
  displayGames ()  {
    const gamesContainer = document.getElementById("game-list");
    gamesContainer.innerHTML = "";
    this.games.forEach((game) => {
      const gameElement = document.createElement("div");
      gameElement.style.cursor = "pointer";
      gameElement.innerHTML = game.id;
      gameElement.addEventListener("click", () => {
        this.selectGame(game.id);
      });


      const deleteButton = document.createElement("button");
      deleteButton.classList.add("delete-button");
      deleteButton.innerHTML = "Delete";
      deleteButton.addEventListener("click", () => {
        fetch(`/api/v1/game/${this.user_id}/${game.id}`, {
          method: 'DELETE',
        });
          this.fetchGames();
      });
      gameElement.appendChild(deleteButton);

      gamesContainer.appendChild(gameElement);
    });
  }
  selectGame (game_id)  {
    fetch(`/api/v1/game/${this.user_id}/${game_id}`)
      .then((res) => res.json())
      .then((game) => {
        // Unpack the grid
        game.grid = JSON.parse(game.grid);
        this.game = game;

        this.displayGame();
      });
  }
  displayGame () {
    const el = document.getElementById("game");
    el.innerHTML = "";

    const gameStateEl = document.querySelector(".game-state");
    gameStateEl.innerHTML = this.game.state;

    const gameTurnsEl = document.querySelector(".game-turns");
    gameTurnsEl.innerHTML = this.game.turn_count;

    // Render a 4x4 grid
    for (let i = 0; i < this.game.grid.width * this.game.grid.height; i++) {
        const tileEl = document.createElement("div");
        tileEl.id = `tile-${i}`;
        tileEl.classList.add("tile");

        const tileSize= 64;

        // set the position
        const x = (i % this.game.grid.width) * tileSize;
        const y = Math.floor(i / this.game.grid.width) * tileSize;

        tileEl.style.left = `${x}px`;
        tileEl.style.top = `${y}px`;

        if(this.game.grid.tiles[i].matched) {
          tileEl.classList.add("disabled");
        }

        // set the text
        tileEl.innerHTML = this.game.grid.tiles[i].match_id;

        tileEl.addEventListener("click", () => {
          this.onSelectTile(this.game.grid.tiles[i]);
        });

        el.appendChild(tileEl);
    }
  }
  onSelectTile (tile) {
    document.getElementById(`tile-${tile.id}`).classList.add("selected-tile");
    if(this.selected_tile) {
      if(this.check_for_match(tile)){
        return;
      }
      setTimeout(() => {
        document.getElementById(`tile-${this.selected_tile.id}`).classList.remove("selected-tile");
        document.getElementById(`tile-${tile.id}`).classList.remove("selected-tile");
        this.selected_tile = null;
      }, 100);
      return;
    }
    this.selected_tile = tile;
  }
  check_for_match (tile) {
    fetch(`/api/v1/game/${this.user_id}/${this.game.id}/play`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({a: this.selected_tile.id, b: tile.id})
    })
      .then((res) => res.json())
      .then((data) => {
        if(data.error) {
          alert(data.error);
          return;
        }
        this.game = data.data.game;
        this.selectGame(this.game.id);
      });
  }
}

const game = new Game();
window.game = game;
